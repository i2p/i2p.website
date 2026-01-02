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
    """Extract front matter from markdown content using regex."""
    if not content:
        return {}
    
    # Handle UTF-8 BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]

    # Match content between triple dashes at the start of the file
    # Handles potential leading whitespace/newlines
    match = re.search(r'^\s*---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    front_matter_str = match.group(1)
    try:
        return yaml.safe_load(front_matter_str) or {}
    except yaml.YAMLError:
        return {}
