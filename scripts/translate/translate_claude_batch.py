#!/usr/bin/env python3
"""Translate Hugo markdown files using OpenAI Batch API for cost savings.

The Batch API provides 50% cost reduction compared to regular API calls,
with a 24-hour completion window. Perfect for bulk translation jobs.

Example usage:
    # Submit a batch job
    python3 translate_claude_batch.py --submit \
        --source ../content/en/blog/2025-10-16-new-i2p-routers.md \
        --target-lang de \
        --model gpt-4.1-mini

    # Check batch status
    python3 translate_claude_batch.py --check batch_abc123

    # Wait for completion and process results
    python3 translate_claude_batch.py --check batch_abc123 --wait

    # List all batches
    python3 translate_claude_batch.py --list

Environment:
    OPENAI_API_KEY (required)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import tempfile
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)

# === COMMENTED OUT CLAUDE IMPORTS ===
# try:
#     import anthropic
# except ImportError:
#     print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
#     sys.exit(1)

BATCH_STATE_FILE = Path(__file__).resolve().parent / "claude_batch_state.json"
TRANSLATION_HASHES_FILE = Path(__file__).resolve().parent / "claude_translation_hashes.json"

# Target languages for translation (can be modified as needed)
TARGET_LANGUAGES = ["zh", "es", "ko", "ru", "cs", "de", "fr", "tr", "vi", "hi", "ar", "pt"]

# Front matter keys that should NOT be translated
NO_TRANSLATE_KEYS = {
    "aliases", "layout", "slug", "lastUpdated", "lastupdated", "accurateFor",
    "reviewStatus", "date", "author", "categories", "tags",
    "toc", "weight", "draft", "number", "created", "thread", "supercedes",
    "supersedes", "supersededby", "updated", "type"
}

SYSTEM_PROMPT = """You are a professional technical translator specializing in I2P (The Invisible Internet Project) documentation.

INSTRUCTIONS:
1. Translate the input text inside <source_text> tags to {target_lang}.
2. Output ONLY the translated text wrapped in <translation> tags.
3. Do not include any other text, preambles, or explanations.

TRANSLATION RULES:
1. Keep untranslated: code blocks, commands, URLs, file paths, variable names, JSON/YAML, Markdown syntax
2. Keep I2P terms in English: router, tunnel, leaseSet, netDb, floodfill, NTCP2, SSU, SAMv3, I2PTunnel, I2CP, I2NP, eepsite, garlic encryption
3. Preserve ALL Markdown formatting exactly (headings, lists, links, inline code)
4. Translate naturally for meaning, not literally
5. For technical terms without equivalents: keep English + add localized explanation in parentheses (once per document)

EXAMPLE INPUT:
<source_text>
Hello world
</source_text>

