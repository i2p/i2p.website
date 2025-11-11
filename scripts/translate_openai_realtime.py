#!/usr/bin/env python3
"""Translate Hugo markdown and HTML files using OpenAI API with real-time results.

This script uses the OpenAI API directly (not batch) for fast translation
suitable for CI/CD pipelines. Use translate_openai_batch.py for mass
translations when you can wait for batch processing (1-12 hours).

For HTML files like papers.html that contain academic/data content:
- The HTML file is COPIED (not translated) to maintain structure
- UI elements are translated via layout templates with i18n
- This keeps academic content in original language (standard practice)

Example usage:
    # Translate a single markdown file
    python3 translate_openai_realtime.py \
        --source content/en/blog/2025-10-16-new-i2p-routers.md \
        --target-lang de \
        --model gpt-4o-mini

    # Translate multiple files in a directory
    python3 translate_openai_realtime.py \
        --source-dir content/en/blog \
        --pattern "2025-*.md" \
        --target-lang de \
        --model gpt-4o-mini

    # Copy HTML data files (like papers.html)
    python3 translate_openai_realtime.py \
        --source content/en/papers.html \
        --target-lang de \
        --copy-html

Environment:
    OPENAI_API_KEY (required)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)

TRANSLATION_HASHES_FILE = Path(__file__).resolve().parent / "translation_hashes.json"
TRANSLATION_LOG = Path(__file__).resolve().parent / "translation_log.json"

# Target languages for translation (can be modified as needed)
TARGET_LANGUAGES = ["zh", "es", "ko", "ru", "cs", "de", "fr", "tr", "vi", "hi", "ar", "pt"]

# Front matter keys that should NOT be translated
NO_TRANSLATE_KEYS = {
    "aliases", "layout", "slug", "lastUpdated", "accurateFor",
    "reviewStatus", "date", "author", "categories", "tags",
    "toc", "weight", "draft"
}

SYSTEM_PROMPT = """You are a professional technical translator with deep familiarity with internet privacy technologies, I2P (The Invisible Internet Project), and network terminology.

Your task is to translate text segments into the target language while preserving precise meaning, tone, and context.

CRITICAL RULES:
1. Do NOT translate or modify: code blocks, commands, configuration examples, URLs, file paths, variable names, JSON/YAML structures, Markdown syntax
2. Keep I2P technical terms in English: router, tunnel, leaseSet, netDb, floodfill, NTCP2, SSU, SAMv3, I2PTunnel, I2CP, I2NP, eepsite, garlic encryption
3. Preserve ALL Markdown formatting exactly (headings, lists, links, inline code with backticks)
4. Translate idioms and expressions naturally - prefer meaning over literal translation
5. For technical terms without perfect equivalents, keep English term + add localized explanation in parentheses (only once per document)
6. Sound human, fluent, and professional - as if written by a bilingual technical writer
7. NEVER invent content - if unclear, return the original text unchanged

