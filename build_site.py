"""Parse TODO_LIST produced by checktransupdate.py and build MkDocs markdown pages."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

TIMESTAMP_RE = re.compile(r"^\[[\d.]+\]\s?")
NO_TRANS_RE = re.compile(r"^No translation in the locale of ")
COMMIT_RE = re.compile(r"^commit ([0-9a-f]+) \(\"(.+)\"\)$")
TOTAL_RE = re.compile(r"^(\d+) commits needs resolving in total$")


@dataclass
class NeedsTranslation:
    path: str


@dataclass
class Commit:
    sha: str
    subject: str


@dataclass
class NeedsUpdate:
    path: str
    commits: list[Commit]
    total: int


@dataclass
class ParsedTodoList:
    needs_translation: list[NeedsTranslation] = field(default_factory=list)
    needs_update: list[NeedsUpdate] = field(default_factory=list)
    skipped: list[list[str]] = field(default_factory=list)


def _strip_prefix(line: str) -> str:
    return TIMESTAMP_RE.sub("", line).rstrip()


def parse_todolist(text: str) -> ParsedTodoList:
    result = ParsedTodoList()
    for raw_block in text.split("\n\n"):
        lines = [_strip_prefix(l) for l in raw_block.splitlines() if l.strip()]
        if not lines:
            continue
        if len(lines) == 2 and NO_TRANS_RE.match(lines[1]):
            result.needs_translation.append(NeedsTranslation(path=lines[0]))
        else:
            m_total = TOTAL_RE.match(lines[-1])
            commits = [COMMIT_RE.match(l) for l in lines[1:-1]]
            if m_total and commits and all(commits):
                result.needs_update.append(
                    NeedsUpdate(
                        path=lines[0],
                        commits=[Commit(sha=m.group(1), subject=m.group(2)) for m in commits],
                        total=int(m_total.group(1)),
                    )
                )
            else:
                result.skipped.append(lines)
                logging.warning("Skipping unrecognized record: %r", lines[0])
    return result


def render_needs_translation(records: list[NeedsTranslation]) -> str:
    lines = [
        "# Needs translation",
        "",
        f"{len(records)} file(s) have no zh_CN translation yet.",
        "",
    ]
    for rec in records:
        lines.append(f"- `{rec.path}`")
    lines.append("")
    return "\n".join(lines)


def render_needs_update(records: list[NeedsUpdate]) -> str:
    lines = [
        "# Needs update",
        "",
        f"{len(records)} file(s) are behind the English original.",
        "",
    ]
    for rec in records:
        lines.append(f"## `{rec.path}`")
        lines.append("")
        lines.append(f"{rec.total} commit(s) to resolve:")
        lines.append("")
        for c in rec.commits:
            lines.append(f"- `{c.sha}` — {c.subject}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Build MkDocs pages from TODO_LIST")
    parser.add_argument("--todo", default="TODO_LIST", help="Path to TODO_LIST")
    parser.add_argument("--out", default="docs", help="Output directory for generated .md")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    text = Path(args.todo).read_text()
    parsed = parse_todolist(text)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "needs-translation.md").write_text(render_needs_translation(parsed.needs_translation))
    (out_dir / "needs-update.md").write_text(render_needs_update(parsed.needs_update))

    logging.info(
        "Wrote %d needs-translation, %d needs-update, %d skipped",
        len(parsed.needs_translation),
        len(parsed.needs_update),
        len(parsed.skipped),
    )


if __name__ == "__main__":
    main()
