#!/usr/bin/env python3
"""Summarize Google Search Console's anchor-less links export.

The CSV is expected to have the columns:
    Page URL,Link URL,Discovered

Usage:
    python scripts/seo/analyze_anchorless.py --table /path/to/Table.csv

The script normalizes www/beta hosts, deduplicates entries, and
emits counts by site section and by link target to help prioritize fixes.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
from collections import Counter, defaultdict
from urllib.parse import urlparse

SUPPORTED_LANGS = {
    "en",
    "ar",
    "zh",
    "cs",
    "fr",
    "de",
    "hi",
    "ko",
    "pt",
    "ru",
    "es",
    "tr",
    "vi",
}

HOST_NORMALIZATION = {
    "www.i2p.net": "i2p.net",
    "beta.i2p.net": "i2p.net",
}

SECTION_PATTERN = re.compile(r"^(?P<lang>[a-z-]+)/(?P<section>[^/]+)")


def normalize_host(netloc: str) -> str:
    return HOST_NORMALIZATION.get(netloc.lower(), netloc.lower())


def detect_section(path: str) -> tuple[str | None, str]:
    path = path.lstrip("/")
    match = SECTION_PATTERN.match(path)
    if not match:
        return None, "(root)"
    lang = match.group("lang")
    section = match.group("section")
    if lang not in SUPPORTED_LANGS:
        return lang, f"unsupported:{section}"
    return lang, section


def summarize(entries: list[tuple[str, str]]) -> None:
    by_section: Counter[str] = Counter()
    by_lang: Counter[str] = Counter()
    by_link: Counter[str] = Counter()
    examples: defaultdict[str, list[str]] = defaultdict(list)

    for page_url, link_url in entries:
        parsed = urlparse(page_url)
        host = normalize_host(parsed.netloc)
        if host != "i2p.net":
            continue
        lang, section = detect_section(parsed.path)
        by_section[section] += 1
        by_lang[lang or "(none)"] += 1
        by_link[link_url] += 1
        if len(examples[section]) < 5:
            examples[section].append(page_url)

    print("Sections with most anchor-less links:\n")
    for section, count in by_section.most_common(20):
        print(f"{section:20} {count:5d}")
        for example in examples[section]:
            print(f"    - {example}")
    print("\nTop external targets:\n")
    for link, count in by_link.most_common(15):
        print(f"{count:5d}  {link}")
    print("\nCounts by language:\n")
    for lang, count in by_lang.most_common():
        print(f"{lang:8} {count:5d}")


def load_entries(path: pathlib.Path) -> list[tuple[str, str]]:
    entries: set[tuple[str, str]] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            page = row.get("Page URL", "").strip()
            link = row.get("Link URL", "").strip()
            if not page or not link:
                continue
            entries.add((page, link))
    return sorted(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table",
        required=True,
        type=pathlib.Path,
        help="CSV exported from Google Search Console",
    )
    args = parser.parse_args()
    entries = load_entries(args.table)
    if not entries:
        raise SystemExit("No entries parsed from table")
    summarize(entries)


if __name__ == "__main__":
    main()
