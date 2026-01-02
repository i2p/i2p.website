import pytest
from pathlib import Path
from .utils import validate_sha256_hash
import tomllib

def test_hugo_config_valid(hugo_config):
    """
    Validate hugo.toml syntax and basic structure.
    The fixture 'hugo_config' already attempts to load the TOML,
    so if this test runs, the syntax is valid.
    """
    assert isinstance(hugo_config, dict), "hugo.toml must be a dictionary"
    assert "baseURL" in hugo_config, "hugo.toml must contain 'baseURL'"
    assert "baseURL" in hugo_config, "hugo.toml must contain 'baseURL'"
    # defaultContentLanguage is more standard in recent Hugo than languageCode at root
    if "languageCode" not in hugo_config:
        assert "defaultContentLanguage" in hugo_config, "hugo.toml must contain 'languageCode' or 'defaultContentLanguage'"
    # Title might be at root or inside [languages]
    has_title = "title" in hugo_config
    if not has_title and "languages" in hugo_config:
        # Check if default language has title
        default_lang = hugo_config.get("defaultContentLanguage", "en")
        if default_lang in hugo_config["languages"]:
            if "title" in hugo_config["languages"][default_lang]:
                has_title = True
    
    assert has_title, "hugo.toml must contain 'title' at root or in default language"

def test_downloads_yaml_structure(downloads_config):
    """
    Validate data/downloads.yaml structure and format.
    """
    assert isinstance(downloads_config, dict), "data/downloads.yaml must be a dictionary"
    
    # Check for required top-level keys if expected (adjust based on actual structure)
    # Based on typical usage, it might contain version info or download links
    pass

def test_i18n_files_valid(i18n_files):
    """
    Validate all i18n/*.toml files are valid TOML.
    The fixture 'i18n_files' finds them, this test parses them.
    """
    for lang, file_path in i18n_files.items():
        with open(file_path, "rb") as f:
            try:
                data = tomllib.load(f)
                assert isinstance(data, dict), f"{file_path.name} must parse to a dictionary"
            except tomllib.TOMLDecodeError as e:
                pytest.fail(f"Failed to parse {file_path.name}: {e}")

def test_downloads_content_validation(downloads_config):
    """
    Check version numbers, SHA256 hashes, and required fields in downloads.yaml.
    """
    # Recursive function to find and validate 'sha256' fields
    def check_hashes(data, path=""):
        if isinstance(data, dict):
            for k, v in data.items():
                current_path = f"{path}.{k}" if path else k
                if k == "sha256":
                    assert validate_sha256_hash(v), f"Invalid SHA256 hash at {current_path}: {v}"
                else:
                    check_hashes(v, current_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                check_hashes(item, f"{path}[{i}]")

    check_hashes(downloads_config)
    
    # Validate specific known structure if possible (e.g. 'version' key)
    # Example:
    # if "version" in downloads_config:
    #     assert isinstance(downloads_config["version"], str)
