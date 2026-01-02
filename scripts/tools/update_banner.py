#!/usr/bin/env python3
"""Update site banner message across all languages using Claude API.

This script:
1. Takes a new banner message (and optional link text/URL)
2. Translates it to all supported languages using Claude API
3. Updates all i18n/*.toml files with the translated messages
4. Increments the banner ID in hugo.toml

Example usage:
    # Update banner with just a message
    python3 scripts/update_banner.py "Important: I2P 2.8.0 Released!"
    
    # Update banner with message and link
    python3 scripts/update_banner.py "Important: I2P 2.8.0 Released!" \
        --link-text "Download Now" \
        --link-url "/downloads/"
    
    # Preview without making changes
    python3 scripts/update_banner.py "Test message" --dry-run

Environment:
    ANTHROPIC_API_KEY (required)
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

# Project paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_DIR = PROJECT_ROOT / "i18n"
HUGO_TOML = PROJECT_ROOT / "hugo.toml"

# Target languages (language code -> language name for prompts)
TARGET_LANGUAGES = {
    "es": "Spanish",
    "ko": "Korean", 
    "zh": "Chinese (Simplified)",
    "ru": "Russian",
    "cs": "Czech",
    "de": "German",
    "fr": "French",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "hi": "Hindi",
    "ar": "Arabic",
    "pt": "Portuguese",
}


def get_claude_client() -> anthropic.Anthropic:
    """Initialize Claude API client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def translate_banner(
    client: anthropic.Anthropic,
    message: str,
    link_text: Optional[str],
    target_lang: str,
    lang_name: str,
) -> Dict[str, str]:
    """Translate banner message and link text to target language."""
    
    # Build the translation request
    texts_to_translate = [f"banner_message: {message}"]
    if link_text:
        texts_to_translate.append(f"banner_link_text: {link_text}")
    
    prompt = f"""Translate the following website banner text to {lang_name}.

Keep translations concise and natural - this is for a website announcement banner.
Return ONLY the translated text in the exact same format (key: value), one per line.
Do not add quotes or extra formatting.

{chr(10).join(texts_to_translate)}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response
    result = {}
    response_text = response.content[0].text.strip()
    
    for line in response_text.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Remove any quotes that might have been added
            value = value.strip('"\'')
            result[key] = value
    
    return result


def update_i18n_file(
    filepath: Path,
    message: str,
    link_text: Optional[str],
    link_url: Optional[str],
    dry_run: bool = False,
) -> bool:
    """Update the [banner] section in an i18n TOML file."""
    
    if not filepath.exists():
        print(f"  Warning: {filepath} does not exist, skipping")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    # Find and update the [banner] section
    banner_pattern = r'(\[banner\]\s*\n)(.*?)(?=\n\[|\Z)'
    
    def replace_banner(match):
        section_header = match.group(1)
        
        # Build new banner content
        lines = [
            f'banner_message = "{message}"',
            f'banner_link_text = "{link_text or "Learn more"}"',
            f'banner_link_url = "{link_url or ""}"',
        ]
        
        # Preserve banner_close from original if it exists
        old_content = match.group(2)
        close_match = re.search(r'banner_close\s*=\s*["\']([^"\']+)["\']', old_content)
        if close_match:
            lines.append(f'banner_close = "{close_match.group(1)}"')
        else:
            lines.append('banner_close = "Close banner"')
        
        return section_header + '\n'.join(lines) + '\n'
    
    new_content = re.sub(banner_pattern, replace_banner, content, flags=re.DOTALL)
    
    if dry_run:
        print(f"  Would update: {filepath.name}")
        return True
    
    filepath.write_text(new_content, encoding='utf-8')
    print(f"  Updated: {filepath.name}")
    return True


def increment_banner_id(dry_run: bool = False) -> str:
    """Increment the banner ID in hugo.toml and return the new ID."""
    
    content = HUGO_TOML.read_text(encoding='utf-8')
    
    # Find current banner ID
    id_pattern = r'(id\s*=\s*["\'])banner-(\d+)(["\'])'
    match = re.search(id_pattern, content)
    
    if match:
        current_num = int(match.group(2))
        new_num = current_num + 1
        new_id = f"banner-{new_num}"
        
        new_content = re.sub(
            id_pattern,
            f'\\1banner-{new_num}\\3',
            content
        )
    else:
        # No banner ID found, set to banner-1
        new_id = "banner-1"
        new_content = content
        print("  Warning: No banner ID found in hugo.toml")
    
    if not dry_run and match:
        HUGO_TOML.write_text(new_content, encoding='utf-8')
        print(f"  Updated banner ID: banner-{current_num} → {new_id}")
    elif dry_run and match:
        print(f"  Would update banner ID: banner-{match.group(2)} → {new_id}")
    
    return new_id


def main():
    parser = argparse.ArgumentParser(
        description="Update site banner message across all languages"
    )
    parser.add_argument(
        "message",
        help="The banner message in English"
    )
    parser.add_argument(
        "--link-text",
        help="Text for the banner link (optional)"
    )
    parser.add_argument(
        "--link-url",
        help="URL for the banner link (optional, use '#poll' for poll modal)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--no-increment",
        action="store_true",
        help="Don't increment the banner ID"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("=== DRY RUN MODE ===\n")
    
    # Initialize Claude client
    print("Initializing Claude API client...")
    client = get_claude_client()
    
    # Update English first (no translation needed)
    print("\nUpdating English (en)...")
    en_file = I18N_DIR / "en.toml"
    update_i18n_file(
        en_file,
        args.message,
        args.link_text,
        args.link_url,
        args.dry_run
    )
    
    # Translate and update other languages
    print("\nTranslating to other languages...")
    for lang_code, lang_name in TARGET_LANGUAGES.items():
        print(f"\nTranslating to {lang_name} ({lang_code})...")
        
        try:
            translations = translate_banner(
                client,
                args.message,
                args.link_text,
                lang_code,
                lang_name
            )
            
            translated_message = translations.get("banner_message", args.message)
            translated_link_text = translations.get("banner_link_text", args.link_text)
            
            lang_file = I18N_DIR / f"{lang_code}.toml"
            update_i18n_file(
                lang_file,
                translated_message,
                translated_link_text,
                args.link_url,  # URL stays the same
                args.dry_run
            )
            
        except Exception as e:
            print(f"  Error translating to {lang_name}: {e}")
            # Fall back to English
            lang_file = I18N_DIR / f"{lang_code}.toml"
            update_i18n_file(
                lang_file,
                args.message,
                args.link_text,
                args.link_url,
                args.dry_run
            )
    
    # Increment banner ID
    if not args.no_increment:
        print("\nUpdating banner ID in hugo.toml...")
        increment_banner_id(args.dry_run)
    
    print("\n✓ Banner update complete!")
    if args.dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()