EXAMPLE OUTPUT:
<translation>
Hola mundo
</translation>
"""

# Patterns that indicate the model included instruction text in its output
# These are common across many languages
ARTIFACT_PATTERNS = [
    # English instruction artifacts
    r"^IMPORTANT:.*(?:translation|Translation|provide|Provide).*$",
    r"^Provide ONLY.*translation.*$",
    r"^Do NOT ask questions.*$",
    r"^Even if the text.*translate.*$",
    r"^Translation:$",
    r"^Translated text:$",
    r"^I don't see any text to translate.*$",
    r"^I notice that you haven't included.*$",
    r"^Please provide the.*text.*translate.*$",
    r"^The section marked.*appears to be empty.*$",
    r"^You've provided the instructions but not.*$",
    r"^I will translate.*$",
    r"^I'll translate.*$",
    r"^Sure, I will translate.*$",
    r"^Sure, I'll translate.*$",
    r"^I will provide only the translation.*$",
    r"^I'll provide only the translation.*$",

    # Chinese artifacts
    r"^我会直接提供翻译.*$",
    r"^请提供需要翻译的.*$",
    r"^我没有看到需要翻译的文本.*$",
    r"^IMPORTANT:.*仅提供翻译.*$",
    r"^只提供翻译.*$",
    r"^翻译如下.*$",
    r"^这是翻译.*$",
    r"^以下是翻译.*$",

    # Korean artifacts
    r"^IMPORTANT:.*번역만 제공.*$",
    r"^번역만 제공.*$",
    r"^이 텍스트에는 번역할 내용이 없습니다.*$",
    r"^번역:?$",
    r"^다음은 번역입니다.*$",

    # Arabic artifacts
    r"^مهم:.*لا تطرح أسئلة.*$",
    r"^مهم:.*قم بترجمته كما هو.*$",
    r"^قدم الترجمة فقط.*$",
    r"^الترجمة:?$",
    r"^هذه هي الترجمة.*$",

    # Turkish artifacts
    r"^ÖNEMLİ:.*YALNIZCA çeviriyi.*$",
    r"^ÖNEMLI:.*YALNIZCA çeviriyi.*$",
    r"^SADECE çeviriyi.*$",
    r"^Çeviri:?$",
    r"^İşte çeviri.*$",

    # Spanish artifacts
    r"^IMPORTANTE:.*proporcione ÚNICAMENTE.*$",
    r"^Proporcione ÚNICAMENTE.*$",
    r"^Aquí está la traducción:?$",
    r"^No veo ningún texto para traducir.*$",

    # French artifacts
    r"^IMPORTANT:.*Fournissez UNIQUEMENT.*$",
    r"^Fournissez UNIQUEMENT.*$",
    r"^Voici la traduction:?$",
    r"^Je ne vois pas de texte à traduire.*$",

    # German artifacts
    r"^WICHTIG:.*Geben Sie NUR.*$",
    r"^Geben Sie NUR.*$",
    r"^Hier ist die Übersetzung:?$",
    r"^Ich sehe keinen Text zum Übersetzen.*$",

    # Russian artifacts
    r"^ВАЖНО:.*Предоставьте ТОЛЬКО.*$",
    r"^Предоставьте ТОЛЬКО.*$",
    r"^Вот перевод:?$",
    r"^Я не вижу текста для перевода.*$",

    # Portuguese artifacts
    r"^IMPORTANTE:.*Forneça APENAS.*$",
    r"^Forneça APENAS.*$",
    r"^Tradução:?$",
    r"^Aqui está a tradução.*$",

    # Vietnamese artifacts
    r"^QUAN TRỌNG:.*Chỉ cung cấp.*$",
    r"^Chỉ cung cấp.*$",
    r"^Bản dịch:?$",
    r"^Đây là bản dịch.*$",

    # Hindi artifacts
    r"^महत्वपूर्ण:.*केवल अनुवाद.*$",
    r"^केवल अनुवाद.*$",
    r"^अनुवाद:?$",
    r"^यहाँ अनुवाद है.*$",

    # Czech artifacts
    r"^DŮLEŽITÉ:.*překlad.*$",
    r"^Poskytněte POUZE.*$",
    r"^Překlad:?$",
    r"^Zde je překlad.*$",

    # General prompt echoing patterns
    r"^Translate the following.*$",
    r"^Text to translate:?$",
    r"^Follow all formatting.*$",
    r"^\[English →.*\]$",
    r"^\[.*→.*\]$",  # Language direction markers
]


def clean_translation_artifacts(text: str) -> str:
    """Extract translation from XML tags or clean up artifacts."""
    import re

    # 1. Try to extract content from <translation> tags
    match = re.search(r'<translation>\s*(.*?)\s*</translation>', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 2. Fallback: Clean up artifacts using regex patterns
    # This handles legacy batches or cases where model forgot tags
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        skip_line = False
        stripped = line.strip()

        # Check against artifact patterns
        for pattern in ARTIFACT_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                skip_line = True
                break

        # Also check for common prefixes that indicate meta-commentary
        if not skip_line:
            lower = stripped.lower()

            # Meta-commentary prefixes to skip entirely
            skip_prefixes = [
                "translation:", "übersetzung:", "traducción:", "traduction:",
                "tradução:", "перевод:", "翻译:", "번역:", "çeviri:", "překlad:",
                "here is", "below is", "aquí está", "voici", "hier ist",
                "i don't see", "i notice", "please provide", "you've provided",
                "i will translate", "i'll translate", "sure, i",
            ]

            for prefix in skip_prefixes:
                if lower.startswith(prefix):
                    # For "translation:" style, try to extract remainder
                    if ":" in prefix and ":" in stripped:
                        remainder = stripped.split(":", 1)[1].strip()
                        if remainder and len(remainder) > 20:  # Only keep if substantial
                            cleaned_lines.append(remainder)
                    skip_line = True
                    break

            # Also check for lines that look like instruction artifacts
            if not skip_line:
                # Lines that start with common instruction phrases
                instruction_markers = [
                    "important:", "note:", "注意:", "주의:", "ملاحظة:",
                    "önemli:", "importante:", "remarque:", "hinweis:",
                ]
                for marker in instruction_markers:
                    if lower.startswith(marker) and any(kw in lower for kw in ["translat", "provid", "翻译", "번역", "ترجم"]):
                        skip_line = True
                        break

        if not skip_line:
            cleaned_lines.append(line)

    result = '\n'.join(cleaned_lines).strip()

    # Remove any stray tags if regex failed to capture full block
    result = result.replace("<translation>", "").replace("</translation>", "").strip()

    # Clean up multiple consecutive blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result


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
        if self.type in ("list", "code", "table"):
            return "\n".join(self.lines)
        return self.text


@dataclass
class SegmentMapping:
    """Maps a segment to its position in the file for reconstruction."""
    custom_id: str
    type: str  # frontmatter, heading, paragraph
    key: Optional[str] = None  # For frontmatter
    level: Optional[int] = None  # For headings


@dataclass
class FileMapping:
    """Maps a source file to its segments and target location."""
    source_path: str
    target_path: str
    segments: List[SegmentMapping] = field(default_factory=list)


@dataclass
class BatchJobState:
    """State of a batch translation job."""
    id: str
    status: str
    model: str
    created_at: str
    target_lang: str
    source_lang: str
    completed_at: Optional[str] = None
    files: List[FileMapping] = field(default_factory=list)
    error_count: int = 0
    total_requests: int = 0
    input_file_id: Optional[str] = None  # OpenAI file ID for batch input


def load_batch_state() -> Dict[str, BatchJobState]:
    """Load batch state from JSON file."""
    if not BATCH_STATE_FILE.exists():
        return {}

    data = json.loads(BATCH_STATE_FILE.read_text(encoding="utf-8"))
    batches = {}
    for batch_id, batch_data in data.get("batches", {}).items():
        # Reconstruct FileMapping objects
        files = []
        for f in batch_data.get("files", []):
            segments = [SegmentMapping(**s) for s in f.get("segments", [])]
            files.append(FileMapping(
                source_path=f["source_path"],
                target_path=f["target_path"],
                segments=segments
            ))

        batch_data["files"] = files
        batches[batch_id] = BatchJobState(**batch_data)

    return batches


def save_batch_state(batches: Dict[str, BatchJobState]) -> None:
    """Save batch state to JSON file."""
    data = {"batches": {}}
    for batch_id, batch in batches.items():
        batch_dict = asdict(batch)
        data["batches"][batch_id] = batch_dict

    BATCH_STATE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


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
        stored_hash = stored_hashes.get(rel_path_str)

        if stored_hash is None:
            # New file
            files_to_translate.append(file_path)
        elif stored_hash != current_hash:
            # File has changed
            files_to_translate.append(file_path)

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

        # Code block (fenced with ```)
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

        # Markdown table (lines starting with |)
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            tokens.append(Token(type="table", lines=table_lines))
            continue

        # HTML block (table, div, details, etc.) - DO NOT translate
        # HTML tables get corrupted if sent for translation
        stripped = line.strip().lower()
        if stripped.startswith("<table") or stripped.startswith("<div") or stripped.startswith("<details") or stripped.startswith("<figure"):
            html_lines = []
            tag_name = stripped.split()[0][1:].rstrip(">")  # Extract tag name

            depth = 0
            while i < len(lines):
                current = lines[i]
                html_lines.append(current)
                current_lower = current.strip().lower()

                # Count opening and closing tags
                if f"<{tag_name}" in current_lower:
                    depth += current_lower.count(f"<{tag_name}")
                if f"</{tag_name}" in current_lower:
                    depth -= current_lower.count(f"</{tag_name}")

                i += 1

                if depth <= 0:
                    break

            tokens.append(Token(type="code", lines=html_lines))  # Treat as code (no translation)
            continue

        # Indented code block (4+ spaces or tab at start of line)
        # This handles RST-style code blocks and indented code in markdown
        # Markdown spec: code blocks are lines indented with 4+ spaces or a tab
        if (line.startswith("    ") or line.startswith("\t")) and line.strip():
            code_lines = []
            # Collect all consecutive indented lines (4+ spaces or tab)
            # Include blank lines that are also indented (they're part of the code block)
            while i < len(lines):
                current_line = lines[i]
                # Continue if line is indented with 4+ spaces or tab
                if (current_line.startswith("    ") or current_line.startswith("\t")):
                    code_lines.append(current_line)
                    i += 1
                # Also include blank lines that follow indented lines (they're part of code block)
                elif not current_line.strip() and code_lines:
                    code_lines.append(current_line)
                    i += 1
                else:
                    break
            # Only treat as code block if we have at least one non-blank indented line
            if code_lines and any(l.strip() for l in code_lines):
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

        # Paragraph - but stop at table rows, indented code blocks, etc.
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].strip().startswith("```") and not lines[i].strip().startswith("|"):
            # Stop if we hit an indented code block (4+ spaces or tab)
            if lines[i].startswith("    ") or lines[i].startswith("\t"):
                break
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            tokens.append(Token(type="paragraph", text=" ".join(para_lines)))

    return tokens


def generate_openai_batch_requests(
    files: List[Path],
    target_lang: str,
    source_lang: str,
    model: str,
    output_root: Path
) -> tuple[List[Dict[str, Any]], List[FileMapping], List[FrontMatterEntry], List[List[Token]]]:
    """Generate OpenAI batch API requests for all files."""

    # Language name mapping
    lang_names = {
        "en": "English", "es": "Spanish", "de": "German", "ko": "Korean",
        "fr": "French", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
        "ja": "Japanese", "zh": "Chinese", "cs": "Czech", "tr": "Turkish",
        "vi": "Vietnamese", "hi": "Hindi", "ar": "Arabic"
    }

    target_lang_name = lang_names.get(target_lang.lower(), target_lang)
    source_lang_name = lang_names.get(source_lang.lower(), source_lang)

    requests = []
    file_mappings = []
    all_fm_entries = []  # Store for reconstruction
    all_tokens = []  # Store for reconstruction

    for file_idx, source_path in enumerate(files, start=1):
        print(f"\nProcessing [{file_idx}/{len(files)}]: {source_path.name}")

        content = source_path.read_text(encoding="utf-8")
        fm_entries, body = split_front_matter(content)
        tokens = tokenize_markdown(body)

        # Store for later reconstruction
        all_fm_entries.append(fm_entries)
        all_tokens.append(tokens)

        # Determine output path
        rel_path = source_path.relative_to(output_root / "content" / source_lang)
        target_path = output_root / "content" / target_lang / rel_path

        file_mapping = FileMapping(
            source_path=str(source_path),
            target_path=str(target_path),
            segments=[]
        )

        file_prefix = f"file{file_idx:03d}"

        # Front matter segments
        for entry in fm_entries:
            if entry.key in NO_TRANSLATE_KEYS:
                continue

            custom_id = f"{file_prefix}_fm_{entry.key}"

            # User prompt with XML wrapper
            user_prompt = f"""[{source_lang_name} → {target_lang_name}]
