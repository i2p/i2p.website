import pytest
import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse


@pytest.fixture(scope="module")
def built_site(build_hugo_site):
    """
    Ensure the site is built once for this module.
    Returns the path to the public directory.
    """
    return build_hugo_site


def get_all_html_files(root: Path):
    return list(root.glob("**/*.html"))


def test_internal_links_in_html(built_site):
    """
    Parse all HTML files and check that internal links point to existing files.

    This test handles Hugo's multilingual setup with relativeURLs = true,
    where links are relative paths like '../en/about/' rather than absolute '/en/about/'.

    Static files (keys, PDFs, images) live at the site root, not under language dirs.
    """
    html_files = get_all_html_files(built_site)
    assert html_files, "No HTML files found in build output"

    broken_links = []
    checked_count = 0

    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # Skip external links, mailto, tel, javascript, anchors
            if href.startswith(("http://", "https://", "mailto:", "tel:", "//", "#", "javascript:")):
                continue

            # Parse the URL to handle query params and fragments
            parsed = urlparse(href)
            path = unquote(parsed.path)

            # Skip empty paths (just fragments like "#section")
            if not path:
                continue

            checked_count += 1
            target = None

            # Resolve the path relative to the HTML file's directory
            # This works for both relative paths (../../foo) and root-relative paths
            if path.startswith("/"):
                # Absolute path from site root (rare with relativeURLs=true)
                rel_path = path.lstrip("/")
                if not rel_path or rel_path.endswith("/"):
                    target = built_site / rel_path / "index.html"
                else:
                    target = built_site / rel_path
                    if not target.exists() and not target.suffix:
                        target = built_site / rel_path / "index.html"
            else:
                # Relative path - resolve from current file's directory
                parent = html_file.parent
                try:
                    target = (parent / path).resolve()
                except OSError:
                    # Handle filename too long or other FS errors
                    broken_links.append((
                        str(html_file.relative_to(built_site)),
                        href,
                        "OSError resolving path"
                    ))
                    continue

                # If target is a directory, look for index.html
                try:
                    if target.is_dir():
                        target = target / "index.html"
                    elif not target.suffix and not target.exists():
                        # No extension and doesn't exist - try as directory
                        target = target / "index.html"
                except OSError:
                    broken_links.append((
                        str(html_file.relative_to(built_site)),
                        href,
                        "OSError checking target"
                    ))
                    continue

            # Check if target exists
            try:
                if not target.exists():
                    broken_links.append((
                        str(html_file.relative_to(built_site)),
                        href,
                        str(target)
                    ))
            except OSError:
                broken_links.append((
                    str(html_file.relative_to(built_site)),
                    href,
                    f"OSError checking existence: {target}"
                ))

    # Generate report if there are broken links
    if broken_links:
        report_path = Path("broken_links_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Broken Links Report\n\n")
            f.write(f"Total links checked: {checked_count}\n")
            f.write(f"Broken links found: {len(broken_links)}\n\n")
            f.write("| Source File | Link | Resolved Path |\n")
            f.write("|-------------|------|---------------|\n")
            for source, link, resolved in broken_links:
                # Escape pipe characters in paths
                link_escaped = link.replace("|", "\\|")
                resolved_escaped = resolved.replace("|", "\\|")
                f.write(f"| {source} | {link_escaped} | {resolved_escaped} |\n")

        print(f"\nGenerated broken links report at: {report_path.absolute()}")
        print(f"Checked {checked_count} links, found {len(broken_links)} broken")

        # Show first few broken links
        print("\nFirst 10 broken links:")
        for source, link, resolved in broken_links[:10]:
            print(f"  {source} -> {link}")

        # Fail the test if there are broken links
        pytest.fail(f"Found {len(broken_links)} broken internal links. See broken_links_report.md for details.")


def test_markdown_internal_links(all_content_files, project_root):
    """
    Regex-based check for [link](url) in Markdown files.

    This checks raw markdown links before Hugo processing.
    Useful for catching typos in relative links between content files.
    """
    broken_md_links = []

    # Regex for standard markdown links [text](target)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')

    for md_file in all_content_files:
        if "node_modules" in str(md_file):
            continue

        # Skip documentation guidelines which contain example links
        if "i2p-documentation-writing-guidelines.md" in md_file.name:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for match in link_pattern.finditer(content):
            url = match.group(1)
            # Clean up title part "link.md 'Title'"
            url = url.split()[0]
            # Strip anchor and query
            url = url.split("#")[0].split("?")[0]

            # Skip external, mailto, shortcodes, and root-relative links
            if url.startswith(("http", "mailto", "#", "{{", "<", "/")):
                continue

            # Skip empty URLs
            if not url:
                continue

            # Relative link - resolve relative to md_file
            target = (md_file.parent / url).resolve()

            # Target could be .md file or a directory (which implies _index.md)
            if not target.exists():
                # Maybe it is just missing extension?
                if not target.suffix:
                    # Try adding .md
                    if not target.with_suffix(".md").exists():
                        # Try _index.md
                        if not (target / "_index.md").exists():
                            broken_md_links.append(f"{md_file.relative_to(project_root)} -> {url}")
                else:
                    broken_md_links.append(f"{md_file.relative_to(project_root)} -> {url}")

    if broken_md_links:
        print(f"\nFound {len(broken_md_links)} potential broken relative links in Markdown:")
        for link in broken_md_links[:20]:
            print(f"  {link}")
        if len(broken_md_links) > 20:
            print(f"  ... and {len(broken_md_links) - 20} more")
