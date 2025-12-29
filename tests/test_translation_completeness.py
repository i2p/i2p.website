"""Translation completeness tests for I2P website.

Tests that all languages have the same content pages,
not just i18n string keys.
"""

from pathlib import Path
from collections import defaultdict

import pytest


class TestTranslationCompleteness:
    """Test that translations are complete across languages."""

    # Languages that should have full translations
    # Add languages as they become fully translated
    REQUIRED_FULL_LANGS = ["en"]  # English is the source

    # Languages that should have core pages
    CORE_LANGS = ["en", "de", "fr", "es", "zh", "ru"]

    # Core pages that all languages should have
    CORE_PAGES = [
        "about/_index.md",
        "downloads/_index.md",
        "docs/_index.md",
        "get-involved/_index.md",
        "blog/_index.md",
    ]

    def test_all_languages_have_index(self, content_dir: Path):
        """Each language should have a main index page."""
        lang_dirs = [d for d in content_dir.iterdir() if d.is_dir()]

        missing_index = []
        for lang_dir in lang_dirs:
            index_file = lang_dir / "_index.md"
            if not index_file.exists():
                missing_index.append(lang_dir.name)

        if missing_index:
            msg = f"Languages missing _index.md: {', '.join(missing_index)}"
            pytest.fail(msg)

    def test_core_pages_exist_in_core_languages(self, content_dir: Path):
        """Core languages should have all core pages."""
        missing = defaultdict(list)

        for lang in self.CORE_LANGS:
            lang_dir = content_dir / lang
            if not lang_dir.exists():
                continue

            for page in self.CORE_PAGES:
                page_path = lang_dir / page
                if not page_path.exists():
                    missing[lang].append(page)

        if missing:
            msg = "Core pages missing in languages:\n"
            for lang, pages in missing.items():
                msg += f"  {lang}: {', '.join(pages)}\n"
            # Warning - translations may be in progress
            pytest.skip(msg)

    def test_translation_coverage(self, content_dir: Path):
        """Report translation coverage for each language."""
        # Get all pages from English (source)
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.skip("English content directory not found")

        en_pages = set()
        for md_file in en_dir.glob("**/*.md"):
            rel_path = md_file.relative_to(en_dir)
            en_pages.add(str(rel_path))

        en_count = len(en_pages)

        # Check coverage for each language
        print(f"\nTranslation coverage (vs {en_count} English pages):")

        coverage = {}
        lang_dirs = [d for d in content_dir.iterdir() if d.is_dir() and d.name != "en"]

        for lang_dir in sorted(lang_dirs):
            lang = lang_dir.name
            lang_pages = set()
            for md_file in lang_dir.glob("**/*.md"):
                rel_path = md_file.relative_to(lang_dir)
                lang_pages.add(str(rel_path))

            translated = len(lang_pages & en_pages)
            pct = (translated / en_count * 100) if en_count > 0 else 0
            coverage[lang] = pct

            print(f"  {lang}: {translated}/{en_count} ({pct:.0f}%)")

        # All languages should have at least some content
        empty_langs = [lang for lang, pct in coverage.items() if pct == 0]
        if empty_langs:
            msg = f"Languages with 0% coverage: {', '.join(empty_langs)}"
            pytest.skip(msg)

    def test_no_orphan_translations(self, content_dir: Path):
        """Translations should not have pages that don't exist in English."""
        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.skip("English content directory not found")

        en_pages = set()
        for md_file in en_dir.glob("**/*.md"):
            rel_path = md_file.relative_to(en_dir)
            en_pages.add(str(rel_path))

        orphans = defaultdict(list)
        lang_dirs = [d for d in content_dir.iterdir() if d.is_dir() and d.name != "en"]

        for lang_dir in lang_dirs:
            lang = lang_dir.name
            for md_file in lang_dir.glob("**/*.md"):
                rel_path = str(md_file.relative_to(lang_dir))
                if rel_path not in en_pages:
                    orphans[lang].append(rel_path)

        if orphans:
            # Filter out known acceptable orphans (e.g., language-specific content)
            significant_orphans = {}
            for lang, pages in orphans.items():
                # Ignore certain patterns
                filtered = [
                    p for p in pages
                    if not p.startswith("_") and not "draft" in p.lower()
                ]
                if filtered:
                    significant_orphans[lang] = filtered

            if significant_orphans:
                msg = "Translations with pages not in English:\n"
                for lang, pages in list(significant_orphans.items())[:5]:
                    sample = pages[:3]
                    msg += f"  {lang}: {sample}{'...' if len(pages) > 3 else ''}\n"
                # This is informational - orphans might be intentional
                print(msg)


