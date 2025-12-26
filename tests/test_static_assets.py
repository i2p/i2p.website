"""Test static asset validation.

Tests:
- Extract all image references from markdown and HTML
- Verify each referenced file exists in static/ directory
- Check for broken references with source file path
"""

import re
from pathlib import Path
from typing import Set, Tuple

import pytest
from bs4 import BeautifulSoup


def extract_image_references_markdown(content_dir: Path) -> Set[Tuple[str, Path]]:
    """Extract image references from markdown files."""
    references = set()

    md_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    html_img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>')

    for md_file in content_dir.glob("**/*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        for match in md_pattern.finditer(content):
            url = match.group(2)

            if url.startswith("/"):
                references.add((url, md_file))

        for match in html_img_pattern.finditer(content):
            url = match.group(1)

            if url.startswith("/"):
                references.add((url, md_file))

    return references


def extract_image_references_html(build_dir: Path) -> Set[Tuple[str, Path]]:
    """Extract image references from HTML files."""
    references = set()

    for html_file in build_dir.glob("**/*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        for img in soup.find_all("img", src=True):
            src = img["src"]

            if src.startswith("/"):
                references.add((src, html_file))

    return references


def get_static_files(static_dir: Path) -> Set[str]:
    """Get all files in static directory."""
    files = set()

    for file_path in static_dir.glob("**/*"):
        if file_path.is_file():
            relative = file_path.relative_to(static_dir)
            files.add(f"/{relative}")

    return files


def test_static_directory_exists(static_dir: Path) -> None:
    """Test that static directory exists."""
    assert static_dir.exists(), "Static directory not found"
    assert static_dir.is_dir(), "Static path is not a directory"


def test_static_has_images(static_dir: Path) -> None:
    """Test that static directory contains image files."""
    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"]

    image_files = [
        f
        for f in static_dir.glob("**/*")
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    assert len(image_files) > 0, "No image files found in static directory"
    print(f"\n✅ Found {len(image_files)} image files in static/")


def test_markdown_image_references(content_dir: Path, static_dir: Path) -> None:
    """Test that all markdown image references exist in static directory."""
    references = extract_image_references_markdown(content_dir)
    static_files = get_static_files(static_dir)

    if not references:
        pytest.skip("No image references found in markdown files")

    broken_references = {}

    for url, source_file in references:
        if url not in static_files:
            # Remove query parameters and anchors
            url_base = url.split("?")[0].split("#")[0]

            if url_base not in static_files:
                relative_path = source_file.relative_to(content_dir)

                if relative_path not in broken_references:
                    broken_references[relative_path] = []
                broken_references[relative_path].append(url)

    if broken_references:
        print(
            f"\n❌ Found {sum(len(refs) for refs in broken_references.values())} broken image references in markdown:"
        )
        for file_path, urls in sorted(broken_references.items()):
            print(f"\n  {file_path}:")
            for url in sorted(urls)[:5]:
                print(f"    - {url}")
            if len(urls) > 5:
                print(f"    ... and {len(urls) - 5} more")

        pytest.fail(
            f"Found broken image references in {len(broken_references)} markdown files"
        )


def test_html_image_references(build_hugo_site: Path, static_dir: Path) -> None:
    """Test that all HTML image references exist in static or build directory."""
    references = extract_image_references_html(build_hugo_site)

    if not references:
        pytest.skip("No image references found in HTML files")

    # Get files from both static directory and build output
    static_files = get_static_files(static_dir)
    build_files = set()

    for file_path in build_hugo_site.glob("**/*"):
        if file_path.is_file():
            relative = file_path.relative_to(build_hugo_site)
            build_files.add(f"/{relative}")

    all_files = static_files | build_files

    broken_references = {}

    for url, source_file in references:
        url_base = url.split("?")[0].split("#")[0]

        if url_base not in all_files:
            relative_path = source_file.relative_to(build_hugo_site)

            if relative_path not in broken_references:
                broken_references[relative_path] = []
            broken_references[relative_path].append(url)

    if broken_references:
        print(
            f"\n❌ Found {sum(len(refs) for refs in broken_references.values())} broken image references in HTML:"
        )
        for file_path, urls in sorted(broken_references.items()):
            print(f"\n  {file_path}:")
            for url in sorted(urls)[:5]:
                print(f"    - {url}")
            if len(urls) > 5:
                print(f"    ... and {len(urls) - 5} more")

        pytest.fail(
            f"Found broken image references in {len(broken_references)} HTML files"
        )


def test_common_static_files_exist(static_dir: Path) -> None:
    """Test that common static files exist."""
    expected_files = []

    favicon_paths = [
        static_dir / "favicon.ico",
        static_dir / "favicon.png",
        static_dir / "images" / "favicon.ico",
        static_dir / "images" / "favicon.png",
    ]

    if not any(p.exists() for p in favicon_paths):
        expected_files.append("favicon.ico or favicon.png")

    if not (static_dir / "robots.txt").exists():
        expected_files.append("robots.txt (optional)")

    if expected_files:
        print(f"\n⚠️  Missing optional static files: {', '.join(expected_files)}")


def test_static_files_no_empty_dirs(static_dir: Path) -> None:
    """Test for empty directories in static folder."""
    empty_dirs = []

    for dir_path in static_dir.rglob("*"):
        if dir_path.is_dir():
            subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
            files = [f for f in dir_path.iterdir() if f.is_file()]

            if not subdirs and not files:
                relative = dir_path.relative_to(static_dir)
                empty_dirs.append(relative)

    if empty_dirs:
        print(f"\n⚠️  Found {len(empty_dirs)} empty directories:")
        for dir_path in empty_dirs[:10]:
            print(f"    {dir_path}")
        if len(empty_dirs) > 10:
            print(f"    ... and {len(empty_dirs) - 10} more")


def test_static_file_sizes_reasonable(static_dir: Path) -> None:
    """Test that static files have reasonable sizes."""
    suspicious_files = []

    for file_path in static_dir.glob("**/*"):
        if file_path.is_file():
            size = file_path.stat().st_size

            if size == 0:
                suspicious_files.append((file_path, "empty"))
            elif (
                file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]
                and size > 10000000
            ):
                suspicious_files.append((file_path, f"very large ({size:,} bytes)"))

    if suspicious_files:
        print(f"\n⚠️  Found {len(suspicious_files)} suspicious files:")
        for file_path, reason in suspicious_files[:20]:
            print(f"    - {file_path.relative_to(static_dir)}: {reason}")
        if len(suspicious_files) > 20:
            print(f"    ... and {len(suspicious_files) - 20} more")


def test_static_image_formats(static_dir: Path) -> None:
    """Test that static images use web-friendly formats."""
    image_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".webp",
        ".ico",
        ".bmp",
        ".tiff",
    ]

    format_counts = {ext: 0 for ext in image_extensions}

    for file_path in static_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            ext = file_path.suffix.lower()
            format_counts[ext] += 1

    total_images = sum(format_counts.values())

    if total_images > 0:
        print(f"\n📊 Static image formats ({total_images} total):")
        for ext, count in sorted(format_counts.items()):
            if count > 0:
                print(f"    {ext}: {count} ({count / total_images * 100:.1f}%)")


def test_static_svg_files_valid(static_dir: Path) -> None:
    """Test that SVG files are valid XML."""
    svg_files = list(static_dir.glob("**/*.svg"))

    if not svg_files:
        pytest.skip("No SVG files found")

    invalid_svgs = []

    for svg_file in svg_files[:20]:
        try:
            with open(svg_file, "r", encoding="utf-8") as f:
                content = f.read()

            if "<svg" not in content or "</svg>" not in content:
                invalid_svgs.append((svg_file, "Missing <svg> tags"))
        except Exception as e:
            invalid_svgs.append((svg_file, str(e)))

    if invalid_svgs:
        print(f"\n❌ Found {len(invalid_svgs)} invalid SVG files:")
        for svg_file, reason in invalid_svgs:
            print(f"    - {svg_file.relative_to(static_dir)}: {reason}")

        pytest.fail("Found invalid SVG files")


def test_static_duplicates_by_name(static_dir: Path) -> None:
    """Test for duplicate filenames in static directory."""
    name_counts = {}

    for file_path in static_dir.glob("**/*"):
        if file_path.is_file():
            name = file_path.name
            name_counts[name] = name_counts.get(name, 0) + 1

    duplicates = {name: count for name, count in name_counts.items() if count > 1}

    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate filenames:")
        for name, count in sorted(duplicates.items())[:10]:
            print(f"    - {name}: {count} occurrences")
        if len(duplicates) > 10:
            print(f"    ... and {len(duplicates) - 10} more")


def test_static_file_paths_no_spaces(static_dir: Path) -> None:
    """Test that static file paths don't contain spaces."""
    files_with_spaces = []

    for file_path in static_dir.glob("**/*"):
        if file_path.is_file():
            if " " in str(file_path.relative_to(static_dir)):
                files_with_spaces.append(file_path.relative_to(static_dir))

    if files_with_spaces:
        print(f"\n⚠️  Found {len(files_with_spaces)} files with spaces in path:")
        for file_path in files_with_spaces[:10]:
            print(f"    - {file_path}")
        if len(files_with_spaces) > 10:
            print(f"    ... and {len(files_with_spaces) - 10} more")


def test_static_css_files_exist(static_dir: Path) -> None:
    """Test that CSS files exist in static directory."""
    css_files = list(static_dir.glob("**/*.css"))

    if css_files:
        print(f"\n✅ Found {len(css_files)} CSS files in static/")
    else:
        print(f"\n⚠️  No CSS files found in static/ (may be in assets/)")


def test_static_js_files_exist(static_dir: Path) -> None:
    """Test that JS files exist in static directory."""
    js_files = list(static_dir.glob("**/*.js"))

    if js_files:
        print(f"\n✅ Found {len(js_files)} JavaScript files in static/")
    else:
        print(f"\n⚠️  No JavaScript files found in static/ (may be in assets/)")
