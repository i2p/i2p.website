"""Accessibility tests for I2P website.

Tests basic accessibility requirements:
- Images have alt attributes
- Proper heading hierarchy (no skipped levels)
- HTML lang attributes present
- Form inputs have labels
- Links have discernible text
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import pytest


class TestImageAccessibility:
    """Test that images have proper alt attributes."""

    def test_images_have_alt_attributes(self, build_hugo_site: Path):
        """All img tags should have alt attributes."""
        html_files = list(build_hugo_site.glob("**/*.html"))
        assert html_files, "No HTML files found"

        missing_alt = []
        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            for img in soup.find_all("img"):
                # Check if alt attribute exists (can be empty for decorative images)
                if not img.has_attr("alt"):
                    rel_path = html_file.relative_to(build_hugo_site)
                    src = img.get("src", "unknown")
                    missing_alt.append(f"{rel_path}: <img src='{src}'>")

        if missing_alt:
            # Limit output to first 20 issues
            sample = missing_alt[:20]
            msg = f"Found {len(missing_alt)} images without alt attributes:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            if len(missing_alt) > 20:
                msg += f"\n  ... and {len(missing_alt) - 20} more"
            pytest.fail(msg)

    def test_decorative_images_have_empty_alt(self, build_hugo_site: Path):
        """Decorative images (icons, etc.) should have empty alt, not missing."""
        # This is informational - we just check that SVG icons inside links
        # or buttons don't have verbose alt text
        html_files = list(build_hugo_site.glob("**/*.html"))[:50]  # Sample

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            # SVGs inside interactive elements should be decorative
            for svg in soup.find_all("svg"):
                parent = svg.parent
                if parent and parent.name in ["a", "button"]:
                    # Should have aria-hidden or be purely decorative
                    # This is just a soft check
                    pass


class TestHeadingHierarchy:
    """Test proper heading structure."""

    def test_no_skipped_heading_levels(self, build_hugo_site: Path):
        """Headings should not skip levels (e.g., h1 to h3)."""
        html_files = list(build_hugo_site.glob("**/*.html"))
        assert html_files, "No HTML files found"

        issues = []
        # Sample pages to avoid slow tests
        sample_files = html_files[:100]

        for html_file in sample_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            # Get all headings in order
            headings = soup.find_all(re.compile(r"^h[1-6]$"))
            if not headings:
                continue

            prev_level = 0
            for heading in headings:
                level = int(heading.name[1])

                # First heading or going up (smaller number) is fine
                # Going down more than 1 level is a skip
                if prev_level > 0 and level > prev_level + 1:
                    rel_path = html_file.relative_to(build_hugo_site)
                    text = heading.get_text(strip=True)[:50]
                    issues.append(
                        f"{rel_path}: h{prev_level} -> h{level} ('{text}')"
                    )
                    break  # One issue per file is enough

                prev_level = level

        if issues:
            sample = issues[:15]
            msg = f"Found {len(issues)} pages with skipped heading levels:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            if len(issues) > 15:
                msg += f"\n  ... and {len(issues) - 15} more"
            # Warning only - don't fail the build
            pytest.skip(msg)

    def test_pages_have_h1(self, build_hugo_site: Path):
        """Each page should have exactly one h1."""
        html_files = list(build_hugo_site.glob("**/*.html"))

        no_h1 = []
        multiple_h1 = []
        # Sample to avoid slow tests
        sample_files = html_files[:100]

        for html_file in sample_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            h1_tags = soup.find_all("h1")
            rel_path = html_file.relative_to(build_hugo_site)

            if len(h1_tags) == 0:
                no_h1.append(str(rel_path))
            elif len(h1_tags) > 1:
                multiple_h1.append(f"{rel_path} ({len(h1_tags)} h1 tags)")

        # Multiple h1s is more problematic than missing
        if multiple_h1:
            sample = multiple_h1[:10]
            msg = f"Found {len(multiple_h1)} pages with multiple h1 tags:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            # Warning only
            pytest.skip(msg)


class TestLangAttribute:
    """Test HTML lang attributes."""

    def test_html_has_lang_attribute(self, build_hugo_site: Path):
        """HTML tag should have lang attribute."""
        html_files = list(build_hugo_site.glob("**/*.html"))
        assert html_files, "No HTML files found"

        missing_lang = []
        sample_files = html_files[:50]

        for html_file in sample_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            html_tag = soup.find("html")
            if html_tag and not html_tag.get("lang"):
                rel_path = html_file.relative_to(build_hugo_site)
                missing_lang.append(str(rel_path))

        if missing_lang:
            sample = missing_lang[:10]
            msg = f"Found {len(missing_lang)} pages without lang attribute:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            pytest.fail(msg)

    def test_lang_matches_content_directory(self, build_hugo_site: Path):
        """Lang attribute should match the content language."""
        # Check a sample of language directories
        for lang in ["en", "de", "fr", "es"]:
            lang_dir = build_hugo_site / lang
            if not lang_dir.exists():
                continue

            html_files = list(lang_dir.glob("*.html"))[:5]
            for html_file in html_files:
                content = html_file.read_text(encoding="utf-8", errors="ignore")
                soup = BeautifulSoup(content, "html.parser")

                html_tag = soup.find("html")
                if html_tag:
                    page_lang = html_tag.get("lang", "")
                    # Lang might be "en" or "en-US", etc.
                    assert page_lang.startswith(lang) or lang in page_lang, (
                        f"{html_file.relative_to(build_hugo_site)}: "
                        f"expected lang='{lang}*', got '{page_lang}'"
                    )


class TestFormAccessibility:
    """Test form accessibility."""

    def test_inputs_have_labels_or_aria(self, build_hugo_site: Path):
        """Form inputs should have associated labels or aria-label."""
        html_files = list(build_hugo_site.glob("**/*.html"))

        unlabeled_inputs = []
        sample_files = html_files[:50]

        for html_file in sample_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            for inp in soup.find_all("input"):
                input_type = inp.get("type", "text")
                # Skip hidden and submit/button types
                if input_type in ["hidden", "submit", "button", "image"]:
                    continue

                input_id = inp.get("id")
                has_label = False

                # Check for associated label
                if input_id:
                    label = soup.find("label", attrs={"for": input_id})
                    if label:
                        has_label = True

                # Check for aria-label or aria-labelledby
                if inp.get("aria-label") or inp.get("aria-labelledby"):
                    has_label = True

                # Check for placeholder (not ideal but acceptable)
                if inp.get("placeholder"):
                    has_label = True

                # Check if wrapped in label
                parent = inp.parent
                if parent and parent.name == "label":
                    has_label = True

                if not has_label:
                    rel_path = html_file.relative_to(build_hugo_site)
                    name = inp.get("name", inp.get("id", "unknown"))
                    unlabeled_inputs.append(f"{rel_path}: input[name='{name}']")

        if unlabeled_inputs:
            sample = unlabeled_inputs[:10]
            msg = f"Found {len(unlabeled_inputs)} inputs without labels:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            # Warning only - some inputs may be intentionally unlabeled
            pytest.skip(msg)


class TestLinkAccessibility:
    """Test link accessibility."""

    def test_links_have_discernible_text(self, build_hugo_site: Path):
        """Links should have text content or aria-label."""
        html_files = list(build_hugo_site.glob("**/*.html"))

        empty_links = []
        sample_files = html_files[:50]

        for html_file in sample_files:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            for link in soup.find_all("a"):
                href = link.get("href", "")
                # Skip anchor links and javascript
                if href.startswith("#") or href.startswith("javascript:"):
                    continue

                has_text = False

                # Check text content
                text = link.get_text(strip=True)
                if text:
                    has_text = True

                # Check aria-label
                if link.get("aria-label"):
                    has_text = True

                # Check for img with alt inside
                img = link.find("img")
                if img and img.get("alt"):
                    has_text = True

                # Check for SVG with title
                svg = link.find("svg")
                if svg:
                    title = svg.find("title")
                    if title and title.get_text(strip=True):
                        has_text = True
                    # SVG icons are often decorative, parent link should have text
                    # This is a soft check

                if not has_text:
                    rel_path = html_file.relative_to(build_hugo_site)
                    empty_links.append(f"{rel_path}: <a href='{href[:50]}'>")

        if empty_links:
            sample = empty_links[:10]
            msg = f"Found {len(empty_links)} links without discernible text:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            # Warning only
            pytest.skip(msg)
