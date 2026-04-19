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

# Locales for which we render a language variant of each generated page.
# File paths and commit SHAs/subjects stay literal across locales — only
# page titles, counts, and wrapper prose are translated.
STRINGS = {
    "en": {
        "needs_translation_title": "# Needs translation",
        "needs_translation_count": "{n} file(s) have no zh_CN translation yet.",
        "needs_update_title": "# Needs update",
        "needs_update_count": "{n} file(s) are behind the English original.",
        "commits_to_resolve": "{n} commit(s) to resolve:",
    },
    "zh": {
        "needs_translation_title": "# 待翻译",
        "needs_translation_count": "{n} 个文件尚无 zh_CN 翻译。",
        "needs_update_title": "# 待更新",
        "needs_update_count": "{n} 个文件落后于英文原文。",
        "commits_to_resolve": "需要合入的提交（{n} 个）：",
    },
}


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


def render_needs_translation(records: list[NeedsTranslation], lang: str = "en") -> str:
    s = STRINGS[lang]
    lines = [
        s["needs_translation_title"],
        "",
        s["needs_translation_count"].format(n=len(records)),
        "",
    ]
    for rec in records:
        lines.append(f"- `{rec.path}`")
    lines.append("")
    return "\n".join(lines)


_TRANSLATIONS_PREFIX = "Documentation/translations/"


def _display_path(path: str) -> str:
    """Strip the `Documentation/translations/` prefix so the locale segment
    becomes the visible head of the path (e.g.
    `Documentation/translations/zh_CN/foo.rst` -> `zh_CN/foo.rst`)."""
    if path.startswith(_TRANSLATIONS_PREFIX):
        return path[len(_TRANSLATIONS_PREFIX):]
    return path


def render_needs_update(records: list[NeedsUpdate], lang: str = "en") -> str:
    s = STRINGS[lang]
    lines = [
        s["needs_update_title"],
        "",
        s["needs_update_count"].format(n=len(records)),
        "",
    ]
    for rec in records:
        lines.append(f"## `{_display_path(rec.path)}`")
        lines.append("")
        lines.append(s["commits_to_resolve"].format(n=rec.total))
        lines.append("")
        for c in rec.commits:
            lines.append(f"- `{c.sha}` — {c.subject}")
        lines.append("")
    return "\n".join(lines)


# Must match the `default: true` locale in mkdocs.yml's i18n plugin config.
DEFAULT_LOCALE = "zh"


def _output_filename(stem: str, lang: str) -> str:
    """Match mkdocs-static-i18n's suffix convention: default locale has no
    suffix, non-default gets `.<locale>` before the extension."""
    if lang == DEFAULT_LOCALE:
        return f"{stem}.md"
    return f"{stem}.{lang}.md"


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
    for lang in STRINGS:
        (out_dir / _output_filename("needs-translation", lang)).write_text(
            render_needs_translation(parsed.needs_translation, lang)
        )
        (out_dir / _output_filename("needs-update", lang)).write_text(
            render_needs_update(parsed.needs_update, lang)
        )

    logging.info(
        "Wrote %d needs-translation, %d needs-update, %d skipped (locales: %s)",
        len(parsed.needs_translation),
        len(parsed.needs_update),
        len(parsed.skipped),
        ", ".join(STRINGS),
    )


if __name__ == "__main__":
    main()
