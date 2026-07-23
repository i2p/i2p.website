#!/usr/bin/env python3
"""Fix broken external links by converting them to plain text.

For markdown links [text](broken_url) → text
For HTML links <a href="broken_url">text</a> → text
For bare URLs in IRC logs → wrap in backticks

Applied across all 13 languages.
"""
import os
import re
import sys

LANGUAGES = ["en", "ar", "cs", "de", "es", "fr", "hi", "ko", "pt", "ru", "tr", "vi", "zh"]

# --- Markdown links to delink: [text](url) → text ---
# Each entry is a regex pattern matching the URL in the markdown link.
# The replacement keeps only the link text.
MARKDOWN_DELINK_URLS = [
    # Category 1: dead clearnet sites with .i2p-like names
    r'http://i2pbote\.i2p\.us/?',
    r'https?://(?:www\.)?onioncat\.org/?',
    # Category 4: dead project sites
    r'https?://(?:www\.)?wiki\.vuze\.com/w/I2PHelper\S*',
    r'https?://veracrypt\.codeplex\.com/?',
    r'https?://(?:www\.)?ipredator\.se\S*',
    r'https?://(?:www\.)?relakks\.com/?',
    r'https?://syndie\.de/download\S*',
    r'https?://github\.com/eyedeekay/colluding_sites_attack/?',
    # Category 7: misc
    r'http://old\.nabble\.com/jetty\S*',
    r'https?://owasp\.org/www-community/attacks/Slowloris\S*',
]

# --- HTML links to delink: <a href="url"...>text</a> → text ---
# Matches <a> tags with these URL patterns and replaces with just the inner text.
HTML_DELINK_URLS = [
    r'https?://0x375\.org/?',
    r'https?://notabug\.org/villain/mooni2p\S*',
    r'https?://notabug\.org/acetone/samty\S*',
    r'https?://github\.com/eyedeekay/Jsam\S*',
]

# --- Bare URLs to wrap in backticks ---
# These appear as bare text in IRC meeting logs and get auto-linked by Goldmark.
BARE_URL_PATTERNS = [
    r'https?://(?:www\.)?airhook\.org/?\S*',
    r'https?://cvs\.ofb\.net/airhook\S*',
    r'https?://(?:www\.)?fissure\.org/humour\S*',
    r'https?://(?:www\.)?ovmj\.org/GNUnet\S*',
    r'https?://i2bbparts\.meeh\.no/i2p-browser\S*',
    r'https?://security\.stackexchange\.com/questions/824\S*',
]


def delink_markdown(content):
    """Remove markdown links for broken URLs, keeping anchor text."""
    count = 0
    for url_pattern in MARKDOWN_DELINK_URLS:
        # Match [text](url) where url matches the pattern
        pattern = re.compile(
            r'\[([^\]]+)\]\(' + url_pattern + r'\)',
            re.IGNORECASE
        )
        matches = pattern.findall(content)
        if matches:
            count += len(matches)
            content = pattern.sub(r'\1', content)
    return content, count


def delink_html(content):
    """Remove HTML <a> tags for broken URLs, keeping inner text."""
    count = 0
    for url_pattern in HTML_DELINK_URLS:
        # Match <a href="url" ...>text</a>
        pattern = re.compile(
            r'<a\s+[^>]*href=["\']' + url_pattern + r'["\'][^>]*>(.*?)</a>',
            re.IGNORECASE | re.DOTALL
        )
        matches = pattern.findall(content)
        if matches:
            count += len(matches)
            content = pattern.sub(r'\1', content)
    return content, count


def backtick_bare_urls(content):
    """Wrap bare broken URLs in backticks to prevent auto-linking."""
    count = 0
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    fm_count = 0

    for line in lines:
        stripped = line.strip()

        # Track frontmatter
        if stripped == '---':
            fm_count += 1
            if fm_count <= 2:
                in_frontmatter = fm_count == 1
                result.append(line)
                continue
        if in_frontmatter:
            result.append(line)
            continue

        # Skip code blocks
        if stripped.startswith('```'):
            result.append(line)
            continue

        new_line = line
        for pattern in BARE_URL_PATTERNS:
            # Match bare URL not already in backticks or markdown link
            bare_re = re.compile(
                r'(?<!`)(?<!\]\()(' + pattern + r')(?!`)',
                re.IGNORECASE
            )
            matches = bare_re.findall(new_line)
            if matches:
                count += len(matches)
                new_line = bare_re.sub(lambda m: f'`{m.group(0)}`', new_line)

        result.append(new_line)

    return '\n'.join(result), count


def process_file(filepath, dry_run=False):
    """Process a single file. Returns count of fixes made."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content, md_count = delink_markdown(content)
    content, html_count = delink_html(content)
    content, bare_count = backtick_bare_urls(content)

    total = md_count + html_count + bare_count

    if total > 0 and content != original and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return total


def main():
    dry_run = "--dry-run" in sys.argv

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    content_dir = os.path.join(project_root, "content")

    if not os.path.isdir(content_dir):
        print(f"Error: content directory not found at {content_dir}")
        sys.exit(1)

    if dry_run:
        print("=== DRY RUN ===\n")

    total_fixes = 0
    total_files = 0

    for lang in LANGUAGES:
        lang_dir = os.path.join(content_dir, lang)
        if not os.path.isdir(lang_dir):
            continue

        for root, _, files in os.walk(lang_dir):
            for fname in files:
                if not (fname.endswith('.md') or fname.endswith('.html')):
                    continue

                filepath = os.path.join(root, fname)
                fixes = process_file(filepath, dry_run)

                if fixes > 0:
                    total_fixes += fixes
                    total_files += 1
                    rel_path = os.path.relpath(filepath, project_root)
                    if dry_run:
                        print(f"  {rel_path}: {fixes} fix(es)")

    action = "would fix" if dry_run else "fixed"
    print(f"\nTotal: {total_fixes} links {action} in {total_files} files")


if __name__ == "__main__":
    main()