Context: These are official I2P documentation pages for a technical audience. Maintain consistency with standard I2P terminology."""


@dataclass
class FrontMatterEntry:
    key: str
    raw_value: str
    quote: Optional[str]
    text: str
    translated: Optional[str] = None

    def formatted(self) -> str:
        value = self.translated if self.translated is not None else self.text
        quote = self.quote
        if quote == '"':
            escaped = value.replace('"', '\\"')
            return f'{self.key}: "{escaped}"'
        if quote == "'":
            escaped = value.replace("'", "''")
            return f"{self.key}: '{escaped}'"
        return f"{self.key}: {value}"


@dataclass
class Token:
    type: str  # heading, paragraph, blank, list, code
    text: str = ""
    level: int = 0
    lines: List[str] = field(default_factory=list)
    translated: Optional[str] = None

    def render(self) -> str:
        if self.type == "blank":
            return ""
        if self.type == "heading":
            content = self.translated if self.translated is not None else self.text
            prefix = "#" * self.level
            return f"{prefix} {content}".rstrip()
        if self.type == "paragraph":
            content = self.translated if self.translated is not None else self.text
            return content.strip()
        if self.type in ("list", "code"):
            return "\n".join(self.lines)
        return self.text


class OpenAITranslator:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def translate(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """Translate a text segment using OpenAI API."""

        # Language name mapping
        lang_names = {
            "en": "English", "es": "Spanish", "de": "German", "ko": "Korean",
            "fr": "French", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
            "ja": "Japanese", "zh": "Chinese", "cs": "Czech", "tr": "Turkish",
            "vi": "Vietnamese", "hi": "Hindi", "ar": "Arabic"
        }

        target_lang_name = lang_names.get(target_lang.lower(), target_lang)
        source_lang_name = lang_names.get(source_lang.lower(), source_lang)

        user_prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}.

Follow all formatting and technical term rules from the system message.

Text to translate:
{text}

Provide ONLY the translation, nothing else:"""

        try:
            # GPT-5 only supports default temperature (1), other models support 0.2
            api_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
            }

            # Only add temperature/top_p for non-GPT-5 models
            if not self.model.startswith("gpt-5"):
                api_params["temperature"] = 0.2
                api_params["top_p"] = 0.9

            response = self.client.chat.completions.create(**api_params)

            translated = response.choices[0].message.content.strip()
            
            # Clean up common artifacts from translation output
            if translated.startswith("Translation:"):
                translated = translated[12:].strip()
            if translated.startswith("Übersetzung:"):
                translated = translated[12:].strip()
            
            return translated

        except Exception as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file content."""
    content = file_path.read_text(encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_translation_hashes() -> Dict[str, str]:
    """Load translation hashes from JSON file."""
    if not TRANSLATION_HASHES_FILE.exists():
        return {}
    
    try:
        data = json.loads(TRANSLATION_HASHES_FILE.read_text(encoding="utf-8"))
        return data.get("hashes", {})
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_translation_hashes(hashes: Dict[str, str]) -> None:
    """Save translation hashes to JSON file."""
    data = {"hashes": hashes}
    TRANSLATION_HASHES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def get_files_to_translate(files: List[Path], base_dir: Optional[Path] = None) -> List[Path]:
    """Compare file hashes and return list of files that need translation.

    Args:
        files: List of file paths to check
        base_dir: Base directory for relative paths in hash file (default: current working directory)

    Returns:
        List of files that are new or have changed (hash differs)
    """
    stored_hashes = load_translation_hashes()
    files_to_translate = []

    if base_dir is None:
        base_dir = Path.cwd()

    print(f"DEBUG get_files_to_translate: base_dir={base_dir}", file=sys.stderr)
    print(f"DEBUG get_files_to_translate: stored_hashes keys={list(stored_hashes.keys())}", file=sys.stderr)

    for file_path in files:
        if not file_path.exists():
            print(f"DEBUG: File does not exist: {file_path}", file=sys.stderr)
            continue

        # Calculate relative path from base_dir for consistency
        try:
            rel_path = file_path.relative_to(base_dir)
        except ValueError:
            # If file is not under base_dir, use absolute path
            rel_path = file_path
            print(f"DEBUG: Could not make relative path for {file_path}, using absolute", file=sys.stderr)

        rel_path_str = str(rel_path).replace("\\", "/")  # Normalize path separators

        current_hash = calculate_file_hash(file_path)
        stored_hash = stored_hashes.get(rel_path_str)

        print(f"DEBUG: Checking {rel_path_str}", file=sys.stderr)
        print(f"DEBUG:   current_hash={current_hash[:16]}...", file=sys.stderr)
        print(f"DEBUG:   stored_hash={stored_hash[:16] if stored_hash else 'None'}...", file=sys.stderr)

        if stored_hash is None:
            # New file
            print(f"DEBUG:   -> NEW FILE, will translate", file=sys.stderr)
            files_to_translate.append(file_path)
        elif stored_hash != current_hash:
            # File has changed
            print(f"DEBUG:   -> CHANGED FILE, will translate", file=sys.stderr)
            files_to_translate.append(file_path)
        else:
            print(f"DEBUG:   -> UNCHANGED, skipping", file=sys.stderr)

    return files_to_translate


def update_translation_hashes(files: List[Path], base_dir: Optional[Path] = None) -> None:
    """Update translation hashes for successfully translated files.
    
    Args:
        files: List of file paths to update hashes for
        base_dir: Base directory for relative paths in hash file (default: current working directory)
    """
    stored_hashes = load_translation_hashes()
    
    if base_dir is None:
        base_dir = Path.cwd()
    
    for file_path in files:
        if not file_path.exists():
            continue
        
        # Calculate relative path from base_dir for consistency
        try:
            rel_path = file_path.relative_to(base_dir)
        except ValueError:
            # If file is not under base_dir, use absolute path
            rel_path = file_path
        
        rel_path_str = str(rel_path).replace("\\", "/")  # Normalize path separators
        current_hash = calculate_file_hash(file_path)
        stored_hashes[rel_path_str] = current_hash
    
    save_translation_hashes(stored_hashes)


def split_front_matter(text: str) -> tuple[List[FrontMatterEntry], str]:
    """Parse YAML front matter from markdown content."""
    if not text.startswith("---"):
        return [], text

    lines = text.splitlines()
    if len(lines) < 3:
        return [], text

    fm_lines: List[str] = []
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break
        fm_lines.append(lines[idx])

    if end_index is None:
        return [], text

    entries: List[FrontMatterEntry] = []
    for raw in fm_lines:
        if not raw.strip():
            continue

        if ":" not in raw:
            continue

        key, _, raw_value = raw.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()

        quote = None
        text = raw_value
        if raw_value.startswith('"') and raw_value.endswith('"'):
            quote = '"'
            text = raw_value[1:-1].replace('\\"', '"')
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            quote = "'"
            text = raw_value[1:-1].replace("''", "'")

        entries.append(FrontMatterEntry(key=key, raw_value=raw_value, quote=quote, text=text))

    body = "\n".join(lines[end_index + 1:])
    return entries, body


def tokenize_markdown(text: str) -> List[Token]:
    """Split markdown body into translatable tokens."""
    lines = text.splitlines()
    tokens: List[Token] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            tokens.append(Token(type="blank"))
            i += 1
            continue

        # Code block
        if line.strip().startswith("```"):
            code_lines = [line]
            i += 1
            while i < len(lines):
                code_lines.append(lines[i])
                if lines[i].strip().startswith("```"):
                    i += 1
                    break
                i += 1
            tokens.append(Token(type="code", lines=code_lines))
            continue

        # Heading
        if line.startswith("#"):
            level = 0
            for ch in line:
                if ch == "#":
                    level += 1
                else:
                    break
            text = line[level:].strip()
            tokens.append(Token(type="heading", text=text, level=level))
            i += 1
            continue

        # List items
        if line.lstrip().startswith(("- ", "* ", "+ ")) or (line.lstrip()[:1].isdigit() and ". " in line[:4]):
            list_lines = []
            while i < len(lines) and (
                lines[i].lstrip().startswith(("- ", "* ", "+ ")) or
                (lines[i].lstrip()[:1].isdigit() and ". " in lines[i][:4]) or
                (lines[i].startswith("  ") and lines[i].strip())
            ):
                list_lines.append(lines[i])
                i += 1
            tokens.append(Token(type="list", lines=list_lines))
            continue

        # Paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].strip().startswith("```"):
            para_lines.append(lines[i])
            i += 1
        tokens.append(Token(type="paragraph", text=" ".join(para_lines)))

    return tokens


def reconstruct_markdown(fm_entries: List[FrontMatterEntry], tokens: List[Token]) -> str:
    """Rebuild markdown file from translated components."""
    output_lines = ["---"]
    for entry in fm_entries:
        output_lines.append(entry.formatted())
    output_lines.append("---")
    output_lines.append("")

    for token in tokens:
        if token.type == "code":
            output_lines.extend(token.lines)
        else:
            rendered = token.render()
            if rendered:
                output_lines.append(rendered)
            if token.type in ("paragraph", "heading", "list"):
                output_lines.append("")

    return "\n".join(output_lines)


def copy_html_file(
    source_path: Path,
    target_lang: str,
    output_root: Path,
    source_lang: str = "en",
    dry_run: bool = False,
    overwrite: bool = False,
    verbose: bool = True
) -> bool:
    """Copy an HTML file without translation (for data files like papers.html).

    Returns:
        True if copy was successful, False otherwise
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"Copying HTML file (no translation)")
        print(f"Source: {source_path}")
        print(f"Target language: {target_lang.upper()}")
        print(f"{'='*60}\n")

    try:
        content = source_path.read_text(encoding="utf-8")

        # Determine output path
        rel_path = source_path.relative_to(output_root / "content" / source_lang)
        output_path = output_root / "content" / target_lang / rel_path

        if dry_run:
            if verbose:
                print(f"\n[DRY RUN] Would copy to: {output_path}")
            return True

        # Check if file exists
        if output_path.exists() and not overwrite:
            if verbose:
                print(f"\n⚠️  File exists: {output_path}")
                print("   Skipping (use --overwrite to replace)")
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        if verbose:
            print(f"\n✅ HTML file copied to: {output_path}")

        return True

    except Exception as exc:
        print(f"\n❌ Error copying {source_path}: {exc}", file=sys.stderr)
        import traceback
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return False


