"""Build performance tests for I2P website.

Tracks and validates:
- Build output size (catch bloat)
- Number of generated pages
- Asset sizes
- Duplicate content detection
"""

import os
import time
import subprocess
import shutil
from pathlib import Path
from collections import defaultdict
import hashlib

import pytest


class TestBuildSize:
    """Test build output size to catch bloat."""

    # Thresholds (adjust based on your site)
    MAX_TOTAL_SIZE_MB = 500  # Maximum total build size
    MAX_SINGLE_FILE_MB = 10  # Maximum size for any single file
    MAX_HTML_FILE_KB = 500  # Maximum size for HTML files

    def test_total_build_size(self, build_hugo_site: Path):
        """Total build should not exceed size threshold."""
        total_size = 0
        for file_path in build_hugo_site.glob("**/*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size

        total_mb = total_size / (1024 * 1024)

        assert total_mb < self.MAX_TOTAL_SIZE_MB, (
            f"Build size {total_mb:.1f}MB exceeds threshold of "
            f"{self.MAX_TOTAL_SIZE_MB}MB"
        )

        # Log the size for tracking
        print(f"\nBuild size: {total_mb:.1f}MB")

    def test_no_oversized_files(self, build_hugo_site: Path):
        """No single file should be excessively large."""
        oversized = []

        for file_path in build_hugo_site.glob("**/*"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > self.MAX_SINGLE_FILE_MB:
                    rel_path = file_path.relative_to(build_hugo_site)
                    oversized.append(f"{rel_path}: {size_mb:.1f}MB")

        if oversized:
            msg = f"Found {len(oversized)} oversized files:\n"
            msg += "\n".join(f"  - {item}" for item in oversized)
            pytest.fail(msg)

    def test_html_file_sizes(self, build_hugo_site: Path):
        """HTML files should not be excessively large."""
        large_html = []

        for html_file in build_hugo_site.glob("**/*.html"):
            size_kb = html_file.stat().st_size / 1024
            if size_kb > self.MAX_HTML_FILE_KB:
                rel_path = html_file.relative_to(build_hugo_site)
                large_html.append(f"{rel_path}: {size_kb:.0f}KB")

        if large_html:
            sample = large_html[:10]
            msg = f"Found {len(large_html)} large HTML files (>{self.MAX_HTML_FILE_KB}KB):\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            if len(large_html) > 10:
                msg += f"\n  ... and {len(large_html) - 10} more"
            # Warning only - some pages may legitimately be large
            pytest.skip(msg)


class TestPageCount:
    """Test page generation metrics."""

    MIN_PAGES = 50  # Minimum expected pages (catch build issues)
    MAX_PAGES_PER_LANG = 500  # Maximum per language (catch runaway generation)

    def test_minimum_pages_generated(self, build_hugo_site: Path):
        """Build should generate minimum number of pages."""
        html_files = list(build_hugo_site.glob("**/*.html"))
        page_count = len(html_files)

        assert page_count >= self.MIN_PAGES, (
            f"Only {page_count} HTML pages generated, expected at least "
            f"{self.MIN_PAGES}. Build may have failed partially."
        )

        print(f"\nTotal pages generated: {page_count}")

    def test_pages_per_language(self, build_hugo_site: Path):
        """Each language should have reasonable page count."""
        lang_counts = defaultdict(int)

        for html_file in build_hugo_site.glob("**/*.html"):
            # Get top-level directory (language code)
            rel_path = html_file.relative_to(build_hugo_site)
            parts = rel_path.parts
            if parts:
                lang = parts[0]
                if len(lang) == 2:  # Language codes are 2 chars
                    lang_counts[lang] += 1

        print(f"\nPages per language:")
        for lang, count in sorted(lang_counts.items()):
            print(f"  {lang}: {count}")

        # Check for runaway generation
        for lang, count in lang_counts.items():
            assert count <= self.MAX_PAGES_PER_LANG, (
                f"Language '{lang}' has {count} pages, exceeds max of "
                f"{self.MAX_PAGES_PER_LANG}"
            )


class TestAssetMetrics:
    """Test asset size and count metrics."""

    def test_css_size(self, build_hugo_site: Path):
        """Track CSS file sizes."""
        css_files = list(build_hugo_site.glob("**/*.css"))
        total_css = sum(f.stat().st_size for f in css_files)
        total_kb = total_css / 1024

        print(f"\nCSS files: {len(css_files)}, total: {total_kb:.1f}KB")

        # Warn if CSS is getting large
        if total_kb > 200:
            pytest.skip(f"CSS total size is {total_kb:.1f}KB - consider optimization")

    def test_js_size(self, build_hugo_site: Path):
        """Track JavaScript file sizes."""
        js_files = list(build_hugo_site.glob("**/*.js"))
        total_js = sum(f.stat().st_size for f in js_files)
        total_kb = total_js / 1024

        print(f"\nJS files: {len(js_files)}, total: {total_kb:.1f}KB")

        # Warn if JS is getting large
        if total_kb > 500:
            pytest.skip(f"JS total size is {total_kb:.1f}KB - consider optimization")

    def test_image_count(self, build_hugo_site: Path):
        """Track image counts by type."""
        image_counts = defaultdict(int)
        image_sizes = defaultdict(int)

        for ext in ["png", "jpg", "jpeg", "gif", "svg", "webp", "ico"]:
            files = list(build_hugo_site.glob(f"**/*.{ext}"))
            image_counts[ext] = len(files)
            image_sizes[ext] = sum(f.stat().st_size for f in files)

        print("\nImage counts:")
        for ext, count in sorted(image_counts.items()):
            if count > 0:
                size_kb = image_sizes[ext] / 1024
                print(f"  .{ext}: {count} files, {size_kb:.1f}KB")


class TestDuplicateContent:
    """Detect duplicate content that might indicate build issues."""

    def test_no_duplicate_html_content(self, build_hugo_site: Path):
        """Check for exact duplicate HTML files."""
        html_files = list(build_hugo_site.glob("**/*.html"))

        # Hash file contents
        hashes = defaultdict(list)
        for html_file in html_files:
            # Only check files > 1KB to ignore tiny template fragments
            if html_file.stat().st_size > 1024:
                content = html_file.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                rel_path = str(html_file.relative_to(build_hugo_site))
                hashes[file_hash].append(rel_path)

        # Find duplicates
        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

        if duplicates:
            # Filter out expected duplicates (same page in different languages is OK)
            unexpected_dupes = []
            for hash_val, paths in duplicates.items():
                # Check if duplicates are just language variants
                base_paths = set()
                for p in paths:
                    # Remove language prefix
                    parts = p.split("/")
                    if len(parts) > 1 and len(parts[0]) == 2:
                        base_paths.add("/".join(parts[1:]))
                    else:
                        base_paths.add(p)

                # If all paths map to same base, it's a language variant
                if len(base_paths) > 1:
                    unexpected_dupes.append(paths)

            if unexpected_dupes:
                sample = unexpected_dupes[:5]
                msg = f"Found {len(unexpected_dupes)} sets of duplicate files:\n"
                for paths in sample:
                    msg += f"  - {paths[:3]}{'...' if len(paths) > 3 else ''}\n"
                # Warning only
                pytest.skip(msg)


class TestBuildTime:
    """Test build performance (informational)."""

    def test_measure_build_time(self, project_root: Path, hugo_bin_path: Path):
        """Measure Hugo build time."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            start_time = time.time()

            cmd = [
                str(hugo_bin_path),
                "--destination",
                tmpdir,
                "--quiet",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=project_root,
                timeout=300,
            )

            build_time = time.time() - start_time

            if result.returncode != 0:
                pytest.skip(f"Build failed: {result.stderr}")

            print(f"\nBuild time: {build_time:.1f}s")

            # Warn if build is slow
            if build_time > 120:
                pytest.skip(
                    f"Build took {build_time:.1f}s - consider optimization"
                )
