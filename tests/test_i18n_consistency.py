"""Test i18n translation consistency across all languages.

Tests:
- Extract all translation keys from en.toml
- Verify each key exists in all other language files
- Report missing translations per language
"""

import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .utils import get_all_nested_keys


def get_translation_keys(file_path: str) -> dict:
    """Get all translation keys from a TOML file."""
    with open(file_path, "rb") as f:
        content = tomllib.load(f)

    keys = {}
    for section, translations in content.items():
        if isinstance(translations, dict):
            keys[section] = set(translations.keys())

    return keys


def test_english_translations_exist(i18n_files: dict[str, str]) -> None:
    """Test that English i18n file exists and has content."""
    assert "en" in i18n_files, "English i18n file not found"
    en_file = i18n_files["en"]

    with open(en_file, "rb") as f:
        en_content = tomllib.load(f)

    assert isinstance(en_content, dict), "English translations not a dict"
    assert len(en_content) > 0, "English translations empty"


def test_english_translation_sections(i18n_files: dict[str, str]) -> None:
    """Test that English i18n has expected sections."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    assert len(en_keys) > 5, f"Expected at least 5 sections, found {len(en_keys)}"

    expected_sections = ["feedback", "research", "security", "getInvolved", "footer"]

    found_sections = set(en_keys.keys())
    for section in expected_sections:
        assert section in found_sections, f"Missing expected section: {section}"


def test_all_languages_have_translations(i18n_files: dict[str, str]) -> None:
    """Test that all language i18n files exist and have content."""
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

    for lang in expected_languages:
        assert lang in i18n_files, f"Missing i18n file: {lang}.toml"

        file_path = i18n_files[lang]
        with open(file_path, "rb") as f:
            content = tomllib.load(f)

        assert isinstance(content, dict), f"{lang}.toml is not a dict"
        assert len(content) > 0, f"{lang}.toml is empty"


def test_english_keys_count(i18n_files: dict[str, str]) -> None:
    """Test and report total English translation key count."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    total_keys = sum(len(keys) for keys in en_keys.values())

    print(f"\n✅ English has {total_keys} translation keys in {len(en_keys)} sections")

    assert total_keys > 100, f"Expected at least 100 English keys, found {total_keys}"


def test_all_languages_match_english_sections(i18n_files: dict[str, str]) -> None:
    """Test that all languages have the same sections as English."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    en_sections = set(en_keys.keys())

    missing_sections = {}

    for lang, file_path in i18n_files.items():
        if lang == "en":
            continue

        lang_keys = get_translation_keys(file_path)
        lang_sections = set(lang_keys.keys())

        missing = en_sections - lang_sections
        if missing:
            missing_sections[lang] = missing

    if missing_sections:
        print("\n❌ Missing sections by language:")
        for lang, sections in sorted(missing_sections.items()):
            print(f"  {lang}: {', '.join(sorted(sections))}")

        pytest.fail(f"{len(missing_sections)} languages are missing sections")


def test_all_translations_match_english_keys(i18n_files: dict[str, str]) -> None:
    """Test that all languages have all English translation keys."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    missing_by_lang = {}
    total_missing = 0

    for lang, file_path in i18n_files.items():
        if lang == "en":
            continue

        lang_keys = get_translation_keys(file_path)

        missing_keys = {}
        for section in en_keys:
            if section not in lang_keys:
                missing_keys[section] = set(en_keys[section])
            else:
                missing = set(en_keys[section]) - lang_keys[section]
                if missing:
                    missing_keys[section] = missing

        if missing_keys:
            missing_count = sum(len(keys) for keys in missing_keys.values())
            missing_by_lang[lang] = (missing_count, missing_keys)
            total_missing += missing_count

    if missing_by_lang:
        print(f"\n❌ Missing translation keys: {total_missing} total")
        for lang, (count, keys_by_section) in sorted(missing_by_lang.items()):
            print(f"\n{lang.upper()} - Missing {count} keys:")
            for section, keys in sorted(keys_by_section.items()):
                for key in sorted(keys):
                    print(f"  - {section}.{key}")

        pytest.fail(f"{len(missing_by_lang)} languages are missing translation keys")