def translate_file(
    source_path: Path,
    target_lang: str,
    translator: OpenAITranslator,
    output_root: Path,
    source_lang: str = "en",
    dry_run: bool = False,
    overwrite: bool = False,
    verbose: bool = True,
    copy_html: bool = False
) -> bool:
    """Translate a single markdown file or copy an HTML file.

    Returns:
        True if translation/copy was successful, False otherwise
    """
    # Handle HTML files
    if source_path.suffix.lower() == '.html':
        if copy_html:
            return copy_html_file(
                source_path=source_path,
                target_lang=target_lang,
                output_root=output_root,
                source_lang=source_lang,
                dry_run=dry_run,
                overwrite=overwrite,
                verbose=verbose
            )
        else:
            if verbose:
                print(f"\n⚠️  Skipping HTML file: {source_path}")
                print("   Use --copy-html to copy HTML files without translation")
            return False

    # Handle markdown files
    if verbose:
        print(f"\n{'='*60}")
        print(f"Source: {source_path}")
        print(f"Target language: {target_lang.upper()}")
        print(f"Model: {translator.model}")
        print(f"{'='*60}\n")

    try:
        content = source_path.read_text(encoding="utf-8")
        fm_entries, body = split_front_matter(content)
        tokens = tokenize_markdown(body)

        # Build list of translatable segments
        segments = []
        for entry in fm_entries:
            if entry.key not in NO_TRANSLATE_KEYS:
                segments.append(("frontmatter", entry))
        
        for token in tokens:
            if token.type in ("heading", "paragraph"):
                segments.append(("token", token))

        if verbose:
            print(f"Translating {len(segments)} segments -> {target_lang.upper()}\n")

        # Translate segments
        for idx, (seg_type, seg) in enumerate(segments, start=1):
            if seg_type == "frontmatter":
                entry = seg
                if verbose:
                    print(f"[{idx}/{len(segments)}] frontmatter:{entry.key}: {entry.text[:60]!r}")
                translated = translator.translate(entry.text, target_lang, source_lang)
                entry.translated = translated
                if verbose:
                    print(f"  → {translated[:60]!r}\n")
            elif seg_type == "token":
                token = seg
                label = f"{token.type}:{token.text[:30]}"
                if verbose:
                    print(f"[{idx}/{len(segments)}] {label}: {token.text[:60]!r}")
                translated = translator.translate(token.text, target_lang, source_lang)
                token.translated = translated
                if verbose:
                    print(f"  → {translated[:60]!r}\n")

        output_text = reconstruct_markdown(fm_entries, tokens)

        # Determine output path
        rel_path = source_path.relative_to(output_root / "content" / source_lang)
        output_path = output_root / "content" / target_lang / rel_path

        if dry_run:
            if verbose:
                print(f"\n[DRY RUN] Would write to: {output_path}")
                print(f"\nPreview (first 500 chars):\n{output_text[:500]}\n")
            return True

        # Check if file exists
        if output_path.exists() and not overwrite:
            if verbose:
                print(f"\n⚠️  File exists: {output_path}")
                print("   Skipping (use --overwrite to replace)")
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
        
        if verbose:
            print(f"\n✅ Translated file written to: {output_path}")

        # Log the translation
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": str(source_path),
            "target": str(output_path),
            "source_lang": source_lang,
            "target_lang": target_lang,
            "model": translator.model,
            "segments": len(segments)
        }

        if TRANSLATION_LOG.exists():
            try:
                log_data = json.loads(TRANSLATION_LOG.read_text(encoding="utf-8"))
                # Ensure log_data is a list, not a dict
                if not isinstance(log_data, list):
                    print(f"Warning: Translation log was not a list, resetting to empty list", file=sys.stderr)
                    log_data = []
            except (json.JSONDecodeError, FileNotFoundError):
                log_data = []
        else:
            log_data = []

        log_data.append(log_entry)
        TRANSLATION_LOG.write_text(json.dumps(log_data, indent=2, ensure_ascii=False), encoding="utf-8")

        return True

    except Exception as exc:
        # Always print errors to stderr, even in quiet mode
        print(f"\n❌ Error translating {source_path}: {exc}", file=sys.stderr)
        import traceback
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return False


