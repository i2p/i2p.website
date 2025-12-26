"""Pytest configuration and shared fixtures for I2P website tests."""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Generator

import pytest
import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def i18n_dir(project_root: Path) -> Path:
    """Get the i18n directory."""
    return project_root / "i18n"


@pytest.fixture(scope="session")
def content_dir(project_root: Path) -> Path:
    """Get the content directory."""
    return project_root / "content"


@pytest.fixture(scope="session")
def static_dir(project_root: Path) -> Path:
    """Get the static directory."""
    return project_root / "static"


@pytest.fixture(scope="session")
def data_dir(project_root: Path) -> Path:
    """Get the data directory."""
    return project_root / "data"


@pytest.fixture(scope="session")
def layouts_dir(project_root: Path) -> Path:
    """Get the layouts directory."""
    return project_root / "layouts"


@pytest.fixture(scope="session")
def hugo_config(project_root: Path) -> dict:
    """Load and parse hugo.toml."""
    config_path = project_root / "hugo.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)


@pytest.fixture(scope="session")
def downloads_config(data_dir: Path) -> dict:
    """Load and parse data/downloads.yaml."""
    downloads_path = data_dir / "downloads.yaml"
    with open(downloads_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def i18n_files(i18n_dir: Path) -> dict[str, Path]:
    """Get all i18n TOML files."""
    return {lang.stem: lang for lang in i18n_dir.glob("*.toml")}


@pytest.fixture(scope="session")
def hugo_bin_path() -> Path:
    """Find Hugo binary path."""
    hugo_path = shutil.which("hugo")
    if not hugo_path:
        pytest.skip("Hugo not found in PATH")
    return Path(hugo_path)


@pytest.fixture(scope="function")
def hugo_build_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for Hugo build output."""
    with tempfile.TemporaryDirectory(prefix="hugo-test-") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(scope="function")
def build_hugo_site(
    project_root: Path, hugo_bin_path: Path, hugo_build_dir: Path
) -> Generator[Path, None, None]:
    """Build Hugo site to a temporary directory."""
    original_dir = os.getcwd()
    try:
        os.chdir(project_root)
        cmd = [
            str(hugo_bin_path),
            "--destination",
            str(hugo_build_dir),
            "--quiet",
            "--gc",
            "--minify",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            pytest.fail(
                f"Hugo build failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )

        yield hugo_build_dir
    finally:
        os.chdir(original_dir)


@pytest.fixture(scope="session")
def all_content_files(content_dir: Path) -> list[Path]:
    """Get all markdown files in content directory."""
    return list(content_dir.glob("**/*.md"))


@pytest.fixture(scope="session")
def all_static_files(static_dir: Path) -> list[Path]:
    """Get all files in static directory."""
    return list(static_dir.glob("**/*"))

    if not lines[0].startswith("---"):
        return {}

    front_matter_lines = []
    for line in lines[1:]:
        if line.startswith("---"):
            break
        front_matter_lines.append(line)

    front_matter_str = "\n".join(front_matter_lines)
    try:
        return yaml.safe_load(front_matter_str) or {}
    except yaml.YAMLError:
        return {}
