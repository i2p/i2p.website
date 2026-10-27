#!/usr/bin/env python3
"""Regenerate static/proposals/*.txt from content/en/proposals/*.md.

The .md files are the source of truth. Each .txt is the downloadable
reStructuredText version linked from the proposal page ("Download Source"),
in the same format as the original proposals: a title block, a
`.. meta::` block built from the front matter, `.. contents::`, then the
body converted with pandoc.

Runs in CI on every push to main and commits any changed .txt files.

Usage: sync_proposal_txt.py [--check]
    --check   Exit 1 if any .txt is out of date, without writing.

Requires pandoc (CI pins the version, so output is stable between runs).
"""
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MD_DIR = PROJECT_ROOT / "content" / "en" / "proposals"
TXT_DIR = PROJECT_ROOT / "static" / "proposals"

# Front matter keys written to the meta block, in the original files' order
META_KEYS = [
    "author", "editor", "created", "thread", "lastupdated", "status",
    "supercedes", "supercededby", "target", "implementedin",
]


def unquote_yaml_scalar(value):
    """Remove one matching pair of outer YAML quotes and undo their escapes."""
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def split_front_matter(text):
    """Return (front matter dict of scalar values, body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv and kv.group(2):
            meta[kv.group(1)] = unquote_yaml_scalar(kv.group(2).strip())
    return meta, text[match.end():]


def normalize_headings(body):
    """Renumber Markdown headings so levels start at 1 and never skip.

    RST infers heading levels from the order underline styles first appear,
    so a skipped level (## then ####) or a deeper heading before the first
    top-level one (### Status before ## Overview) produces invalid RST.
    Each heading's level becomes its depth among the enclosing headings.
    """
    out = []
    stack = []
    fence = None
    for line in body.split("\n"):
        stripped = line.lstrip()
        if fence:
            if stripped.startswith(fence):
                fence = None
        elif stripped.startswith(("```", "~~~")):
            fence = stripped[:3]
        else:
            match = re.match(r"^(#{1,6})(\s.*)$", line)
            if match:
                level = len(match.group(1))
                while stack and stack[-1] >= level:
                    stack.pop()
                stack.append(level)
                line = "#" * len(stack) + match.group(2)
        out.append(line)
    return "\n".join(out)


def body_to_rst(body):
    """Convert the Markdown body to RST."""
    result = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "rst", "--wrap=preserve"],
        input=normalize_headings(body), capture_output=True, text=True, check=True,
    )
    return result.stdout


def build_txt(md_text):
    meta, body = split_front_matter(md_text)
    title = meta.get("title", "")
    rule = "=" * len(title)
    lines = [rule, title, rule, ".. meta::"]
    lines += [f"    :{key}: {meta[key]}" for key in META_KEYS if key in meta]
    lines += ["", ".. contents::", "", ""]
    return "\n".join(lines) + "\n" + body_to_rst(body).rstrip("\n") + "\n"


def main():
    check = "--check" in sys.argv
    stale = []
    for md_path in sorted(MD_DIR.glob("[0-9]*.md")):
        txt_path = TXT_DIR / f"{md_path.stem}.txt"
        new = build_txt(md_path.read_text(encoding="utf-8"))
        old = txt_path.read_text(encoding="utf-8") if txt_path.exists() else None
        if new == old:
            continue
        stale.append(txt_path.relative_to(PROJECT_ROOT))
        if not check:
            txt_path.write_text(new, encoding="utf-8")

    action = "out of date" if check else "updated"
    for path in stale:
        print(f"  {path}")
    print(f"{len(stale)} proposal .txt files {action}")
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main())
