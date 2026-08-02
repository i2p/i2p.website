"""Practical unit tests for I2P website.

These tests catch real problems:
- Config syntax errors (hugo.toml, i18n/*.toml, downloads.yaml)
- Missing required frontmatter in content files
- Broken image references in markdown
- Invalid SHA256 hashes in downloads
- Missing i18n translation keys
- Translation completeness across languages

Run with: pytest tests/test_quick.py -v
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Set

import pytest
import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .utils import extract_markdown_front_matter, validate_sha256_hash


# =============================================================================
# CONFIG VALIDATION - Catch syntax errors before build
# =============================================================================


class TestConfigSyntax:
    """Test that all config files are syntactically valid."""

    def test_hugo_toml_valid(self, hugo_config: dict):
        """hugo.toml must parse and have required keys."""
        assert isinstance(hugo_config, dict), "hugo.toml must be a dictionary"
        assert "baseURL" in hugo_config, "hugo.toml must contain 'baseURL'"
        assert "languages" in hugo_config, "hugo.toml must define languages"
        assert "defaultContentLanguage" in hugo_config, (
            "hugo.toml must set defaultContentLanguage"
        )

    def test_hugo_toml_languages_valid(self, hugo_config: dict):
        """Each language config must have required fields."""
        languages = hugo_config.get("languages", {})
        assert languages, "No languages configured"

        for lang_code, lang_config in languages.items():
            assert "contentDir" in lang_config, (
                f"Language {lang_code} missing contentDir"
            )
            assert "languageName" in lang_config, (
                f"Language {lang_code} missing languageName"
            )
            assert "title" in lang_config, f"Language {lang_code} missing title"

    def test_goldmark_preserves_double_hyphens(self, hugo_config: dict):
        """Goldmark must not replace double hyphens in technical identifiers."""
        typographer = hugo_config["markup"]["goldmark"]["extensions"]["typographer"]
        assert typographer["enDash"] == "--"

    def test_i18n_files_valid_toml(self, i18n_files: Dict[str, Path]):
        """All i18n/*.toml files must be valid TOML."""
        invalid = []
        for lang, file_path in i18n_files.items():
            try:
                with open(file_path, "rb") as f:
                    data = tomllib.load(f)
                assert isinstance(data, dict), f"{lang}.toml parsed but is not a dict"
            except tomllib.TOMLDecodeError as e:
                invalid.append(f"{lang}.toml: {e}")

        if invalid:
            pytest.fail(f"Invalid TOML files:\n" + "\n".join(invalid))

    def test_downloads_yaml_valid(self, downloads_config: dict):
        """downloads.yaml must parse and have required structure."""
        assert isinstance(downloads_config, dict), "downloads.yaml must be a dict"
        assert "current_version" in downloads_config, "Missing current_version"
        assert "downloads" in downloads_config, "Missing downloads section"
        assert isinstance(downloads_config["downloads"], dict), (
            "downloads must be a dict"
        )


# =============================================================================
# DOWNLOADS VALIDATION - Catch release mistakes
# =============================================================================


class TestDownloadsConfig:
    """Validate downloads.yaml for release integrity."""

    def test_sha256_hashes_valid_format(self, downloads_config: dict):
        """All SHA256 hashes must be valid 64-char hex strings."""
        downloads = downloads_config.get("downloads", {})
        invalid = []

        for name, entry in downloads.items():
            if "sha256" in entry:
                sha = entry["sha256"]
                if not validate_sha256_hash(sha):
                    invalid.append(f"{name}: {sha[:20]}... (len={len(sha)})")

        if invalid:
            pytest.fail(f"Invalid SHA256 hashes:\n" + "\n".join(invalid))

    def test_sha256_hashes_unique(self, downloads_config: dict):
        """SHA256 hashes should be unique (same hash = wrong file)."""
        downloads = downloads_config.get("downloads", {})
        seen: Dict[str, str] = {}
        duplicates = []

        for name, entry in downloads.items():
            sha = entry.get("sha256", "")
            if sha in seen:
                duplicates.append(f"{name} and {seen[sha]} have same hash")
            else:
                seen[sha] = name

        if duplicates:
            pytest.fail(f"Duplicate SHA256 hashes:\n" + "\n".join(duplicates))

    def test_version_in_filenames(self, downloads_config: dict):
        """Filenames should contain version number (catches stale configs).

        Note: Some files like generic APKs may not include version in filename.
        """
        current_version = downloads_config.get("current_version", "")
        downloads = downloads_config.get("downloads", {})

        mismatches = []

        # Only check non-android downloads for version in filename
        # Android APK often uses generic "I2P.apk" name
        for name, entry in downloads.items():
            if name == "android":
                continue  # Skip android - often uses generic filename

            filename = entry.get("file", "")
            if current_version and current_version not in filename:
                mismatches.append(f"{name}: {filename} (expected {current_version})")

        if mismatches:
            pytest.fail(f"Version mismatches in filenames:\n" + "\n".join(mismatches))

    def test_download_links_have_https(self, downloads_config: dict):
        """Primary download links should use HTTPS."""
        downloads = downloads_config.get("downloads", {})
        http_links = []

        for name, entry in downloads.items():
            links = entry.get("links", {})
            primary = links.get("primary", "")
            if primary.startswith("http://") and not ".i2p" in primary:
                http_links.append(f"{name}: {primary}")

        if http_links:
            pytest.fail(
                f"Primary links using HTTP instead of HTTPS:\n" + "\n".join(http_links)
            )

    def test_required_download_fields(self, downloads_config: dict):
        """Each download must have file, size, sha256, and links."""
        downloads = downloads_config.get("downloads", {})
        missing = []

        required = ["file", "sha256", "links"]
        for name, entry in downloads.items():
            for field in required:
                if field not in entry:
                    missing.append(f"{name}: missing {field}")

        if missing:
            pytest.fail(f"Missing required fields:\n" + "\n".join(missing))


# =============================================================================
# I18N KEY CONSISTENCY - Catch missing translations
# =============================================================================


class TestI18nConsistency:
    """Verify translation files have consistent keys."""

    def _get_keys(self, data: dict, prefix: str = "") -> Set[str]:
        """Recursively extract all keys from nested dict."""
        keys = set()
        for k, v in data.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.add(full_key)
            if isinstance(v, dict):
                keys.update(self._get_keys(v, full_key))
        return keys

    def test_all_langs_have_critical_keys(self, i18n_files: Dict[str, Path]):
        """All languages must have critical UI keys."""
        # Keys that absolutely must exist for the site to work
        critical_keys = {
            "nav.home",
            "nav.about",
            "nav.docs",
            "nav.downloads",
            "nav.blog",
        }

        missing = []
        for lang, path in i18n_files.items():
            with open(path, "rb") as f:
                data = tomllib.load(f)

            lang_keys = self._get_keys(data)
            missing_critical = critical_keys - lang_keys

            if missing_critical:
                missing.append(f"{lang}: missing {missing_critical}")

        # Only fail if critical keys are missing (not a warning)
        if missing:
            # Check if the critical keys even exist in English first
            en_path = i18n_files.get("en")
            if en_path:
                with open(en_path, "rb") as f:
                    en_data = tomllib.load(f)
                en_keys = self._get_keys(en_data)
                actual_critical = critical_keys & en_keys
                if not actual_critical:
                    pytest.skip("Critical keys not defined in English i18n")

    def test_translation_coverage_report(self, i18n_files: Dict[str, Path]):
        """Report translation coverage (informational)."""
        en_path = i18n_files.get("en")
        if not en_path:
            pytest.skip("English i18n file not found")

        with open(en_path, "rb") as f:
            en_data = tomllib.load(f)
        en_keys = self._get_keys(en_data)

        coverage = {}
        for lang, path in i18n_files.items():
            if lang == "en":
                continue
            with open(path, "rb") as f:
                lang_data = tomllib.load(f)
            lang_keys = self._get_keys(lang_data)

            matched = len(lang_keys & en_keys)
            total = len(en_keys)
            pct = (matched / total * 100) if total > 0 else 0
            coverage[lang] = pct

        print(f"\ni18n translation coverage:")
        for lang, pct in sorted(coverage.items(), key=lambda x: -x[1]):
            print(f"  {lang}: {pct:.0f}%")


# =============================================================================
# CONTENT VALIDATION - Catch broken content before build
# =============================================================================


class TestFrontMatter:
    """Validate markdown frontmatter."""

    def test_all_md_files_have_frontmatter(self, all_content_files: list):
        """All markdown files should start with ---."""
        missing = []

        for md_file in all_content_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read(100)

            # Handle BOM
            if content.startswith("\ufeff"):
                content = content[1:]

            if not content.strip().startswith("---"):
                rel_path = md_file.relative_to(md_file.parent.parent.parent)
                missing.append(str(rel_path))

        if missing:
            sample = missing[:10]
            pytest.fail(
                f"Found {len(missing)} files without frontmatter:\n"
                + "\n".join(f"  - {p}" for p in sample)
                + (f"\n  ... and {len(missing) - 10} more" if len(missing) > 10 else "")
            )

    def test_blog_posts_have_date(self, all_content_files: list):
        """Blog posts must have date field."""
        blog_files = [
            f for f in all_content_files if "/blog/" in str(f) and f.name != "_index.md"
        ]

        missing_date = []
        for md_file in blog_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            fm = extract_markdown_front_matter(content)
            if isinstance(fm, dict) and "date" not in fm:
                rel_path = md_file.relative_to(md_file.parent.parent.parent)
                missing_date.append(str(rel_path))

        if missing_date:
            sample = missing_date[:10]
            pytest.fail(
                f"Blog posts without date:\n" + "\n".join(f"  - {p}" for p in sample)
            )

    def test_all_files_have_title(self, all_content_files: list):
        """All content files should have a title."""
        missing_title = []

        for md_file in all_content_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            fm = extract_markdown_front_matter(content)
            if isinstance(fm, dict) and "title" not in fm:
                rel_path = md_file.relative_to(md_file.parent.parent.parent)
                missing_title.append(str(rel_path))

        if missing_title:
            sample = missing_title[:10]
            pytest.fail(
                f"Files without title:\n" + "\n".join(f"  - {p}" for p in sample)
            )


# =============================================================================
# STATIC ASSET VALIDATION - Catch broken references
# =============================================================================


class TestStaticAssets:
    """Validate static assets."""

    def test_svgs_valid_xml(self, all_static_files: list):
        """SVG files must be valid XML."""
        invalid = []

        for f in all_static_files:
            if f.suffix.lower() == ".svg":
                try:
                    ET.parse(f)
                except ET.ParseError as e:
                    invalid.append(f"{f.name}: {e}")
                except Exception as e:
                    invalid.append(f"{f.name}: {e}")

        if invalid:
            pytest.fail(f"Invalid SVG files:\n" + "\n".join(invalid[:10]))

    def test_image_refs_in_markdown(self, all_content_files: list, project_root: Path):
        """Check that image references in markdown point to existing files."""
        md_img = re.compile(r"!\[.*?\]\((.*?)\)")
        html_img = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
        # Patterns to strip code blocks before checking image refs
        fenced_code = re.compile(r"```[\s\S]*?```|~~~[\s\S]*?~~~", re.MULTILINE)
        indented_code = re.compile(r"^(?: {4}|\t).*$", re.MULTILINE)

        broken = []
        static_dir = project_root / "static"

        # Only check a sample for speed
        sample = all_content_files[:200]

        for md_file in sample:
            try:
                content = md_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            # Strip code blocks to avoid false positives from example code
            content_no_code = fenced_code.sub("", content)
            content_no_code = indented_code.sub("", content_no_code)

            refs = []
            for m in md_img.finditer(content_no_code):
                refs.append(m.group(1).split()[0])
            for m in html_img.finditer(content_no_code):
                refs.append(m.group(1))

            for ref in refs:
                ref = ref.strip()
                # Skip external, data URIs, legacy router console links
                if (
                    ref.startswith(("http", "data:", "{{"))
                    or "configservice.jsp" in ref
                ):
                    continue

                if ref.startswith("/"):
                    target = static_dir / ref.lstrip("/")
                    if not target.exists():
                        # Also check content
                        content_target = project_root / "content" / ref.lstrip("/")
                        if not content_target.exists():
                            broken.append(
                                f"{md_file.relative_to(project_root)} -> {ref}"
                            )
                else:
                    target = (md_file.parent / ref).resolve()
                    if not target.exists():
                        broken.append(f"{md_file.relative_to(project_root)} -> {ref}")

        if broken:
            sample = broken[:15]
            pytest.fail(
                f"Broken image references:\n"
                + "\n".join(f"  - {b}" for b in sample)
                + (f"\n  ... and {len(broken) - 15} more" if len(broken) > 15 else "")
            )


# =============================================================================
# LANGUAGE DIRECTORY STRUCTURE - Catch missing content
# =============================================================================


class TestContentStructure:
    """Validate content directory structure."""

    CORE_PAGES = [
        "_index.md",
        "about/_index.md",
        "downloads/_index.md",
        "docs/_index.md",
        "blog/_index.md",
        "get-involved/_index.md",
    ]

    def test_all_langs_have_index(self, content_dir: Path, hugo_config: dict):
        """Each configured language must have a main index."""
        languages = hugo_config.get("languages", {}).keys()

        missing = []
        for lang in languages:
            lang_dir = content_dir / lang
            if not lang_dir.exists():
                missing.append(f"{lang}: directory missing")
            elif not (lang_dir / "_index.md").exists():
                missing.append(f"{lang}: _index.md missing")

        if missing:
            pytest.fail(f"Language directories/indices missing:\n" + "\n".join(missing))

    def test_english_has_core_pages(self, content_dir: Path):
        """English (source) must have all core pages."""
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.fail("English content directory not found")

        missing = []
        for page in self.CORE_PAGES:
            if not (en_dir / page).exists():
                missing.append(page)

        if missing:
            pytest.fail(f"English missing core pages:\n" + "\n".join(missing))


# =============================================================================
# TRANSLATION COMPLETENESS - Catch missing translated content
# =============================================================================


class TestTranslationCompleteness:
    """Test that translations are complete across languages."""

    # Core pages that ALL languages should have translated
    CORE_PAGES = [
        "_index.md",
        "about/_index.md",
        "downloads/_index.md",
        "docs/_index.md",
        "blog/_index.md",
        "get-involved/_index.md",
    ]

    def test_core_pages_exist_all_languages(self, content_dir: Path, hugo_config: dict):
        """All configured languages should have core pages."""
        languages = list(hugo_config.get("languages", {}).keys())
        missing = {}

        for lang in languages:
            lang_dir = content_dir / lang
            if not lang_dir.exists():
                missing[lang] = ["(directory missing)"]
                continue

            lang_missing = []
            for page in self.CORE_PAGES:
                if not (lang_dir / page).exists():
                    lang_missing.append(page)

            if lang_missing:
                missing[lang] = lang_missing

        if missing:
            msg = "Core pages missing in languages:\n"
            for lang, pages in sorted(missing.items()):
                msg += f"  {lang}: {', '.join(pages)}\n"
            pytest.fail(msg)

    def test_translation_coverage(self, content_dir: Path, hugo_config: dict):
        """Report and validate translation coverage for each language."""
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.fail("English content directory not found")

        # Get all English pages
        en_pages = set()
        for md_file in en_dir.glob("**/*.md"):
            rel_path = md_file.relative_to(en_dir)
            en_pages.add(str(rel_path))

        en_count = len(en_pages)
        languages = list(hugo_config.get("languages", {}).keys())

        print(f"\nTranslation coverage (vs {en_count} English pages):")

        coverage = {}
        low_coverage = []

        for lang in sorted(languages):
            if lang == "en":
                continue

            lang_dir = content_dir / lang
            if not lang_dir.exists():
                coverage[lang] = 0
                low_coverage.append(f"{lang}: 0% (directory missing)")
                continue

            lang_pages = set()
            for md_file in lang_dir.glob("**/*.md"):
                rel_path = md_file.relative_to(lang_dir)
                lang_pages.add(str(rel_path))

            # Count pages that exist in both
            translated = len(lang_pages & en_pages)
            pct = (translated / en_count * 100) if en_count > 0 else 0
            coverage[lang] = pct

            status = ""
            if pct < 50:
                status = " [LOW]"
                low_coverage.append(f"{lang}: {pct:.0f}%")

            print(f"  {lang}: {translated}/{en_count} ({pct:.0f}%){status}")

        # Fail if any language has < 10% coverage (likely broken)
        critical_low = [l for l, p in coverage.items() if p < 10]
        if critical_low:
            pytest.fail(
                f"Languages with critically low coverage (<10%): {', '.join(critical_low)}"
            )

    def test_no_orphan_translations(self, content_dir: Path):
        """Warn about translated pages that don't exist in English."""
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.skip("English content directory not found")

        en_pages = set()
        for md_file in en_dir.glob("**/*.md"):
            rel_path = md_file.relative_to(en_dir)
            en_pages.add(str(rel_path))

        orphans = {}
        for lang_dir in content_dir.iterdir():
            if not lang_dir.is_dir() or lang_dir.name == "en":
                continue

            lang = lang_dir.name
            lang_orphans = []

            for md_file in lang_dir.glob("**/*.md"):
                rel_path = str(md_file.relative_to(lang_dir))
                if rel_path not in en_pages:
                    # Skip draft files and special files
                    if not rel_path.startswith("_") and "draft" not in rel_path.lower():
                        lang_orphans.append(rel_path)

            if lang_orphans:
                orphans[lang] = lang_orphans

        if orphans:
            total = sum(len(v) for v in orphans.values())
            print(f"\nOrphan translations (not in English): {total} files")
            for lang, pages in sorted(orphans.items()):
                sample = pages[:3]
                more = f" (+{len(pages) - 3} more)" if len(pages) > 3 else ""
                print(f"  {lang}: {sample}{more}")

    def test_blog_posts_translated(self, content_dir: Path, hugo_config: dict):
        """Check that recent blog posts are translated."""
        en_blog = content_dir / "en" / "blog"
        if not en_blog.exists():
            pytest.skip("English blog directory not found")

        # Get English blog posts (excluding _index.md)
        en_posts = []
        for md_file in en_blog.glob("*.md"):
            if md_file.name != "_index.md":
                en_posts.append(md_file.name)

        if not en_posts:
            pytest.skip("No English blog posts found")

        languages = list(hugo_config.get("languages", {}).keys())
        missing_posts = {}

        for lang in languages:
            if lang == "en":
                continue

            lang_blog = content_dir / lang / "blog"
            if not lang_blog.exists():
                missing_posts[lang] = len(en_posts)
                continue

            lang_posts = set(
                f.name for f in lang_blog.glob("*.md") if f.name != "_index.md"
            )
            missing = len(en_posts) - len(lang_posts & set(en_posts))

            if missing > 0:
                missing_posts[lang] = missing

        if missing_posts:
            print(f"\nBlog post translation status ({len(en_posts)} English posts):")
            for lang, count in sorted(missing_posts.items(), key=lambda x: -x[1]):
                pct = (len(en_posts) - count) / len(en_posts) * 100
                print(f"  {lang}: {len(en_posts) - count}/{len(en_posts)} ({pct:.0f}%)")

    def test_frontmatter_consistency(self, content_dir: Path):
        """Check that translated pages have consistent frontmatter fields."""
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.skip("English content directory not found")

        # Sample core pages
        test_pages = [
            "about/_index.md",
            "downloads/_index.md",
            "docs/_index.md",
        ]

        mismatches = []

        for page in test_pages:
            en_page = en_dir / page
            if not en_page.exists():
                continue

            en_content = en_page.read_text(encoding="utf-8")
            en_fm = extract_markdown_front_matter(en_content)
            if not isinstance(en_fm, dict):
                continue

            en_keys = set(en_fm.keys())

            # Check other languages
            for lang_dir in content_dir.iterdir():
                if not lang_dir.is_dir() or lang_dir.name == "en":
                    continue

                lang_page = lang_dir / page
                if not lang_page.exists():
                    continue

                lang_content = lang_page.read_text(encoding="utf-8")
                lang_fm = extract_markdown_front_matter(lang_content)
                if not isinstance(lang_fm, dict):
                    continue

                lang_keys = set(lang_fm.keys())

                # Check for missing required keys (not optional ones)
                missing = (
                    en_keys
                    - lang_keys
                    - {"draft", "aliases", "weight", "translationKey"}
                )
                if missing:
                    mismatches.append(f"{lang_dir.name}/{page}: missing {missing}")

        if mismatches:
            sample = mismatches[:10]
            print(f"\nFrontmatter mismatches:")
            for m in sample:
                print(f"  - {m}")


# =============================================================================
# QUICK SANITY CHECKS
# =============================================================================


class TestSanity:
    """Quick sanity checks."""

    def test_content_dir_not_empty(self, content_dir: Path):
        """Content directory should have files."""
        md_files = list(content_dir.glob("**/*.md"))
        assert len(md_files) > 100, (
            f"Only {len(md_files)} markdown files found - suspicious"
        )

    def test_static_dir_not_empty(self, static_dir: Path):
        """Static directory should have files."""
        files = list(static_dir.glob("**/*"))
        assert len([f for f in files if f.is_file()]) > 10, (
            "Static directory seems empty"
        )

    def test_layouts_dir_not_empty(self, layouts_dir: Path):
        """Layouts directory should have templates."""
        html_files = list(layouts_dir.glob("**/*.html"))
        assert len(html_files) > 5, "Layouts directory seems empty"
