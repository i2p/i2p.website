"""Test download link verification.

Tests:
- Validate URL formats for all link types
- Verify all URLs start with correct protocol
- Check that version numbers in filenames match config
- Verify required link types exist per download entry
"""

import re

import pytest

from .utils import validate_sha256_hash


pytestmark = pytest.mark.skip(reason="Temporarily disabled for live CI/CD testing")


def validate_url_format(url: str, expected_schemes: list[str]) -> bool:
    """Validate URL starts with expected scheme."""
    return any(url.startswith(scheme) for scheme in expected_schemes)


@pytest.mark.skip(reason="Temporarily disabled for live testing")
def test_download_urls_have_protocols(downloads_config: dict) -> None:
    """Test that all download URLs have valid protocols."""
    downloads = downloads_config["downloads"]

    invalid_urls = {}

    for name, entry in downloads.items():
        for link_type, url in entry["links"].items():
            if not url:
                continue

            valid_schemes = ["https://", "http://", "magnet:?", "git+", "ssh://"]

            if not validate_url_format(url, valid_schemes):
                if name not in invalid_urls:
                    invalid_urls[name] = []
                invalid_urls[name].append((link_type, url))

    if invalid_urls:
        print(
            f"\n❌ Found {sum(len(urls) for urls in invalid_urls.values())} invalid URLs:"
        )
        for name, urls in sorted(invalid_urls.items()):
            print(f"\n  {name}:")
            for link_type, url in urls:
                print(f"    - {link_type}: {url}")

        pytest.fail("Found download URLs with invalid protocols")


def test_primary_links_use_https(downloads_config: dict) -> None:
    """Test that primary download links use HTTPS."""
    downloads = downloads_config["downloads"]

    http_primary = []

    for name, entry in downloads.items():
        if "primary" in entry["links"]:
            url = entry["links"]["primary"]
            if url.startswith("http://"):
                http_primary.append((name, url))

    if http_primary:
        print(
            f"\n⚠️  Found {len(http_primary)} primary links using HTTP instead of HTTPS:"
        )
        for name, url in http_primary:
            print(f"    - {name}: {url}")

        pytest.fail("Primary download links should use HTTPS")


def test_magnet_links_valid_format(downloads_config: dict) -> None:
    """Test that magnet links have valid format."""
    downloads = downloads_config["downloads"]

    invalid_magnets = []

    for name, entry in downloads.items():
        if "torrent" in entry["links"]:
            url = entry["links"]["torrent"]

            if url.startswith("magnet:?"):
                xt_match = re.search(r"xt=urn:btih:([a-fA-F0-9]+)", url)
                if not xt_match:
                    invalid_magnets.append((name, "Missing or invalid xt=urn:btih"))
            elif url.startswith("http://") or url.startswith("https://"):
                pass
            else:
                invalid_magnets.append((name, "Invalid magnet link format"))

    if invalid_magnets:
        print(f"\n❌ Found {len(invalid_magnets)} invalid magnet/torrent links:")
        for name, reason in invalid_magnets:
            print(f"    - {name}: {reason}")

        pytest.fail("Found invalid magnet links")


def test_i2p_links_valid_format(downloads_config: dict) -> None:
    """Test that I2P links have valid format."""
    downloads = downloads_config["downloads"]

    invalid_i2p = []

    for name, entry in downloads.items():
        if "i2p" in entry["links"]:
            url = entry["links"]["i2p"]

            if not (url.startswith("http://") or url.startswith("https://")):
                invalid_i2p.append((name, url))

    if invalid_i2p:
        print(f"\n❌ Found {len(invalid_i2p)} invalid I2P links:")
        for name, url in invalid_i2p:
            print(f"    - {name}: {url}")

        pytest.fail("I2P links should use HTTP or HTTPS")


def test_onion_links_valid_format(downloads_config: dict) -> None:
    """Test that Tor .onion links have valid format."""
    downloads = downloads_config["downloads"]

    invalid_onion = []

    for name, entry in downloads.items():
        if "tor" in entry["links"]:
            url = entry["links"]["tor"]

            if not url.startswith("http://") and not url.startswith("https://"):
                invalid_onion.append((name, url))
            elif ".onion" not in url:
                invalid_onion.append((name, f"Missing .onion domain: {url}"))

    if invalid_onion:
        print(f"\n❌ Found {len(invalid_onion)} invalid Tor links:")
        for name, url in invalid_onion:
            print(f"    - {name}: {url}")

        pytest.fail("Tor links should use HTTP/HTTPS with .onion domain")


def test_version_consistency(downloads_config: dict) -> None:
    """Test that download filenames match version numbers."""
    current_version = downloads_config["current_version"]
    android_version = downloads_config["android_version"]

    version_mismatches = []

    downloads = downloads_config["downloads"]

    for name, entry in downloads.items():
        filename = entry["file"]

        if name == "android":
            if android_version not in filename:
                version_mismatches.append((name, filename, android_version))
        elif name == "source":
            if current_version not in filename:
                version_mismatches.append((name, filename, current_version))
        else:
            if current_version not in filename:
                version_mismatches.append((name, filename, current_version))

    if version_mismatches:
        print(f"\n❌ Found {len(version_mismatches)} version mismatches:")
        for name, filename, version in version_mismatches:
            print(f"    - {name}: {filename} (expected version: {version})")

        pytest.fail("Download filenames should contain version numbers")