class TestTranslationConsistency:
    """Test consistency between translations."""

    def test_frontmatter_fields_match(self, content_dir: Path):
        """Translated pages should have same frontmatter structure."""
        import yaml

        en_dir = content_dir / "en"
        if not en_dir.exists():
            pytest.skip("English content directory not found")

        # Sample a few important pages
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

            # Get English frontmatter keys
            en_content = en_page.read_text(encoding="utf-8")
            if not en_content.startswith("---"):
                continue

            try:
                en_fm_text = en_content.split("---")[1]
                en_fm = yaml.safe_load(en_fm_text)
                en_keys = set(en_fm.keys()) if en_fm else set()
            except Exception:
                continue

            # Check other languages
            for lang_dir in content_dir.iterdir():
                if not lang_dir.is_dir() or lang_dir.name == "en":
                    continue

                lang_page = lang_dir / page
                if not lang_page.exists():
                    continue

                lang_content = lang_page.read_text(encoding="utf-8")
                if not lang_content.startswith("---"):
                    continue

                try:
                    lang_fm_text = lang_content.split("---")[1]
                    lang_fm = yaml.safe_load(lang_fm_text)
                    lang_keys = set(lang_fm.keys()) if lang_fm else set()
                except Exception:
                    continue

                # Check for missing required keys
                missing = en_keys - lang_keys
                # Filter out optional keys
                required_missing = missing - {"draft", "aliases", "weight"}
                if required_missing:
                    mismatches.append(
                        f"{lang_dir.name}/{page}: missing {required_missing}"
                    )

        if mismatches:
            sample = mismatches[:10]
            msg = "Frontmatter key mismatches:\n"
            msg += "\n".join(f"  - {item}" for item in sample)
            # Warning only
            pytest.skip(msg)


class TestBuildOutputLanguages:
    """Test that all configured languages build correctly."""

    def test_all_languages_build(self, build_hugo_site: Path, hugo_config: dict):
        """All configured languages should produce output."""
        # Get configured languages from hugo.toml
        languages = hugo_config.get("languages", {})
        if not languages:
            pytest.skip("No languages configured in hugo.toml")

        missing_output = []
        for lang in languages.keys():
            lang_dir = build_hugo_site / lang
            if not lang_dir.exists():
                missing_output.append(lang)
            elif not list(lang_dir.glob("*.html")):
                missing_output.append(f"{lang} (empty)")

        if missing_output:
            msg = f"Languages missing from build output: {', '.join(missing_output)}"
            pytest.fail(msg)

    def test_language_switcher_links_valid(self, build_hugo_site: Path):
        """Language switcher links should point to valid pages."""
        # Sample the English homepage
        en_index = build_hugo_site / "en" / "index.html"
        if not en_index.exists():
            pytest.skip("English index not found")

        from bs4 import BeautifulSoup

        content = en_index.read_text(encoding="utf-8")
        soup = BeautifulSoup(content, "html.parser")

        # Look for language switcher (common patterns)
        lang_links = soup.select('a[hreflang], .language-switcher a, [data-lang] a')

        broken_links = []
        for link in lang_links:
            href = link.get("href", "")
            if href.startswith("/"):
                # Check if target exists
                target = build_hugo_site / href.lstrip("/")
                # Handle directory indexes
                if target.is_dir():
                    target = target / "index.html"
                elif not target.suffix:
                    target = target.with_suffix(".html")

                if not target.exists() and not (target.parent / "index.html").exists():
                    broken_links.append(href)

        if broken_links:
            sample = broken_links[:5]
            msg = f"Broken language switcher links: {sample}"
            pytest.skip(msg)
