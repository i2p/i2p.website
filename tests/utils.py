"""Shared utility functions for tests."""

import re
import yaml
from pathlib import Path
from typing import Dict, List


def get_all_nested_keys(data: Dict, prefix: str = "") -> List[str]:
    """Recursively get all nested keys from a dictionary."""
    keys = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.extend(get_all_nested_keys(value, full_key))
        else:
            keys.append(full_key)
    return keys


def validate_sha256_hash(hash_value: str) -> bool:
    """Validate SHA256 hash format (64 hex characters)."""
    if len(hash_value) != 64:
        return False
    try:
        int(hash_value, 16)
        return True
    except ValueError:
        return False


def extract_markdown_front_matter(content: str) -> Dict:
    """Extract front matter from markdown content."""
    lines = content.split("\n")

    if not lines:
        return {}

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
