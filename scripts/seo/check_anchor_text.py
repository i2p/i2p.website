#!/usr/bin/env python3
"""Detect bare URLs that render without descriptive anchor text."""

from __future__ import annotations

import argparse
import pathlib
import re
from dataclasses import dataclass

CONTENT_ROOT = pathlib.Path("content")
CODE_FENCE = re.compile(r"^```")
MARKDOWN_LINK = re.compile(r"\[[^]]*\]\([^)]*\)")
HTML_LINK = re.compile(r"<a [^>]+>.*?</a>", re.IGNORECASE)
ANGLE_LINK = re.compile(r"<https?://[^>]+>")
PROTOCOL = re.compile(r"https?://")
INLINE_CODE = re.compile(r"`[^`]+`")


@dataclass
class Violation:
    path: pathlib.Path
    line_no: int
    line: str


def scrub_line(line: str) -> str:
    cleaned = MARKDOWN_LINK.sub("", line)
    cleaned = HTML_LINK.sub("", cleaned)
    cleaned = ANGLE_LINK.sub("", cleaned)
    cleaned = INLINE_CODE.sub("", cleaned)
    return cleaned


def scan_file(path: pathlib.Path) -> list[Violation]:
    violations: list[Violation] = []
    in_fence = False
    with path.open(encoding="utf-8") as handle:
        for idx, raw in enumerate(handle, start=1):
            line = raw.rstrip("\n")
            if CODE_FENCE.match(line.strip()):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            cleaned = scrub_line(line)
            if PROTOCOL.search(cleaned):
                violations.append(Violation(path, idx, line.strip()))
    return violations


def iter_markdown(root: pathlib.Path, filters: list[str] | None) -> list[pathlib.Path]:
    def matches(path: pathlib.Path) -> bool:
        if not filters:
            return True
        rel = str(path).lower()
        return any(substring.lower() in rel for substring in filters)

    return sorted(
        p for p in root.rglob("*.md") if p.is_file() and matches(p)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true", help="Print offending lines")
    parser.add_argument(
        "--path-contains",
        action="append",
        default=None,
        help=(
            "Only scan files whose path contains this substring. May be supplied "
            "multiple times."
        ),
    )
    args = parser.parse_args()
    violations: list[Violation] = []
    for path in iter_markdown(CONTENT_ROOT, args.path_contains):
        violations.extend(scan_file(path))
    if args.report and violations:
        current = None
        for violation in violations:
            if violation.path != current:
                print(f"\n{violation.path}")
                current = violation.path
            print(f"  L{violation.line_no:4d}: {violation.line}")
        print()
    if violations:
        print(f"Found {len(violations)} anchor-less URLs across {len({v.path for v in violations})} files.")
        raise SystemExit(1)
    print("No bare URLs detected.")


if __name__ == "__main__":
    main()
