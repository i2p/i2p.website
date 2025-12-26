"""Test configuration file validation.

Tests:
- Validate hugo.toml TOML syntax
- Validate data/downloads.yaml syntax and structure
- Validate all i18n/*.toml files for proper TOML syntax
"""

from pathlib import Path
import re

import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib
import yaml

from .utils import validate_sha256_hash


def test_hugo_config_valid_toml(hugo_config: dict) -> None:
    """Test that hugo.toml is valid TOML."""
    assert isinstance(hugo_config, dict)
    assert len(hugo_config) > 0


def test_hugo_config_required_fields(hugo_config: dict) -> None:
    """Test that hugo.toml contains required top-level fields."""
    required_fields = ["baseURL", "languages", "params"]
    for field in required_fields:
        assert field in hugo_config, f"Missing required field: {field}"


def test_hugo_config_languages_configured(hugo_config: dict) -> None:
    """Test that languages are properly configured."""
    assert "languages" in hugo_config
    assert isinstance(hugo_config["languages"], dict)
    assert len(hugo_config["languages"]) > 0

    languages = hugo_config["languages"]
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
        assert lang in languages, f"Missing language configuration: {lang}"


def test_downloads_yaml_valid(downloads_config: dict) -> None:
    """Test that data/downloads.yaml is valid YAML."""
    assert isinstance(downloads_config, dict)
    assert len(downloads_config) > 0


def test_downloads_required_fields(downloads_config: dict) -> None:
    """Test that downloads.yaml contains required top-level fields."""
    assert "current_version" in downloads_config
    assert "android_version" in downloads_config
    assert "downloads" in downloads_config
    assert isinstance(downloads_config["downloads"], dict)


def test_downloads_version_format(downloads_config: dict) -> None:
    """Test that version numbers follow semantic versioning."""
    current_version = downloads_config["current_version"]
    android_version = downloads_config["android_version"]

    version_pattern = r"^\d+\.\d+\.\d+(-\d+)?$"
    assert current_version, "current_version is empty"
    assert android_version, "android_version is empty"

    assert re.match(version_pattern, current_version), (
        f"Invalid current_version format: {current_version}"
    )
    assert re.match(version_pattern, android_version), (
        f"Invalid android_version format: {android_version}"
    )


def test_download_entries_structure(downloads_config: dict) -> None:
    """Test that each download entry has required fields."""
    downloads = downloads_config["downloads"]
    assert len(downloads) > 0, "No download entries found"

    required_fields = ["file", "size", "sha256", "links"]

    for name, entry in downloads.items():
        assert isinstance(entry, dict), f"Download entry '{name}' is not a dict"

        for field in required_fields:
            assert field in entry, f"Download entry '{name}' missing field: {field}"

        assert isinstance(entry["links"], dict), (
            f"Download entry '{name}' links is not a dict"
        )


def test_download_links_required_types(downloads_config: dict) -> None:
    """Test that each download has required link types."""
    downloads = downloads_config["downloads"]
    required_links = ["primary"]
    optional_links = ["mirror", "torrent", "i2p", "tor", "github"]

    for name, entry in downloads.items():
        links = entry["links"]

        for link_type in required_links:
            assert link_type in links, (
                f"Download entry '{name}' missing required link: {link_type}"
            )
            assert links[link_type], (
                f"Download entry '{name}' has empty {link_type} link"
            )

        at_least_one_optional = any(
            link in links and links[link] for link in optional_links
        )
        assert at_least_one_optional, (
            f"Download entry '{name}' should have at least one optional link (mirror, torrent, i2p, tor, github)"
        )


@pytest.mark.skip(reason="Temporarily disabled for live CI/CD testing")
def test_download_sha256_hashes_valid(downloads_config: dict) -> None:
    """Test that all SHA256 hashes are valid 64-character hex strings."""
    downloads = downloads_config["downloads"]

    for name, entry in downloads.items():
        sha256 = entry["sha256"]
        assert validate_sha256_hash(sha256), (
            f"Download entry '{name}' has invalid SHA256 hash: {sha256}"
        )


def test_download_file_sizes_format(downloads_config: dict) -> None:
    """Test that file sizes are properly formatted."""
    downloads = downloads_config["downloads"]

    for name, entry in downloads.items():
        size = entry["size"]
        assert isinstance(size, str), f"Download entry '{name}' size is not a string"
        assert len(size) > 0, f"Download entry '{name}' size is empty"

        size_pattern = r"^~?\d+(\.\d+)?\s*[KMGT]?B?$"
        assert re.search(size_pattern, size), (
            f"Download entry '{name}' has invalid size format: {size}"
        )


def test_android_download_structure(downloads_config: dict) -> None:
    """Test that Android download entry has required fields."""
    assert "downloads" in downloads_config
    assert "android" in downloads_config["downloads"]

    android = downloads_config["downloads"]["android"]
    assert "version" in android, "Android download missing version field"
    assert "requirements" in android, "Android download missing requirements field"

    assert isinstance(android["version"], str), "Android version is not a string"
    assert isinstance(android["requirements"], str), (
        "Android requirements is not a string"
    )


def test_i18n_files_exist(i18n_files: dict[str, Path]) -> None:
    """Test that all expected i18n files exist."""
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
        assert i18n_files[lang].exists(), f"i18n file not found: {i18n_files[lang]}"


def test_i18n_files_valid_toml(i18n_files: dict[str, Path]) -> None:
    """Test that all i18n files are valid TOML."""
    for lang, file_path in i18n_files.items():
        with open(file_path, "rb") as f:
            content = tomllib.load(f)
        assert isinstance(content, dict), f"i18n/{lang}.toml does not parse as dict"
        assert len(content) > 0, f"i18n/{lang}.toml is empty"


def test_i18n_english_has_content(i18n_files: dict[str, Path]) -> None:
    """Test that English i18n file has translation keys."""
    en_file = i18n_files["en"]
    with open(en_file, "rb") as f:
        en_content = tomllib.load(f)

    assert isinstance(en_content, dict), "en.toml is not a dict"
    assert len(en_content) > 0, "en.toml has no translations"

    total_keys = 0
    for section, translations in en_content.items():
        if isinstance(translations, dict):
            total_keys += len(translations)

    assert total_keys > 100, "en.toml should have at least 100 translation keys"


def test_mirrors_config(downloads_config: dict) -> None:
    """Test that mirrors section exists and is properly configured."""
    assert "mirrors" in downloads_config
    mirrors = downloads_config["mirrors"]

    assert isinstance(mirrors, dict), "mirrors is not a dict"
    assert len(mirrors) > 0, "mirrors section is empty"

    assert "primary" in mirrors, "Missing primary mirror"
    primary = mirrors["primary"]
    assert "name" in primary, "Primary mirror missing name"
    assert "url" in primary, "Primary mirror missing url"
    assert primary["url"].startswith(("http://", "https://")), (
        "Primary mirror URL should start with http:// or https://"
    )


def test_resources_config(downloads_config: dict) -> None:
    """Test that resources section exists and is properly configured."""
    assert "resources" in downloads_config
    resources = downloads_config["resources"]

    assert isinstance(resources, dict), "resources is not a dict"
    assert "archive" in resources, "Missing archive resource"
    assert "pgp_keys" in resources, "Missing pgp_keys resource"

    archive_url = resources["archive"]
    assert archive_url.startswith(("http://", "https://")), (
        f"Archive URL should start with http:// or https://: {archive_url}"
    )