def main() -> int:
    print("DEBUG: Script starting", file=sys.stderr)

    try:
        parser = argparse.ArgumentParser(description="Translate Hugo markdown using OpenAI API (realtime)")

        # File selection
        file_group = parser.add_mutually_exclusive_group(required=True)
        file_group.add_argument("--source", help="Source markdown file path (for single file)")
        file_group.add_argument("--source-dir", help="Source directory (for multiple files)")

        parser.add_argument("--pattern", help="File pattern for source-dir (e.g., '2025-*.md')")
        parser.add_argument("--target-lang", required=True, help="Target language code (e.g., de, ko, es)")
        parser.add_argument("--source-lang", default="en", help="Source language code (default: en)")
        parser.add_argument("--model", default="gpt-5", help="OpenAI model (default: gpt-5)")
        parser.add_argument("--output-root", help="Output root directory (default: auto-detect)")
        parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
        parser.add_argument("--overwrite", action="store_true", help="Overwrite existing translated files")
        parser.add_argument("--check-hashes", action="store_true", default=True, help="Only translate files that changed (default: True)")
        parser.add_argument("--no-check-hashes", dest="check_hashes", action="store_false", help="Translate all files regardless of hash")
        parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
        parser.add_argument("--update-hashes", action="store_true", default=True, help="Update translation hashes after successful translation (default: True)")
        parser.add_argument("--no-update-hashes", dest="update_hashes", action="store_false", help="Don't update translation hashes")
        parser.add_argument("--copy-html", action="store_true", help="Copy HTML files without translation (for data files like papers.html)")

        print("DEBUG: Parsing arguments", file=sys.stderr)
        args = parser.parse_args()
        print(f"DEBUG: Args parsed successfully: source={args.source}, target_lang={args.target_lang}", file=sys.stderr)
    except Exception as exc:
        print(f"FATAL ERROR during argument parsing: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is required", file=sys.stderr)
        return 1

    # Collect files
    files = []
    try:
        if args.source:
            source_path = Path(args.source).resolve()
            if not source_path.exists():
                print(f"Error: File not found: {source_path}", file=sys.stderr)
                return 1
            if not source_path.is_file():
                print(f"Error: Source path is not a file: {source_path}", file=sys.stderr)
                return 1
            files.append(source_path)
        elif args.source_dir:
            source_dir = Path(args.source_dir).resolve()
            if not source_dir.exists():
                print(f"Error: Directory not found: {source_dir}", file=sys.stderr)
                return 1
            if not source_dir.is_dir():
                print(f"Error: Source path is not a directory: {source_dir}", file=sys.stderr)
                return 1

            pattern = args.pattern or "*.md"
            files = sorted(source_dir.glob(pattern))

            if not files:
                print(f"Error: No files matching pattern '{pattern}' in {source_dir}", file=sys.stderr)
                return 1
    except Exception as exc:
        print(f"Error collecting files: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1

    # Filter by hash if requested
    if args.check_hashes and not args.dry_run:
        base_dir = files[0].parent.parent.parent if files else Path.cwd()
        print(f"DEBUG: Hash checking enabled", file=sys.stderr)
        print(f"DEBUG: base_dir = {base_dir}", file=sys.stderr)
        print(f"DEBUG: files[0] = {files[0]}", file=sys.stderr)
        print(f"DEBUG: files[0].parent.parent.parent = {files[0].parent.parent.parent}", file=sys.stderr)

        original_count = len(files)
        files = get_files_to_translate(files, base_dir=base_dir)

        print(f"DEBUG: Original file count: {original_count}", file=sys.stderr)
        print(f"DEBUG: After hash filter: {len(files)}", file=sys.stderr)

        if not files:
            if not args.quiet:
                print("No files need translation (all files already translated)")
            else:
                # In quiet mode, still log to stderr if files were filtered
                print("No files need translation (all files already translated)", file=sys.stderr)
            return 0
        if len(files) < original_count:
            if not args.quiet:
                print(f"Filtered {original_count - len(files)} file(s) that don't need translation")
            else:
                print(f"Filtered {original_count - len(files)} file(s) that don't need translation", file=sys.stderr)

    # Auto-detect output root
    try:
        if args.output_root:
            output_root = Path(args.output_root).resolve()
        else:
            parts = files[0].parts
            try:
                content_idx = parts.index("content")
                output_root = Path(*parts[:content_idx])
            except ValueError:
                print("Error: Could not auto-detect output root. Use --output-root", file=sys.stderr)
                print(f"  File path: {files[0]}", file=sys.stderr)
                return 1
    except Exception as exc:
        print(f"Error determining output root: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1

    try:
        translator = OpenAITranslator(api_key=api_key, model=args.model)
    except Exception as exc:
        print(f"Error initializing translator: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"\n{'='*60}")
        print(f"Real-time Translation")
        print(f"{'='*60}")
        print(f"Files: {len(files)}")
        print(f"Target language: {args.target_lang.upper()}")
        print(f"Model: {args.model}")
        print(f"{'='*60}\n")

    # Translate files
    successful = []
    failed = []

    for file_path in files:
        success = translate_file(
            source_path=file_path,
            target_lang=args.target_lang,
            translator=translator,
            output_root=output_root,
            source_lang=args.source_lang,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
            verbose=not args.quiet,
            copy_html=args.copy_html
        )
        
        if success:
            successful.append(file_path)
        else:
            failed.append(file_path)

    # Update hashes for successfully translated files
    if args.update_hashes and successful and not args.dry_run:
        base_dir = output_root if args.output_root else Path.cwd()
        update_translation_hashes(successful, base_dir=base_dir)

    # Summary
    if not args.quiet:
        print(f"\n{'='*60}")
        print(f"Summary")
        print(f"{'='*60}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        if failed:
            print(f"\nFailed files:")
            for f in failed:
                print(f"  - {f}")
        print()

    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FATAL UNCAUGHT EXCEPTION: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

