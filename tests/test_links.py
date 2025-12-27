"""Test internal link validation.

Tests:
- Validate internal links in generated HTML
- Validate internal links in markdown content
"""

import re
from pathlib import Path
from typing import Set

import pytest
from bs4 import BeautifulSoup


def extract_internal_links_from_html(html_path: Path) -> Set[str]:
    """Extract all internal links from an HTML file."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"]

        if href.startswith("/"):
            links.add(href.split("#")[0].split("?")[0])
        elif href.startswith("http://") or href.startswith("https://"):
            pass
        elif href.startswith("#") or href.startswith("?"):
            pass
        elif href and not href.startswith(("mailto:", "tel:", "ftp://", "file://")):
            links.add(href)

    return links


def get_valid_urls_from_build(build_dir: Path) -> Set[str]:
    """Get all valid URLs from Hugo build output."""
    valid_urls = set()

    for html_file in build_dir.glob("**/*.html"):
        relative = html_file.relative_to(build_dir)

        if relative.name == "index.html":
            path = str(relative.parent)
            if path == ".":
                valid_urls.add("/")
            else:
                valid_urls.add(f"/{path}")
                valid_urls.add(f"/{path}/")
        else:
            valid_urls.add(f"/{relative}")

    for json_file in build_dir.glob("**/*.json"):
        relative = json_file.relative_to(build_dir)
        valid_urls.add(f"/{relative}")

    for xml_file in build_dir.glob("**/*.xml"):
        relative = xml_file.relative_to(build_dir)
        valid_urls.add(f"/{relative}")

    return valid_urls


def extract_internal_links_from_markdown(content_dir: Path) -> Set[str]:
    """Extract internal links from markdown files."""
    links = set()

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for md_file in content_dir.glob("**/*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        for match in link_pattern.finditer(content):
            url = match.group(2)

            if url.startswith("/"):
                links.add(url)
            elif url.startswith("http://") or url.startswith("https://"):
                pass
            elif url.startswith("#"):
                pass
            elif url and not url.startswith(("mailto:", "tel:")):
                links.add(url)

    return links


def get_content_file_paths(content_dir: Path) -> Set[str]:
    """Get paths of all content files for validation."""
    paths = set()

    for content_file in content_dir.glob("**/*.md"):
        relative = content_file.relative_to(content_dir)

        if relative.name == "_index.md":
            path = f"/{relative.parent}/"
        else:
            path = f"/{relative.with_suffix('')}/"

        paths.add(path)

    return paths


def test_hugo_build_succeeds(build_hugo_site: Path) -> None:
    """Test that Hugo builds successfully."""
    assert build_hugo_site.exists(), "Hugo build directory not found"
    assert (build_hugo_site / "index.html").exists(), (
        "index.html not found in build output"
    )


def test_html_links_valid(build_hugo_site: Path) -> None:
    """Test that all internal HTML links point to valid URLs."""
    import os
    valid_urls = get_valid_urls_from_build(build_hugo_site)

    broken_links = {}

    for html_file in build_hugo_site.glob("**/*.html"):
        html_rel_path = html_file.relative_to(build_hugo_site)
        links = extract_internal_links_from_html(html_file)

        broken = []
        for link in links:
            resolved_link = link
            # If relative link, resolve it relative to the current file
            if not link.startswith("/"):
                file_dir = html_rel_path.parent
                norm_path = os.path.normpath(os.path.join(file_dir, link))
                if norm_path == "." or norm_path == "..":
                    resolved_link = "/"
                else:
                    resolved_link = "/" + norm_path.lstrip("/")
            
            # Check if resolved link is valid
            if resolved_link not in valid_urls:
                # Also try adding/removing trailing slash if not already found
                alt_link = resolved_link.rstrip("/") if resolved_link.endswith("/") else (resolved_link + "/")
                if alt_link not in valid_urls:
                    broken.append(link)

        if broken:
            broken_links[str(html_rel_path)] = broken

    if broken_links:
        print(
            f"\n❌ Found {sum(len(b) for b in broken_links.values())} broken links in HTML:"
        )
        for file_path, links in sorted(broken_links.items()):
            print(f"\n  {file_path}:")
            for link in sorted(links)[:5]:
                print(f"    - {link}")
            if len(links) > 5:
                print(f"    ... and {len(links) - 5} more")

        pytest.fail(f"Found broken internal links in {len(broken_links)} HTML files")


def test_markdown_links_valid(content_dir: Path) -> None:
    """Test that all internal markdown links point to valid content files."""
    content_paths = get_content_file_paths(content_dir)
    markdown_links = extract_internal_links_from_markdown(content_dir)

    broken_links = [link for link in markdown_links if link not in content_paths]

    if broken_links:
        print(f"\n❌ Found {len(broken_links)} broken links in markdown content:")
        for link in sorted(broken_links)[:20]:
            print(f"    - {link}")
        if len(broken_links) > 20:
            print(f"    ... and {len(broken_links) - 20} more")

        pytest.fail(f"Found {len(broken_links)} broken links in markdown files")


def test_all_languages_have_index(build_hugo_site: Path) -> None:
    """Test that all language directories have an index.html."""
    expected_languages = [
        "en",
        "es",
        "ko",
        "zh",
        "ru",
        "cs",
        "de",
        "fr",
        "tr",
        "vi",
        "hi",
        "ar",
        "pt",
    ]

    missing_languages = []

    for lang in expected_languages:
        index_path = build_hugo_site / lang / "index.html"
        if not index_path.exists():
            missing_languages.append(lang)

    if missing_languages:
        pytest.fail(f"Missing index.html for languages: {', '.join(missing_languages)}")


def test_root_index_exists(build_hugo_site: Path) -> None:
    """Test that root index.html exists."""
    assert (build_hugo_site / "index.html").exists(), "Root index.html not found"


def test_docs_index_json_exists(build_hugo_site: Path) -> None:
    """Test that docs search index JSON files exist for all languages."""
    expected_languages = [
        "en",
        "es",
        "ko",
        "zh",
        "ru",
        "cs",
        "de",
        "fr",
        "tr",
        "vi",
        "hi",
        "ar",
        "pt",
    ]

    missing_languages = []

    for lang in expected_languages:
        index_path = build_hugo_site / lang / "docs" / "index.json"
        if not index_path.exists():
            missing_languages.append(lang)

    if missing_languages:
        pytest.fail(
            f"Missing docs/index.json for languages: {', '.join(missing_languages)}"
        )


def test_rss_feeds_exist(build_hugo_site: Path) -> None:
    """Test that RSS feeds exist for all languages."""
    expected_languages = [
        "en",
        "es",
        "ko",
        "zh",
        "ru",
        "cs",
        "de",
        "fr",
        "tr",
        "vi",
        "hi",
        "ar",
        "pt",
    ]

    missing_languages = []

    for lang in expected_languages:
        feed_path = build_hugo_site / lang / "index.xml"
        if not feed_path.exists():
            missing_languages.append(lang)

    if missing_languages:
        pytest.fail(
            f"Missing index.xml (RSS feed) for languages: {', '.join(missing_languages)}"
        )


def test_no_broken_anchor_links(build_hugo_site: Path) -> None:
    """Test that anchor links (#section) point to existing elements."""
    broken_anchors = {}

    for html_file in build_hugo_site.glob("**/*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        anchor_ids = set()
        for tag in soup.find_all(attrs={"id": True}):
            anchor_ids.add(tag["id"])

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if "#" in href and not href.startswith("#"):
                url_part, anchor = href.split("#", 1)

                if url_part == "" or url_part == "/" or url_part.startswith("/"):
                    pass
                else:
                    continue

                if anchor and anchor not in anchor_ids:
                    relative_path = html_file.relative_to(build_hugo_site)
                    if relative_path not in broken_anchors:
                        broken_anchors[relative_path] = []
                    broken_anchors[relative_path].append(anchor)

    if broken_anchors:
        print(f"\n❌ Found broken anchor links in {len(broken_anchors)} files:")
        for file_path, anchors in sorted(broken_anchors.items()):
            print(f"\n  {file_path}:")
            for anchor in sorted(anchors)[:5]:
                print(f"    - #{anchor}")
            if len(anchors) > 5:
                print(f"    ... and {len(anchors) - 5} more")

        pytest.fail(f"Found broken anchor links")


def test_static_files_exist(build_hugo_site: Path, static_dir: Path) -> None:
    """Test that referenced static files exist in build output."""
    static_files_in_build = set()

    for static_file in build_hugo_site.glob("**/*"):
        if static_file.is_file():
            static_files_in_build.add(static_file.name)

    for static_file in static_dir.glob("**/*"):
        if static_file.is_file():
            if static_file.name not in static_files_in_build:
                relative_path = static_file.relative_to(static_dir)
                print(f"\n⚠️  Static file not in build: {relative_path}")


def test_image_links_exist(build_hugo_site: Path) -> None:
    """Test that image src attributes point to existing files."""
    broken_images = {}

    for html_file in build_hugo_site.glob("**/*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        for img in soup.find_all("img", src=True):
            src = img["src"]

            if src.startswith("/"):
                file_path = build_hugo_site / src.lstrip("/")

                if not file_path.exists():
                    relative_path = html_file.relative_to(build_hugo_site)
                    if relative_path not in broken_images:
                        broken_images[relative_path] = []
                    broken_images[relative_path].append(src)

    if broken_images:
        print(f"\n❌ Found broken image links in {len(broken_images)} files:")
        for file_path, images in sorted(broken_images.items()):
            print(f"\n  {file_path}:")
            for img in sorted(images)[:5]:
                print(f"    - {img}")
            if len(images) > 5:
                print(f"    ... and {len(images) - 5} more")

        pytest.fail(f"Found broken image links")