def test_no_extra_keys_in_non_english(i18n_files: dict[str, str]) -> None:
    """Test that non-English files don't have extra keys not in English."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    extra_by_lang = {}

    for lang, file_path in i18n_files.items():
        if lang == "en":
            continue

        lang_keys = get_translation_keys(file_path)

        extra_keys = {}
        for section, keys in lang_keys.items():
            if section not in en_keys:
                extra_keys[section] = keys
            else:
                extra = keys - en_keys[section]
                if extra:
                    if section not in extra_keys:
                        extra_keys[section] = set()
                    extra_keys[section].update(extra)

        if extra_keys:
            extra_count = sum(len(keys) for keys in extra_keys.values())
            extra_by_lang[lang] = (extra_count, extra_keys)

    if extra_by_lang:
        print(
            f"\n⚠️  Found extra keys not in English (these should probably be removed or added to English):"
        )
        for lang, (count, keys_by_section) in sorted(extra_by_lang.items()):
            print(f"\n{lang.upper()} - {count} extra keys:")
            for section, keys in sorted(keys_by_section.items()):
                for key in sorted(keys):
                    print(f"  - {section}.{key}")

        pytest.fail(f"{len(extra_by_lang)} languages have extra keys not in English")


def test_translation_key_coverage(i18n_files: dict[str, str]) -> None:
    """Test translation key coverage percentage for each language."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    total_en_keys = sum(len(keys) for keys in en_keys.values())

    coverage_report = {}

    for lang, file_path in i18n_files.items():
        lang_keys = get_translation_keys(file_path)

        present_keys = 0
        missing_keys = 0

        for section in en_keys:
            if section in lang_keys:
                present = len(en_keys[section] & lang_keys[section])
                missing = len(en_keys[section]) - present
                present_keys += present
                missing_keys += missing
            else:
                missing_keys += len(en_keys[section])

        coverage_pct = (present_keys / total_en_keys * 100) if total_en_keys > 0 else 0
        coverage_report[lang] = {
            "present": present_keys,
            "missing": missing_keys,
            "coverage": coverage_pct,
        }

    print(
        f"\n📊 Translation coverage report (English reference: {total_en_keys} keys):"
    )
    print(f"{'Language':<10} {'Present':<10} {'Missing':<10} {'Coverage':<10}")
    print("-" * 42)

    failures = []
    for lang in sorted(coverage_report.keys()):
        stats = coverage_report[lang]
        print(
            f"{lang:<10} {stats['present']:<10} {stats['missing']:<10} {stats['coverage']:.1f}%",
            end="",
        )

        if stats["coverage"] < 100:
            print(" ❌")
            failures.append(
                f"{lang} ({stats['coverage']:.1f}% - missing {stats['missing']} keys)"
            )
        else:
            print(" ✅")

    if failures:
        pytest.fail(
            f"\nLanguages with incomplete translations:\n"
            + "\n".join(f"  - {f}" for f in failures)
        )


def test_critical_translations_complete(i18n_files: dict[str, str]) -> None:
    """Test that critical translations are complete in all languages."""
    en_file = i18n_files["en"]
    en_keys = get_translation_keys(en_file)

    critical_keys = [
        ("footer", "quickLinks"),
        ("footer", "home"),
        ("footer", "about"),
        ("footer", "docs"),
        ("nav", "home"),
        ("nav", "about"),
        ("nav", "docs"),
    ]

    missing_critical = {}

    for lang, file_path in i18n_files.items():
        lang_keys = get_translation_keys(file_path)

        for section, key in critical_keys:
            if section not in lang_keys or key not in lang_keys[section]:
                if lang not in missing_critical:
                    missing_critical[lang] = []
                missing_critical[lang].append(f"{section}.{key}")

    if missing_critical:
        print("\n❌ Critical translation keys missing:")
        for lang, keys in sorted(missing_critical.items()):
            print(f"  {lang}: {', '.join(keys)}")

        pytest.fail(
            f"{len(missing_critical)} languages are missing critical translations"
        )
