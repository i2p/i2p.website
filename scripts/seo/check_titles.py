#!/usr/bin/env python3
"""
Scan generated HTML files for duplicate <title> elements.

Usage:
    python3 scripts/seo/check_titles.py [--root public] [--csv out.csv]
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
import re


TITLE_PATTERN = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect duplicate <title> tags.")
    parser.add_argument(
        "--root",
        default="public",
        help="Directory to scan (default: %(default)s).",
    )
    parser.add_argument(
        "--path-contains",
        action="append",
        default=None,
        help=(
            "Only scan files whose relative path contains this substring. "
            "May be supplied multiple times. Defaults to ['blog']."
        ),
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan every HTML file (disables --path-contains filtering).",
    )
    parser.add_argument(
        "--csv",
        default=None,
        help="Optional path to write duplicates as CSV.",
    )
    return parser.parse_args()


def should_include(path: Path, filters: List[str] | None, scan_all: bool) -> bool:
    if scan_all or not filters:
        return True
    rel = str(path).lower()
    return any(substring.lower() in rel for substring in filters)


def collect_titles(root: Path, filters: List[str] | None, scan_all: bool) -> Dict[str, List[Path]]:
    mapping: Dict[str, List[Path]] = defaultdict(list)
    for html_file in root.rglob("*.html"):
        rel_path = html_file.relative_to(root)
        if not should_include(rel_path, filters, scan_all):
            continue
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        match = TITLE_PATTERN.search(text)
        if not match:
            continue
        title = match.group(1).strip()
        mapping[title].append(rel_path)
    return mapping


def write_csv(duplicates: Dict[str, List[Path]], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Title", "Occurrences"])
        for title, files in sorted(duplicates.items(), key=lambda item: item[0]):
            writer.writerow([title, "; ".join(str(p) for p in files)])


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"[error] Directory not found: {root}", file=sys.stderr)
        return 2

    filters = args.path_contains or ["blog"]

    titles = collect_titles(root, filters, args.all)
    duplicates = {title: files for title, files in titles.items() if len(files) > 1}

    if args.csv:
        write_csv(duplicates, Path(args.csv))

    if not duplicates:
        print("No duplicate <title> values found.")
        return 0

    print(f"Found {len(duplicates)} duplicate <title> values:")
    for title, files in sorted(duplicates.items(), key=lambda item: len(item[1]), reverse=True):
        print(f"  - {title} ({len(files)} pages)")
        for path in files:
            print(f"      {path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