<source_text>
{entry.text}
</source_text>"""

            # OpenAI Batch API format (JSONL line)
            request = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": model,
                    "max_completion_tokens": 4096,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)},
                        {"role": "user", "content": user_prompt}
                    ]
                }
            }

            requests.append(request)
            file_mapping.segments.append(SegmentMapping(
                custom_id=custom_id,
                type="frontmatter",
                key=entry.key
            ))

        # Body segments
        heading_counts = {}  # Count per level: {2: 0, 3: 0, 4: 0, ...}
        paragraph_count = 0
        list_count = 0
        table_count = 0

        for token in tokens:
            if token.type == "heading":
                level = token.level
                heading_counts[level] = heading_counts.get(level, 0) + 1
                custom_id = f"{file_prefix}_h{level}_{heading_counts[level]:03d}"

                user_prompt = f"""[{source_lang_name} → {target_lang_name}]
<source_text>
{token.text}
</source_text>"""

                request = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model,
                        "max_completion_tokens": 4096,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                }

                requests.append(request)
                file_mapping.segments.append(SegmentMapping(
                    custom_id=custom_id,
                    type="heading",
                    level=token.level
                ))

            elif token.type == "paragraph":
                paragraph_count += 1
                custom_id = f"{file_prefix}_p_{paragraph_count:03d}"

                user_prompt = f"""[{source_lang_name} → {target_lang_name}]
