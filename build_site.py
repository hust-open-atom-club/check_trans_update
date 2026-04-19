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
            if m_total and all(commits):
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