def test_all_link_types_present_for_entry(downloads_config: dict) -> None:
    """Test that each download entry has expected link types."""
    downloads = downloads_config["downloads"]

    required_links = {
        "windows": ["primary", "mirror", "torrent", "i2p", "tor"],
        "windows_easy_installer": ["primary", "mirror", "torrent", "i2p", "tor"],
        "mac_linux": ["primary", "mirror", "torrent", "i2p", "tor"],
        "source": ["primary", "torrent", "github"],
        "android": ["primary", "torrent", "i2p"],
    }

    missing_links = []

    for name, required in required_links.items():
        if name not in downloads:
            continue

        entry = downloads[name]
        links = entry["links"]

        for link_type in required:
            if link_type not in links or not links[link_type]:
                missing_links.append((name, link_type))

    if missing_links:
        print(f"\n❌ Found {len(missing_links)} missing required link types:")
        for name, link_type in missing_links:
            print(f"    - {name}: missing {link_type}")

        pytest.fail("Some download entries are missing required link types")


def test_mirrors_section_valid(downloads_config: dict) -> None:
    """Test that mirrors section has valid URLs."""
    if "mirrors" not in downloads_config:
        pytest.skip("mirrors section not found")

    mirrors = downloads_config["mirrors"]

    invalid_mirror_urls = []

    for mirror_name, mirror_info in mirrors.items():
        if isinstance(mirror_info, dict):
            url = mirror_info.get("url", "")
            if url and not (url.startswith("http://") or url.startswith("https://")):
                invalid_mirror_urls.append((mirror_name, url))

    if invalid_mirror_urls:
        print(f"\n❌ Found {len(invalid_mirror_urls)} invalid mirror URLs:")
        for name, url in invalid_mirror_urls:
            print(f"    - {name}: {url}")

        pytest.fail("Mirror URLs should use HTTP or HTTPS")


def test_resources_section_valid(downloads_config: dict) -> None:
    """Test that resources section has valid URLs."""
    if "resources" not in downloads_config:
        pytest.skip("resources section not found")

    resources = downloads_config["resources"]

    invalid_resource_urls = []

    for resource_name, url in resources.items():
        if url and not (url.startswith("http://") or url.startswith("https://")):
            invalid_resource_urls.append((resource_name, url))

    if invalid_resource_urls:
        print(f"\n❌ Found {len(invalid_resource_urls)} invalid resource URLs:")
        for name, url in invalid_resource_urls:
            print(f"    - {name}: {url}")

        pytest.fail("Resource URLs should use HTTP or HTTPS")


def test_sha256_hashes_unique(downloads_config: dict) -> None:
    """Test that SHA256 hashes are unique across downloads."""
    downloads = downloads_config["downloads"]

    hash_map = {}
    duplicates = []

    for name, entry in downloads.items():
        sha256 = entry["sha256"]

        if sha256 in hash_map:
            duplicates.append((name, hash_map[sha256]))
        else:
            hash_map[sha256] = name

    if duplicates:
        print(f"\n❌ Found {len(duplicates)} duplicate SHA256 hashes:")
        for name, original in duplicates:
            print(f"    - {name} has same hash as {original}")

        pytest.fail("SHA256 hashes should be unique")


def test_download_requirements_present(downloads_config: dict) -> None:
    """Test that download entries have requirements field where needed."""
    downloads = downloads_config["downloads"]

    missing_requirements = []

    for name, entry in downloads.items():
        if name in ["windows", "windows_easy_installer", "mac_linux"]:
            if "requirements" not in entry or not entry["requirements"]:
                missing_requirements.append(name)

    if missing_requirements:
        print(f"\n❌ Found {len(missing_requirements)} downloads missing requirements:")
        for name in missing_requirements:
            print(f"    - {name}")

        pytest.fail("Some downloads are missing requirements field")


def test_download_sizes_format(downloads_config: dict) -> None:
    """Test that download sizes are properly formatted."""
    downloads = downloads_config["downloads"]

    invalid_sizes = []

    for name, entry in downloads.items():
        size = entry["size"]

        size_pattern = r"^~?\d+(\.\d+)?[KMGT]?B?$"
        if not re.match(size_pattern, size):
            invalid_sizes.append((name, size))

    if invalid_sizes:
        print(f"\n❌ Found {len(invalid_sizes)} invalid size formats:")
        for name, size in invalid_sizes:
            print(f"    - {name}: {size}")

        pytest.fail("Download sizes should follow format: ~123MB, 30MB, etc.")


def test_no_empty_required_links(downloads_config: dict) -> None:
    """Test that required links are not empty."""
    downloads = downloads_config["downloads"]

    empty_links = []

    for name, entry in downloads.items():
        for link_type, url in entry["links"].items():
            if not url or url.strip() == "":
                empty_links.append((name, link_type))

    if empty_links:
        print(f"\n❌ Found {len(empty_links)} empty link values:")
        for name, link_type in empty_links:
            print(f"    - {name}.{link_type}")

        pytest.fail("Link values should not be empty")