<source_text>
{token.text}
</source_text>"""

                request = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model,
                        "max_completion_tokens": 4096,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                }

                requests.append(request)
                file_mapping.segments.append(SegmentMapping(
                    custom_id=custom_id,
                    type="paragraph"
                ))

            elif token.type == "list":
                list_count += 1
                custom_id = f"{file_prefix}_list_{list_count:03d}"

                # Join list lines for translation, preserving structure
                list_text = "\n".join(token.lines)

                user_prompt = f"""[{source_lang_name} → {target_lang_name}] [list - preserve structure]
<source_text>
{list_text}
</source_text>"""

                request = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model,
                        "max_completion_tokens": 4096,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                }

                requests.append(request)
                file_mapping.segments.append(SegmentMapping(
                    custom_id=custom_id,
                    type="list"
                ))

            elif token.type == "table":
                table_count += 1
                custom_id = f"{file_prefix}_table_{table_count:03d}"

                table_text = "\n".join(token.lines)

                user_prompt = f"""[{source_lang_name} → {target_lang_name}] [table - preserve Markdown structure exactly]
<source_text>
{table_text}
</source_text>"""

                request = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model,
                        "max_completion_tokens": 4096,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                }

                requests.append(request)
                file_mapping.segments.append(SegmentMapping(
                    custom_id=custom_id,
                    type="table"
                ))

        file_mappings.append(file_mapping)
        print(f"  Generated {len(file_mapping.segments)} translation requests")

    return requests, file_mappings, all_fm_entries, all_tokens


# === COMMENTED OUT CLAUDE BATCH REQUEST GENERATOR ===
# def generate_batch_requests(
#     files: List[Path],
#     target_lang: str,
#     source_lang: str,
#     model: str,
#     output_root: Path
# ) -> tuple[List[Dict[str, Any]], List[FileMapping], List[FrontMatterEntry], List[List[Token]]]:
#     """Generate batch API requests for all files (Claude format)."""
#     # ... Claude format code ...
#     pass


def submit_batch(
    files: List[Path],
    target_lang: str,
    source_lang: str,
    model: str,
    output_root: Path,
    dry_run: bool = False
) -> Optional[str]:
    """Submit a batch translation job using OpenAI Batch API."""

    print(f"\n{'='*60}")
    print(f"Batch Translation Submission (OpenAI)")
    print(f"{'='*60}")
    print(f"Files: {len(files)}")
    print(f"Target language: {target_lang.upper()}")
    print(f"Source language: {source_lang.upper()}")
    print(f"Model: {model}")
    print(f"Dry run: {dry_run}")
    print(f"{'='*60}\n")

    # Generate requests
    requests, file_mappings, _, _ = generate_openai_batch_requests(
        files, target_lang, source_lang, model, output_root
    )

    print(f"\n✅ Generated {len(requests)} total translation requests")

    if dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - Preview of requests (first 5)")
        print(f"{'='*60}\n")
        for req in requests[:5]:
            print(json.dumps(req, indent=2, ensure_ascii=False))
            print()

        print(f"... and {len(requests) - 5} more requests")
        return None

    # Submit to OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print("\n🚀 Creating batch job...")

    try:
        # Write JSONL file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False, encoding='utf-8') as f:
            for req in requests:
                f.write(json.dumps(req, ensure_ascii=False) + '\n')
            jsonl_path = f.name

        print(f"📝 Created JSONL file: {jsonl_path}")

        # Upload file to OpenAI
        with open(jsonl_path, 'rb') as f:
            batch_file = client.files.create(
                file=f,
                purpose="batch"
            )

        print(f"📤 Uploaded file: {batch_file.id}")

        # Create batch job
        batch = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )

        print(f"✅ Batch job created: {batch.id}")
        print(f"   Status: {batch.status}")
        print(f"   Created: {batch.created_at}")

        # Clean up temp file
        os.unlink(jsonl_path)

        # Save state
        batches = load_batch_state()
        batches[batch.id] = BatchJobState(
            id=batch.id,
            status=batch.status,
            model=model,
            created_at=datetime.now(timezone.utc).isoformat(),
            target_lang=target_lang,
            source_lang=source_lang,
            files=file_mappings,
            total_requests=len(requests),
            input_file_id=batch_file.id
        )
        save_batch_state(batches)

        print(f"\n💾 State saved to: {BATCH_STATE_FILE}")
        print(f"\n📋 To check status, run:")
        print(f"   python3 {Path(__file__).name} --check {batch.id}")
        print(f"\n⏰ Batch jobs typically complete in 1-24 hours")

        return batch.id

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


# === COMMENTED OUT CLAUDE SUBMIT BATCH ===
# def submit_batch_claude(
#     files: List[Path],
#     target_lang: str,
#     source_lang: str,
#     model: str,
#     output_root: Path,
#     dry_run: bool = False
# ) -> Optional[str]:
#     """Submit a batch translation job using Claude."""
#     api_key = os.getenv("ANTHROPIC_API_KEY")
#     if not api_key:
#         print("Error: ANTHROPIC_API_KEY environment variable required", file=sys.stderr)
#         return None
#
#     client = anthropic.Anthropic(api_key=api_key)
#     # ... rest of Claude submit code ...
#     pass


def reconstruct_files(
    batch_state: BatchJobState,
    results: Dict[str, str],
    output_root: Path
) -> int:
    """Reconstruct translated markdown files from batch results."""

    files_written = 0

    for file_mapping in batch_state.files:
        source_path = Path(file_mapping.source_path)
        target_path = Path(file_mapping.target_path)

        print(f"\n  Processing: {source_path.name}")

        # Read original file
        if not source_path.exists():
            print(f"    ⚠️  Source file not found: {source_path}")
            continue

        content = source_path.read_text(encoding="utf-8")
        fm_entries, body = split_front_matter(content)
        tokens = tokenize_markdown(body)

        # Apply translations from results
        for segment in file_mapping.segments:
            if segment.custom_id not in results:
                print(f"    ⚠️  Missing translation for: {segment.custom_id}")
                continue

            translation = results[segment.custom_id]

            # Apply to front matter
            if segment.type == "frontmatter":
                for entry in fm_entries:
                    if entry.key == segment.key:
                        entry.translated = translation
                        break

            # Apply to tokens
            elif segment.type == "heading":
                heading_count = 0
                for token in tokens:
                    if token.type == "heading" and token.level == segment.level:
                        heading_count += 1
                        # Extract heading number from custom_id (e.g., "file001_h2_001" -> 1)
                        id_parts = segment.custom_id.split("_")
                        expected_num = int(id_parts[-1])
                        if heading_count == expected_num:
                            token.translated = translation
                            break

            elif segment.type == "paragraph":
                paragraph_count = 0
                for token in tokens:
                    if token.type == "paragraph":
                        paragraph_count += 1
                        # Extract paragraph number from custom_id
                        id_parts = segment.custom_id.split("_")
                        expected_num = int(id_parts[-1])
                        if paragraph_count == expected_num:
                            token.translated = translation
                            break

            elif segment.type == "list":
                list_count = 0
                for token in tokens:
                    if token.type == "list":
                        list_count += 1
                        # Extract list number from custom_id
                        id_parts = segment.custom_id.split("_")
                        expected_num = int(id_parts[-1])
                        if list_count == expected_num:
                            # Replace list lines with translated content
                            token.lines = translation.split("\n")
                            break

            elif segment.type == "table":
                table_count = 0
                for token in tokens:
                    if token.type == "table":
                        table_count += 1
                        # Extract table number from custom_id
                        id_parts = segment.custom_id.split("_")
                        expected_num = int(id_parts[-1])
                        if table_count == expected_num:
                            # Replace table lines with translated content
                            token.lines = translation.split("\n")
                            break

        # Reconstruct markdown
        output_lines = ["---"]
        for entry in fm_entries:
            output_lines.append(entry.formatted())
        output_lines.append("---")
        output_lines.append("")

        for token in tokens:
            if token.type == "code":
                output_lines.extend(token.lines)
            elif token.type == "table":
                output_lines.extend(token.lines)
            else:
                rendered = token.render()
                if rendered:
                    output_lines.append(rendered)
                if token.type in ("paragraph", "heading", "list"):
                    output_lines.append("")

        output_text = "\n".join(output_lines)

        # Write file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(output_text, encoding="utf-8")

        print(f"    ✅ Written to: {target_path}")
        files_written += 1

    return files_written


def check_batch(batch_id: str, wait: bool = False) -> None:
    """Check batch status and process results if complete (OpenAI)."""

    # Load state
    batches = load_batch_state()
    if batch_id not in batches:
        print(f"❌ Batch {batch_id} not found in state file", file=sys.stderr)
        return

    batch_state = batches[batch_id]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"\n{'='*60}")
    print(f"Batch Status: {batch_id}")
    print(f"{'='*60}\n")

    while True:
        try:
            batch = client.batches.retrieve(batch_id)

            print(f"Status: {batch.status}")
            print(f"Created: {batch.created_at}")
            print(f"Total requests: {batch_state.total_requests}")

            if batch.request_counts:
                print(f"Completed: {batch.request_counts.completed}")
                print(f"Failed: {batch.request_counts.failed}")
                print(f"Total: {batch.request_counts.total}")

            # Update state
            batch_state.status = batch.status

            if batch.status == "completed":
                print(f"\n✅ Batch completed!")

                # Download and process results
                print(f"\n📥 Downloading results...")

                results = {}
                error_count = 0

                # Get output file
                if batch.output_file_id:
                    output_content = client.files.content(batch.output_file_id)
                    output_text = output_content.text

                    for line in output_text.strip().split('\n'):
                        if not line.strip():
                            continue
                        try:
                            result = json.loads(line)
                            custom_id = result.get("custom_id")

                            if result.get("response") and result["response"].get("body"):
                                body = result["response"]["body"]
                                if body.get("choices") and len(body["choices"]) > 0:
                                    message = body["choices"][0].get("message", {})
                                    translation = message.get("content", "").strip()

                                    # Clean up translation artifacts
                                    translation = clean_translation_artifacts(translation)

                                    results[custom_id] = translation
                            elif result.get("error"):
                                print(f"⚠️  Failed: {custom_id} - {result['error']}")
                                error_count += 1
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON decode error: {e}")
                            error_count += 1

                batch_state.error_count = error_count
                print(f"\n✅ Retrieved {len(results)} translations ({error_count} errors)")

                # Reconstruct files
                print(f"\n📝 Reconstructing markdown files...")

                # Determine output root from first file
                if batch_state.files:
                    first_source = Path(batch_state.files[0].source_path)
                    parts = first_source.parts
                    try:
                        content_idx = parts.index("content")
                        output_root = Path(*parts[:content_idx])
                    except ValueError:
                        print("❌ Could not determine output root", file=sys.stderr)
                        output_root = Path.cwd()
                else:
                    output_root = Path.cwd()

                files_written = reconstruct_files(batch_state, results, output_root)

                print(f"\n✅ Reconstructed {files_written} file(s)")

                batch_state.completed_at = datetime.now(timezone.utc).isoformat()
                save_batch_state(batches)

                break

            elif batch.status in ("failed", "cancelled", "expired"):
                print(f"\n❌ Batch {batch.status}")
                if batch.errors:
                    for error in batch.errors.data[:5]:  # Show first 5 errors
                        print(f"   Error: {error.message}")
                batch_state.status = batch.status
                save_batch_state(batches)
                break

            elif wait:
                print(f"\n⏳ Waiting 60 seconds before next check...")
                time.sleep(60)
            else:
                print(f"\n💡 Use --wait to poll until completion")
                save_batch_state(batches)
                break

        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            break

    save_batch_state(batches)


# === COMMENTED OUT CLAUDE CHECK BATCH ===
# def check_batch_claude(batch_id: str, wait: bool = False) -> None:
#     """Check batch status and process results if complete (Claude)."""
#     api_key = os.getenv("ANTHROPIC_API_KEY")
#     if not api_key:
#         print("Error: ANTHROPIC_API_KEY environment variable required", file=sys.stderr)
#         return
#
#     client = anthropic.Anthropic(api_key=api_key)
#     # ... rest of Claude check code ...
#     pass


def cancel_batch(batch_id: str) -> None:
    """Cancel a batch job (OpenAI)."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        batch = client.batches.cancel(batch_id)
        print(f"✅ Batch cancellation requested: {batch_id}")
        print(f"   Status: {batch.status}")

        # Update state
        batches = load_batch_state()
        if batch_id in batches:
            batches[batch_id].status = batch.status
            save_batch_state(batches)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)


def list_batches() -> None:
    """List all batch jobs from state file."""

    batches = load_batch_state()

    if not batches:
        print("No batch jobs found")
        return

    print(f"\n{'='*80}")
    print(f"OpenAI Batch Translation Jobs")
    print(f"{'='*80}\n")

    for batch_id, batch in batches.items():
        print(f"ID: {batch_id}")
        print(f"  Status: {batch.status}")
        print(f"  Model: {batch.model}")
        print(f"  Target: {batch.target_lang.upper()}")
        print(f"  Files: {len(batch.files)}")
        print(f"  Requests: {batch.total_requests}")
        print(f"  Created: {batch.created_at}")
        if batch.completed_at:
            print(f"  Completed: {batch.completed_at}")
        print()


def check_all_batches(wait: bool = False, interval: int = 60) -> None:
    """Check status of all batch jobs at once (OpenAI)."""

    batches = load_batch_state()

    if not batches:
        print("No batch jobs found")
        return

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"\n{'='*80}")
    print(f"Batch Status Summary - {len(batches)} batch(es)")
    print(f"{'='*80}\n")

    while True:
        all_completed = True
        all_ended = True

        for batch_id, batch_state in batches.items():
            try:
                batch = client.batches.retrieve(batch_id)
                batch_state.status = batch.status

                # Print status
                status_icon = "✅" if batch.status == "completed" else "⏳" if batch.status in ("validating", "in_progress", "finalizing") else "❌"
                print(f"{status_icon} {batch_id[:20]}... | {batch_state.target_lang.upper():3s} | {batch.status:12s} | ", end="")

                if batch.request_counts:
                    print(f"Completed: {batch.request_counts.completed:4d} | Failed: {batch.request_counts.failed:4d} | Total: {batch.request_counts.total:4d}")
                else:
                    print("No request counts available")

                if batch.status not in ("completed", "failed", "cancelled", "expired"):
                    all_completed = False
                    all_ended = False
                elif batch.status == "completed":
                    all_ended = True

            except Exception as e:
                print(f"❌ {batch_id[:20]}... | Error: {e}")
                all_completed = False
                all_ended = False

        save_batch_state(batches)

        print()

        if all_completed and all_ended:
            print("✅ All batches have completed!")
            print("\nTo process results, run:")
            for batch_id in batches.keys():
                print(f"  python3 translate_claude_batch.py --check {batch_id}")
            break

        if not wait:
            print("💡 Use --wait to poll until all batches complete")
            break

        print(f"⏳ Waiting {interval} seconds before next check...")
        time.sleep(interval)
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch translate Hugo markdown using OpenAI Batch API")

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--submit", action="store_true", help="Submit a new batch job")
    mode_group.add_argument("--check", metavar="BATCH_ID", help="Check batch status and retrieve results")
    mode_group.add_argument("--check-all", action="store_true", help="Check status of all batch jobs")
    mode_group.add_argument("--cancel", metavar="BATCH_ID", help="Cancel a batch job")
    mode_group.add_argument("--list", action="store_true", help="List all batch jobs")

    # Submit options
    parser.add_argument("--source", help="Source markdown file path (for single file)")
    parser.add_argument("--source-dir", help="Source directory (for multiple files)")
    parser.add_argument("--pattern", help="File pattern for source-dir (e.g., '2025-*.md')")
    parser.add_argument("--target-lang", help="Target language code (e.g., de, ko, es)")
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en)")
    parser.add_argument("--model", default="gpt-5", help="OpenAI model (default: gpt-5)")
    parser.add_argument("--output-root", help="Output root directory (default: auto-detect)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without submitting")

    # Check options
    parser.add_argument("--wait", action="store_true", help="Poll until batch completes")

    args = parser.parse_args()

    if args.list:
        list_batches()
        return 0

    if args.check:
        check_batch(args.check, wait=args.wait)
        return 0

    if args.check_all:
        check_all_batches(wait=args.wait, interval=60)
        return 0

    if args.cancel:
        cancel_batch(args.cancel)
        return 0

    if args.submit:
        # Validate required arguments
        if not args.target_lang:
            print("Error: --target-lang required for submit mode", file=sys.stderr)
            return 1

        if not args.source and not args.source_dir:
            print("Error: --source or --source-dir required for submit mode", file=sys.stderr)
            return 1

        # Collect files
        files = []
        if args.source:
            source_path = Path(args.source).resolve()
            if not source_path.exists():
                print(f"Error: File not found: {source_path}", file=sys.stderr)
                return 1
            files.append(source_path)

        elif args.source_dir:
            source_dir = Path(args.source_dir).resolve()
            if not source_dir.exists():
                print(f"Error: Directory not found: {source_dir}", file=sys.stderr)
                return 1

            pattern = args.pattern or "*.md"
            files = sorted(source_dir.glob(pattern))

            if not files:
                print(f"Error: No files matching pattern '{pattern}' in {source_dir}", file=sys.stderr)
                return 1

        # Auto-detect output root
        if args.output_root:
            output_root = Path(args.output_root).resolve()
        else:
            parts = files[0].parts
            try:
                content_idx = parts.index("content")
                output_root = Path(*parts[:content_idx])
            except ValueError:
                print("Error: Could not auto-detect output root. Use --output-root", file=sys.stderr)
                return 1

        # Submit batch
        batch_id = submit_batch(
            files=files,
            target_lang=args.target_lang,
            source_lang=args.source_lang,
            model=args.model,
            output_root=output_root,
            dry_run=args.dry_run
        )

        if batch_id:
            return 0
        else:
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
