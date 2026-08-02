#!/usr/bin/env python3
"""Translate Hugo markdown and HTML files using Claude API with real-time results.

This script uses the Claude API directly (not batch) for fast translation
suitable for CI/CD pipelines. It incorporates all guardrails from the batch
translation script including XML tag extraction and artifact cleaning.

For HTML files like papers.html that contain academic/data content:
- The HTML file is COPIED (not translated) to maintain structure
- UI elements are translated via layout templates with i18n
- This keeps academic content in original language (standard practice)

Example usage:
    # Translate a single markdown file
    python3 translate_claude_realtime.py \
        --source content/en/blog/2025-10-16-new-i2p-routers.md \
        --target-lang de \
        --model claude-sonnet-4-20250514

    # Translate multiple files in a directory
    python3 translate_claude_realtime.py \
        --source-dir content/en/blog \
        --pattern "2025-*.md" \
        --target-lang de

    # Copy HTML data files (like papers.html)
    python3 translate_claude_realtime.py \
        --source content/en/papers.html \
        --target-lang de \
        --copy-html

Environment:
    ANTHROPIC_API_KEY (required for --provider claude)
    TOGETHER_API_KEY (required for --provider together)
    OPENROUTER_API_KEY (required for --provider openrouter)
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

import unicodedata

TRANSLATION_HASHES_FILE = Path(__file__).resolve().parent / "claude_translation_hashes.json"
TRANSLATION_LOG = Path(__file__).resolve().parent / "claude_translation_log.json"
SEGMENT_CACHE_FILE = Path(__file__).resolve().parent / "claude_segment_cache.json"

# Target languages for translation (can be modified as needed)
TARGET_LANGUAGES = ["zh", "es", "ko", "ru", "cs", "de", "fr", "tr", "vi", "hi", "ar", "pt"]

# Front matter keys that should NOT be translated
NO_TRANSLATE_KEYS = {
    "aliases", "layout", "slug", "lastUpdated", "lastupdated", "accurateFor",
    "reviewStatus", "date", "author", "categories", "tags",
    "toc", "weight", "draft", "number", "created", "thread", "supercedes",
    "supersedes", "supersededby", "updated", "type", "API"
}

SYSTEM_PROMPT = """You are a professional technical translator specializing in I2P (The Invisible Internet Project) documentation.

INSTRUCTIONS:
1. Translate the input text inside <source_text> tags to {target_lang}.
2. Output ONLY the translated text wrapped in <translation> tags.
3. Do not include any other text, preambles, or explanations.

TRANSLATION RULES:
1. Keep untranslated: code blocks, commands, URLs, file paths, variable names, JSON/YAML, Markdown syntax
2. Keep I2P terms in English: router, tunnel, leaseSet, netDb, floodfill, NTCP2, SSU, SAMv3, I2PTunnel, I2CP, I2NP, eepsite, garlic encryption
3. Keep project and software names in English exactly as written: i2pd, Go-I2P, Emissary, I2P+, Java I2P, Kovri, XD, MuWire, BiglyBT
4. Preserve ALL Markdown formatting exactly (headings, lists, links, inline code)
5. Translate naturally for meaning, not literally
6. For technical terms without equivalents: keep English + add localized explanation in parentheses (once per document)

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

    # 1. Try to extract content from <translation> tags
    match = re.search(r'<translation>\s*(.*?)\s*</translation>', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 2. Fallback: Clean up artifacts using regex patterns
    # This handles cases where model forgot tags
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
    segment_id: Optional[str] = None  # For segment-level caching

    def formatted(self) -> str:
        value = self.translated if self.translated is not None else self.text
        quote = self.quote

        # Handle YAML arrays (multiline values starting with newline)
        if value.startswith("\n"):
            # This is an array - output key: followed by array items
            return f"{self.key}:{value}"

        if quote == '"':
            escaped = value.replace('"', '\\"')
            return f'{self.key}: "{escaped}"'
        if quote == "'":
            escaped = value.replace("'", "''")
            return f"{self.key}: '{escaped}'"
        return f"{self.key}: {value}"


@dataclass
class Token:
    type: str  # heading, paragraph, blank, list, code, table
    text: str = ""
    level: int = 0
    lines: List[str] = field(default_factory=list)
    translated: Optional[str] = None
    segment_id: Optional[str] = None  # For segment-level caching

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


class ClaudeTranslator:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514") -> None:
        try:
            import anthropic
        except ImportError:
            print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
            sys.exit(1)

        self.anthropic = anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def translate(
        self, text: str, target_lang: str, source_lang: str = "en",
        max_retries: int = 5
    ) -> str:
        """Translate a text segment using Claude API with retry logic.

        Retries with exponential backoff on rate-limit (429), server errors
        (500+), and transient network failures.
        """

        # Language name mapping
        lang_names = {
            "en": "English", "es": "Spanish", "de": "German", "ko": "Korean",
            "fr": "French", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
            "ja": "Japanese", "zh": "Chinese", "cs": "Czech", "tr": "Turkish",
            "vi": "Vietnamese", "hi": "Hindi", "ar": "Arabic"
        }

        target_lang_name = lang_names.get(target_lang.lower(), target_lang)
        source_lang_name = lang_names.get(source_lang.lower(), source_lang)

        system_prompt = SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)

        user_prompt = f"""[{source_lang_name} → {target_lang_name}]
<source_text>
{text}
</source_text>"""

        last_exc = None
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )

                raw_translation = response.content[0].text.strip()

                # Clean up translation artifacts
                translated = clean_translation_artifacts(raw_translation)

                return translated

            except self.anthropic.RateLimitError as exc:
                last_exc = exc
                # Use Retry-After header if available, otherwise exponential backoff
                wait = getattr(exc, "retry_after", None) or (2 ** attempt * 5)
                print(f"  Rate limited (attempt {attempt + 1}/{max_retries}), "
                      f"waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)

            except self.anthropic.APIStatusError as exc:
                last_exc = exc
                if exc.status_code >= 500:
                    wait = 2 ** attempt * 2
                    print(f"  Server error {exc.status_code} (attempt {attempt + 1}/"
                          f"{max_retries}), waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                else:
                    # 4xx errors (except 429) are not retryable
                    raise RuntimeError(f"Claude API request failed: {exc}") from exc

            except self.anthropic.APIConnectionError as exc:
                last_exc = exc
                wait = 2 ** attempt * 2
                print(f"  Connection error (attempt {attempt + 1}/{max_retries}), "
                      f"waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)

            except Exception as exc:
                raise RuntimeError(f"Claude API request failed: {exc}") from exc

        raise RuntimeError(
            f"Claude API request failed after {max_retries} retries: {last_exc}"
        ) from last_exc


# =============================================================================
# TOGETHER AI (OPENAI-COMPATIBLE) TRANSLATOR
# =============================================================================

class TogetherTranslator:
    """Translate text segments using Together AI's OpenAI-compatible API.

    Designed for Qwen3-235B-A22B-Instruct which provides good translation
    quality at ~7.5x lower cost than Claude Sonnet.
    """

    def __init__(
        self, api_key: str,
        model: str = "Qwen/Qwen3-235B-A22B-Instruct-2507-tput"
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: openai package required for Together AI. "
                  "Install with: pip install openai", file=sys.stderr)
            sys.exit(1)

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.together.xyz/v1"
        )
        self.model = model
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def translate(
        self, text: str, target_lang: str, source_lang: str = "en",
        max_retries: int = 5
    ) -> str:
        """Translate a text segment using Together AI with retry logic."""
        lang_names = {
            "en": "English", "es": "Spanish", "de": "German", "ko": "Korean",
            "fr": "French", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
            "ja": "Japanese", "zh": "Chinese", "cs": "Czech", "tr": "Turkish",
            "vi": "Vietnamese", "hi": "Hindi", "ar": "Arabic"
        }

        target_lang_name = lang_names.get(target_lang.lower(), target_lang)
        source_lang_name = lang_names.get(source_lang.lower(), source_lang)

        system_prompt = SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)

        user_prompt = f"""[{source_lang_name} → {target_lang_name}]
<source_text>
{text}
</source_text>"""

        last_exc = None
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=4096,
                )

                if response.usage:
                    self.total_input_tokens += response.usage.prompt_tokens
                    self.total_output_tokens += response.usage.completion_tokens

                raw_translation = response.choices[0].message.content.strip()
                translated = clean_translation_artifacts(raw_translation)
                return translated

            except Exception as exc:
                last_exc = exc
                error_str = str(exc).lower()
                if "rate" in error_str or "429" in error_str:
                    wait = 2 ** attempt * 5
                    print(f"  Rate limited (attempt {attempt + 1}/{max_retries}), "
                          f"waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                elif "500" in error_str or "502" in error_str or "503" in error_str:
                    wait = 2 ** attempt * 2
                    print(f"  Server error (attempt {attempt + 1}/{max_retries}), "
                          f"waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                else:
                    raise RuntimeError(f"Together API error: {exc}") from exc

        raise RuntimeError(
            f"Together API failed after {max_retries} retries: {last_exc}"
        ) from last_exc


class OpenRouterTranslator(TogetherTranslator):
    """Translate text segments through OpenRouter's OpenAI-compatible API."""

    def __init__(
        self, api_key: str,
        model: str = "qwen/qwen3-235b-a22b-2507"
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: openai package required for OpenRouter. "
                  "Install with: pip install openai", file=sys.stderr)
            sys.exit(1)

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://geti2p.net",
                "X-OpenRouter-Title": "I2P Website Translation",
            },
        )
        self.model = model
        self.total_input_tokens = 0
        self.total_output_tokens = 0


# =============================================================================
# POST-TRANSLATION VALIDATION
# =============================================================================

# Unicode script ranges for language contamination detection
_SCRIPT_RANGES = {
    "ar": {"Arabic"},
    "hi": {"Devanagari"},
    "ko": {"Hangul"},
    "zh": {"CJK", "Han"},
    "ru": {"Cyrillic"},
    "cs": {"Latin"},
    "de": {"Latin"},
    "es": {"Latin"},
    "fr": {"Latin"},
    "pt": {"Latin"},
    "tr": {"Latin"},
    "vi": {"Latin"},
}

# Scripts that should NEVER appear in output for a given target language
# (small amounts of Latin are OK everywhere since technical terms stay English)
_FORBIDDEN_SCRIPTS = {
    "ar": {"Cyrillic", "Hangul", "Devanagari"},
    "hi": {"Cyrillic", "Hangul", "Arabic"},
    "ko": {"Cyrillic", "Arabic", "Devanagari"},
    "zh": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "ru": {"Hangul", "Arabic", "Devanagari"},
    "cs": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "de": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "es": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "fr": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "pt": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "tr": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
    "vi": {"Cyrillic", "Hangul", "Arabic", "Devanagari"},
}


def _extract_urls(text: str) -> set:
    """Extract all URLs from text."""
    return set(re.findall(r'https?://[^\s\)\]>"\']+', text))


def _extract_code_spans(text: str) -> set:
    """Extract inline code spans (backtick-delimited)."""
    return set(re.findall(r'`([^`]+)`', text))


def _detect_script_contamination(text: str, target_lang: str) -> list:
    """Detect characters from scripts that shouldn't appear in the target language.

    Returns list of (script_name, example_char, position) tuples for violations.
    """
    forbidden = _FORBIDDEN_SCRIPTS.get(target_lang, set())
    if not forbidden:
        return []

    violations = []
    seen_scripts = set()

    for i, char in enumerate(text):
        if not char.strip():
            continue
        try:
            script = unicodedata.name(char, "").split()[0]
        except (ValueError, IndexError):
            continue

        # Map Unicode character names to script categories
        script_cat = None
        if "CYRILLIC" in script:
            script_cat = "Cyrillic"
        elif "HANGUL" in script:
            script_cat = "Hangul"
        elif "ARABIC" in script:
            script_cat = "Arabic"
        elif "DEVANAGARI" in script:
            script_cat = "Devanagari"

        if script_cat and script_cat in forbidden and script_cat not in seen_scripts:
            seen_scripts.add(script_cat)
            violations.append((script_cat, char, i))

    return violations


def validate_translation(
    source: str,
    translated: str,
    target_lang: str,
    segment_type: str = "paragraph"
) -> list:
    """Validate a translation against the source text.

    Returns a list of validation error strings. Empty list = passed.

    Checks:
    1. URLs preserved (all source URLs appear in translation)
    2. Code spans preserved (backtick content unchanged)
    3. Numeric literals preserved exactly
    4. No script contamination (e.g., Cyrillic in Arabic output)
    5. Translation is not empty
    6. Translation is not identical to source (unless very short/technical)
    """
    errors = []

    # 1. Empty translation
    if not translated.strip():
        errors.append("Translation is empty")
        return errors

    # 2. URL preservation
    source_urls = _extract_urls(source)
    translated_urls = _extract_urls(translated)
    missing_urls = source_urls - translated_urls
    if missing_urls:
        errors.append(f"Missing URLs: {', '.join(list(missing_urls)[:3])}")

    # 3. Code span preservation (only for paragraphs and lists, not headings)
    if segment_type in ("paragraph", "list"):
        source_code = _extract_code_spans(source)
        translated_code = _extract_code_spans(translated)
        # Code spans should be preserved exactly
        missing_code = source_code - translated_code
        if missing_code:
            # Filter out very short spans that might legitimately change
            significant_missing = {c for c in missing_code if len(c) > 2}
            if significant_missing:
                errors.append(
                    f"Modified code spans: {', '.join(list(significant_missing)[:3])}"
                )

    # 4. Numeric literal preservation. Technical values, sizes, protocol
    # versions, and message numbers must not change during translation.
    source_numbers = Counter(re.findall(r"\d+", source))
    translated_numbers = Counter(re.findall(r"\d+", translated))
    if source_numbers != translated_numbers:
        errors.append(
            "Modified numeric literals: "
            f"expected {dict(source_numbers)}, got {dict(translated_numbers)}"
        )

    # 5. Script contamination
    contamination = _detect_script_contamination(translated, target_lang)
    if contamination:
        details = ", ".join(
            f"{script}('{char}')" for script, char, _ in contamination
        )
        errors.append(f"Script contamination: {details}")

    # 6. Unchanged translation (for non-trivial, non-technical text)
    # Skip this check for headings (often contain technical names that stay English)
    # and for short text (< 50 chars) which is often mostly technical terms
    if (len(source) > 50 and segment_type not in ("heading", "frontmatter")
            and source.strip() == translated.strip()):
        errors.append("Translation identical to source")

    return errors


def translate_with_validation(
    translator,
    source_text: str,
    target_lang: str,
    source_lang: str,
    segment_type: str,
    max_validation_retries: int = 2,
    verbose: bool = True
) -> str:
    """Translate text with post-translation validation and retry.

    On validation failure, retries with a more specific prompt that
    describes what went wrong.

    Args:
        translator: ClaudeTranslator or TogetherTranslator instance
        source_text: Text to translate
        target_lang: Target language code
        source_lang: Source language code
        segment_type: Type of segment (heading, paragraph, list, table)
        max_validation_retries: Max retries on validation failure
        verbose: Print validation details

    Returns:
        Validated translation string
    """
    translated = translator.translate(source_text, target_lang, source_lang)

    for retry in range(max_validation_retries):
        errors = validate_translation(
            source_text, translated, target_lang, segment_type
        )

        if not errors:
            return translated

        if verbose:
            print(f"  VALIDATION FAILED (attempt {retry + 1}): "
                  f"{'; '.join(errors)}", file=sys.stderr)

        # Build a correction prompt with specific feedback
        lang_names = {
            "en": "English", "es": "Spanish", "de": "German", "ko": "Korean",
            "fr": "French", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
            "ja": "Japanese", "zh": "Chinese", "cs": "Czech", "tr": "Turkish",
            "vi": "Vietnamese", "hi": "Hindi", "ar": "Arabic"
        }
        target_lang_name = lang_names.get(target_lang.lower(), target_lang)

        correction_feedback = "\n".join(f"- {e}" for e in errors)
        correction_prompt = (
            f"Your previous translation had these issues:\n{correction_feedback}\n\n"
            f"Please re-translate to {target_lang_name}, fixing these issues. "
            f"Preserve ALL URLs, code spans (backtick content), and technical terms exactly."
        )

        # Re-translate with feedback — use a fresh call with the correction context
        system_prompt = SYSTEM_PROMPT.replace("{target_lang}", target_lang_name)
        source_lang_name = lang_names.get(source_lang.lower(), source_lang)

        if isinstance(translator, ClaudeTranslator):
            try:
                response = translator.client.messages.create(
                    model=translator.model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": f"[{source_lang_name} → {target_lang_name}]\n<source_text>\n{source_text}\n</source_text>"},
                        {"role": "assistant", "content": f"<translation>\n{translated}\n</translation>"},
                        {"role": "user", "content": correction_prompt},
                    ]
                )
                raw = response.content[0].text.strip()
                translated = clean_translation_artifacts(raw)
            except Exception:
                break  # Fall through with best attempt
        elif isinstance(translator, TogetherTranslator):
            try:
                response = translator.client.chat.completions.create(
                    model=translator.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"[{source_lang_name} → {target_lang_name}]\n<source_text>\n{source_text}\n</source_text>"},
                        {"role": "assistant", "content": f"<translation>\n{translated}\n</translation>"},
                        {"role": "user", "content": correction_prompt},
                    ],
                    max_tokens=4096,
                )
                if response.usage:
                    translator.total_input_tokens += response.usage.prompt_tokens
                    translator.total_output_tokens += response.usage.completion_tokens
                raw = response.choices[0].message.content.strip()
                translated = clean_translation_artifacts(raw)
            except Exception:
                break

    # Final validation — log but accept anyway (best effort)
    final_errors = validate_translation(
        source_text, translated, target_lang, segment_type
    )
    if final_errors and verbose:
        print(f"  VALIDATION WARNING (accepting anyway): "
              f"{'; '.join(final_errors)}", file=sys.stderr)

    return translated


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file content."""
    content = file_path.read_text(encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _content_dir_from_base(base_dir: Path) -> Path:
    """Derive the content/ directory from a base directory."""
    content_dir = base_dir / "content"
    return content_dir if content_dir.exists() else base_dir


def _file_cache_key(file_path: Path, base_dir: Path) -> str:
    """Compute the cache key for a file (relative to content/ dir, e.g. 'en/blog/post.md')."""
    content_dir = _content_dir_from_base(base_dir)
    try:
        rel_path = file_path.relative_to(content_dir)
    except ValueError:
        try:
            rel_path = file_path.relative_to(base_dir)
        except ValueError:
            rel_path = file_path
    return str(rel_path).replace("\\", "/")


def get_files_to_translate(
    files: List[Path],
    base_dir: Optional[Path] = None,
    segment_cache: Optional[Dict] = None
) -> List[Path]:
    """Compare file hashes and return list of files that need translation.

    Args:
        files: List of file paths to check
        base_dir: Base directory (default: current working directory)
        segment_cache: Segment cache dict containing file_hash entries

    Returns:
        List of files that are new or have changed (hash differs)
    """
    # Read stored hashes from segment cache
    stored_hashes = {}
    if segment_cache:
        for file_key, file_data in segment_cache.get("files", {}).items():
            fh = file_data.get("file_hash")
            if fh:
                stored_hashes[file_key] = fh

    files_to_translate = []

    if base_dir is None:
        base_dir = Path.cwd()

    for file_path in files:
        if not file_path.exists():
            continue

        rel_path_str = _file_cache_key(file_path, base_dir)
        current_hash = calculate_file_hash(file_path)
        stored_hash = stored_hashes.get(rel_path_str)

        if stored_hash is None or stored_hash != current_hash:
            files_to_translate.append(file_path)

    return files_to_translate


def update_translation_hashes(
    files: List[Path],
    base_dir: Optional[Path] = None,
    segment_cache: Optional[Dict] = None
) -> None:
    """Update file hashes in the segment cache for successfully translated files.

    Does NOT save to disk; caller must call save_segment_cache() afterward.

    Args:
        files: List of file paths to update hashes for
        base_dir: Base directory (default: current working directory)
        segment_cache: Segment cache dict (modified in place)
    """
    if segment_cache is None:
        return

    if base_dir is None:
        base_dir = Path.cwd()

    for file_path in files:
        if not file_path.exists():
            continue

        rel_path_str = _file_cache_key(file_path, base_dir)
        current_hash = calculate_file_hash(file_path)

        if rel_path_str not in segment_cache.get("files", {}):
            segment_cache.setdefault("files", {})[rel_path_str] = {"segments": {}}
        segment_cache["files"][rel_path_str]["file_hash"] = current_hash


# =============================================================================
# SEGMENT-LEVEL CACHING
# =============================================================================

def calculate_segment_hash(text: str) -> str:
    """Calculate hash for a segment's source text (16 char prefix for readability)."""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]


def _migrate_cache_v1_to_v2(cache: Dict) -> Dict:
    """Migrate segment cache from version 1 to version 2.

    Imports file hashes from claude_translation_hashes.json into the
    segment cache, eliminating the need for a separate hashes file.
    """
    if TRANSLATION_HASHES_FILE.exists():
        try:
            hash_data = json.loads(TRANSLATION_HASHES_FILE.read_text(encoding="utf-8"))
            old_hashes = hash_data.get("hashes", {})

            for old_key, file_hash in old_hashes.items():
                # Normalize key: old format is "content/en/blog/post.md"
                # New format is "en/blog/post.md" (relative to content/ dir)
                new_key = old_key[len("content/"):] if old_key.startswith("content/") else old_key

                if new_key not in cache["files"]:
                    cache["files"][new_key] = {"segments": {}}

                cache["files"][new_key]["file_hash"] = file_hash

            print(f"Migrated {len(old_hashes)} file hashes from {TRANSLATION_HASHES_FILE.name} into segment cache")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not read old hashes file during migration: {e}", file=sys.stderr)

    cache["version"] = 2
    return cache


def load_segment_cache() -> Dict:
    """Load segment cache from JSON file.

    Handles migration from v1 (separate hashes file) to v2 (hashes merged in).
    Retries on transient read errors (e.g., file being replaced by a writer).
    """
    if not SEGMENT_CACHE_FILE.exists():
        cache = {"version": 2, "files": {}}
        # Migrate hashes from old file if it exists
        if TRANSLATION_HASHES_FILE.exists():
            cache = _migrate_cache_v1_to_v2(cache)
        return cache

    # Retry up to 3 times with short delay to handle the rare case where
    # a concurrent writer is mid-rename (atomic replace)
    last_exc = None
    for attempt in range(3):
        try:
            data = json.loads(SEGMENT_CACHE_FILE.read_text(encoding="utf-8"))
            if "version" not in data:
                data["version"] = 1
            if "files" not in data:
                data["files"] = {}

            # Migrate v1 -> v2
            if data["version"] < 2:
                data = _migrate_cache_v1_to_v2(data)

            return data
        except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError) as exc:
            last_exc = exc
            if attempt < 2:
                import time as _time
                _time.sleep(0.5)

    print(f"Warning: Could not read segment cache after 3 attempts: {last_exc}",
          file=sys.stderr)
    cache = {"version": 2, "files": {}}
    if TRANSLATION_HASHES_FILE.exists():
        cache = _migrate_cache_v1_to_v2(cache)
    return cache


def _merge_cache(target: Dict, source: Dict) -> None:
    """Merge source cache into target, combining translations per segment.

    Used during parallel CI runs where multiple language jobs may update
    the cache concurrently. Each language writes to a different translation
    key within each segment, so merging is non-conflicting.
    """
    for file_key, file_data in source.get("files", {}).items():
        if file_key not in target.get("files", {}):
            target.setdefault("files", {})[file_key] = file_data
            continue
        target_file = target["files"][file_key]
        # Update file hash if source has one
        if "file_hash" in file_data:
            target_file["file_hash"] = file_data["file_hash"]
        # Merge segments
        for seg_id, seg_data in file_data.get("segments", {}).items():
            if seg_id not in target_file.get("segments", {}):
                target_file.setdefault("segments", {})[seg_id] = seg_data
            else:
                target_seg = target_file["segments"][seg_id]
                if target_seg.get("source_hash") != seg_data.get("source_hash"):
                    # Translations for the old source text are stale. Replace
                    # the segment; concurrent writers for the new source hash
                    # will merge through the branch below.
                    target_file["segments"][seg_id] = seg_data
                    continue
                for lang, trans in seg_data.get("translations", {}).items():
                    target_seg.setdefault("translations", {})[lang] = trans


def save_segment_cache(cache: Dict) -> None:
    """Save segment cache to JSON file with atomic writes for parallel safety.

    Uses write-to-temp-then-rename for atomicity so parallel readers never
    see a partially-written file. Also uses file locking to serialize
    concurrent writers (merge before write).
    """
    import tempfile

    lock_file = SEGMENT_CACHE_FILE.with_suffix(".lock")

    with open(lock_file, "a+b") as lf:
        if os.name == "nt":
            import msvcrt
            if lf.tell() == 0:
                lf.write(b"\0")
                lf.flush()
            lf.seek(0)
            msvcrt.locking(lf.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            # Re-read current cache from disk to pick up changes from
            # other parallel processes, then merge our updates in
            if SEGMENT_CACHE_FILE.exists():
                try:
                    disk_cache = json.loads(
                        SEGMENT_CACHE_FILE.read_text(encoding="utf-8")
                    )
                    _merge_cache(disk_cache, cache)
                    cache = disk_cache
                except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                    pass  # Use our in-memory cache as-is

            # Atomic write: write to temp file in same directory, then rename.
            # os.rename() is atomic on POSIX, so readers never see partial data.
            fd, tmp_path = tempfile.mkstemp(
                dir=SEGMENT_CACHE_FILE.parent,
                prefix=".segment_cache_",
                suffix=".tmp",
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as tmp_f:
                    json.dump(cache, tmp_f, indent=2, ensure_ascii=False)
                os.replace(tmp_path, SEGMENT_CACHE_FILE)
            except BaseException:
                # Clean up temp file on any failure
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        finally:
            if os.name == "nt":
                lf.seek(0)
                msvcrt.locking(lf.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lf, fcntl.LOCK_UN)


def get_cached_translation(
    cache: Dict,
    file_path_str: str,
    segment_id: str,
    source_hash: str,
    target_lang: str
) -> Optional[str]:
    """Get cached translation for a segment if source hash matches.

    Uses a two-pass lookup:
    1. Primary: exact segment_id match with hash validation
    2. Fallback: scan all segments for matching source_hash (handles ID shifting
       when paragraphs are added/removed, causing sequential IDs to shift)

    Returns:
        Cached translation string if found and hash matches, None otherwise
    """
    file_cache = cache.get("files", {}).get(file_path_str, {})
    segments = file_cache.get("segments", {})

    # Primary lookup: by segment_id + hash match
    segment_data = segments.get(segment_id, {})
    if segment_data.get("source_hash") == source_hash:
        result = segment_data.get("translations", {}).get(target_lang)
        if result is not None:
            return result

    # Fallback: scan all segments for matching source_hash
    # This handles cases where segment IDs shifted (e.g., p_005 became p_006
    # because a new paragraph was inserted above)
    for sid, sdata in segments.items():
        if sid != segment_id and sdata.get("source_hash") == source_hash:
            result = sdata.get("translations", {}).get(target_lang)
            if result is not None:
                return result

    return None


def update_segment_cache(
    cache: Dict,
    file_path_str: str,
    segment_id: str,
    source_hash: str,
    target_lang: str,
    translation: str
) -> None:
    """Update cache with a new translation for a segment."""
    if "files" not in cache:
        cache["files"] = {}

    if file_path_str not in cache["files"]:
        cache["files"][file_path_str] = {"segments": {}}

    if "segments" not in cache["files"][file_path_str]:
        cache["files"][file_path_str]["segments"] = {}

    segments = cache["files"][file_path_str]["segments"]

    if (segment_id not in segments or
            segments[segment_id].get("source_hash") != source_hash):
        # Never carry translations forward when the source text changed.
        segments[segment_id] = {"source_hash": source_hash, "translations": {}}

    segments[segment_id]["translations"][target_lang] = translation


def assign_segment_ids(
    fm_entries: List[FrontMatterEntry],
    tokens: List[Token]
) -> None:
    """Assign unique segment IDs to front matter entries and tokens.

    IDs follow the pattern:
    - Front matter: fm_{key} (e.g., fm_title, fm_description)
    - Headings: h{level}_{count:03d} (e.g., h2_001, h3_002)
    - Paragraphs: p_{count:03d} (e.g., p_001, p_002)
    - Lists: list_{count:03d}
    - Tables: table_{count:03d}
    """
    # Assign IDs to front matter entries
    for entry in fm_entries:
        entry.segment_id = f"fm_{entry.key}"

    # Counters for each heading level and other types
    heading_counts: Dict[int, int] = {}
    paragraph_count = 0
    list_count = 0
    table_count = 0

    for token in tokens:
        if token.type == "heading":
            level = token.level
            if level not in heading_counts:
                heading_counts[level] = 0
            heading_counts[level] += 1
            token.segment_id = f"h{level}_{heading_counts[level]:03d}"

        elif token.type == "paragraph":
            paragraph_count += 1
            token.segment_id = f"p_{paragraph_count:03d}"

        elif token.type == "list":
            list_count += 1
            token.segment_id = f"list_{list_count:03d}"

        elif token.type == "table":
            table_count += 1
            token.segment_id = f"table_{table_count:03d}"


def build_cache_from_existing(
    content_root: Path,
    source_lang: str = "en",
    verbose: bool = True
) -> int:
    """Build segment cache from existing source and translated files.

    This function reads English source files and their existing translations,
    then populates the segment cache without making any API calls.

    Args:
        content_root: Path to content/ directory
        source_lang: Source language code (default: en)
        verbose: Print progress

    Returns:
        Number of segments cached
    """
    source_dir = content_root / source_lang
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}", file=sys.stderr)
        return 0

    # Find all markdown files in source directory
    source_files = list(source_dir.rglob("*.md"))

    if verbose:
        print(f"\n{'='*60}")
        print(f"Building Segment Cache from Existing Translations")
        print(f"{'='*60}")
        print(f"Source directory: {source_dir}")
        print(f"Found {len(source_files)} source files")
        print(f"Target languages: {', '.join(TARGET_LANGUAGES)}")
        print(f"{'='*60}\n")

    cache = load_segment_cache()
    total_segments = 0
    total_translations = 0

    for source_path in source_files:
        try:
            source_content = source_path.read_text(encoding="utf-8")
            source_fm, source_body = split_front_matter(source_content)
            source_tokens = tokenize_markdown(source_body)
            assign_segment_ids(source_fm, source_tokens)

            rel_path = source_path.relative_to(content_root)
            file_path_str = str(rel_path).replace("\\", "/")

            if verbose:
                print(f"Processing: {file_path_str}")

            # Count source segments for reporting
            seg_count = sum(1 for e in source_fm if e.key not in NO_TRANSLATE_KEYS and e.segment_id)
            seg_count += sum(1 for t in source_tokens if t.type in ("heading", "paragraph", "list", "table") and t.segment_id)
            total_segments += seg_count

            cached = build_cache_for_file(
                cache=cache,
                file_path_str=file_path_str,
                source_fm=source_fm,
                source_tokens=source_tokens,
                content_dir=content_root,
                source_lang=source_lang,
                verbose=verbose
            )
            total_translations += cached

        except Exception as e:
            if verbose:
                print(f"  Warning: Could not process {source_path}: {e}")
            continue

    # Save cache
    save_segment_cache(cache)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Cache Build Complete")
        print(f"{'='*60}")
        print(f"Files processed: {len(source_files)}")
        print(f"Segments indexed: {total_segments}")
        print(f"Translations cached: {total_translations}")
        print(f"Cache saved to: {SEGMENT_CACHE_FILE}")
        print(f"{'='*60}\n")

    return total_translations


def build_cache_for_file(
    cache: Dict,
    file_path_str: str,
    source_fm: List[FrontMatterEntry],
    source_tokens: List[Token],
    content_dir: Path,
    source_lang: str = "en",
    target_languages: Optional[List[str]] = None,
    verbose: bool = True
) -> int:
    """Build segment cache for a single file from existing translations on disk.

    Reads existing translated files for each target language, parses them,
    matches segments by ID, and populates the cache. This avoids unnecessary
    API calls when the segment cache is cold for a file that already has
    translations on disk.

    Args:
        cache: The segment cache dict (modified in place)
        file_path_str: Cache key for the file (e.g., "en/blog/post.md")
        source_fm: Already-parsed source front matter entries (with segment_ids)
        source_tokens: Already-parsed source tokens (with segment_ids)
        content_dir: Path to the content/ directory
        source_lang: Source language code (default: "en")
        target_languages: Languages to check (default: TARGET_LANGUAGES)
        verbose: Print progress

    Returns:
        Number of segment-language pairs cached
    """
    if target_languages is None:
        target_languages = TARGET_LANGUAGES

    # Build source segments list
    source_segments = []
    for entry in source_fm:
        if entry.key not in NO_TRANSLATE_KEYS and entry.segment_id:
            source_hash = calculate_segment_hash(entry.text)
            source_segments.append({
                "type": "frontmatter",
                "segment_id": entry.segment_id,
                "source_hash": source_hash,
            })

    for token in source_tokens:
        if token.segment_id and token.type in ("heading", "paragraph"):
            source_hash = calculate_segment_hash(token.text)
            source_segments.append({
                "type": token.type,
                "segment_id": token.segment_id,
                "source_hash": source_hash,
            })
        elif token.segment_id and token.type in ("list", "table"):
            source_text = "\n".join(token.lines)
            source_hash = calculate_segment_hash(source_text)
            source_segments.append({
                "type": token.type,
                "segment_id": token.segment_id,
                "source_hash": source_hash,
            })

    cached_count = 0

    for target_lang in target_languages:
        # Construct target path from cache key
        target_rel = file_path_str.replace(f"{source_lang}/", f"{target_lang}/", 1)
        target_path = content_dir / target_rel

        if not target_path.exists():
            continue

        try:
            target_content = target_path.read_text(encoding="utf-8")
            target_fm, target_body = split_front_matter(target_content)
            target_tokens = tokenize_markdown(target_body)
            assign_segment_ids(target_fm, target_tokens)

            # Build lookup for target segments
            target_fm_lookup = {e.segment_id: e.text for e in target_fm if e.segment_id}
            target_token_lookup = {}
            for t in target_tokens:
                if t.segment_id:
                    if t.type in ("heading", "paragraph"):
                        target_token_lookup[t.segment_id] = t.text
                    elif t.type in ("list", "table"):
                        target_token_lookup[t.segment_id] = "\n".join(t.lines)

            # Match source segments with target translations
            for seg in source_segments:
                seg_id = seg["segment_id"]
                if seg["type"] == "frontmatter":
                    translated = target_fm_lookup.get(seg_id)
                else:
                    translated = target_token_lookup.get(seg_id)

                if translated:
                    update_segment_cache(
                        cache, file_path_str, seg_id,
                        seg["source_hash"], target_lang, translated
                    )
                    cached_count += 1

        except Exception as e:
            if verbose:
                print(f"  Warning: Could not parse {target_path}: {e}")
            continue

    return cached_count


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
    i = 0
    while i < len(fm_lines):
        raw = fm_lines[i]

        if not raw.strip():
            i += 1
            continue

        if ":" not in raw:
            i += 1
            continue

        key, _, raw_value = raw.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()

        # Handle YAML arrays (multi-line values starting with -)
        # If the value is empty and next lines are indented array items
        if not raw_value and i + 1 < len(fm_lines):
            array_lines = []
            j = i + 1
            # Collect array items (lines starting with spaces and -)
            while j < len(fm_lines):
                next_line = fm_lines[j]
                # Check if it's an array item (indented, starts with -)
                if next_line.strip() and not next_line[0].isspace():
                    break  # Next key found
                if next_line.strip().startswith("-"):
                    array_lines.append(next_line)
                    j += 1
                elif next_line.strip():
                    # Non-array line, stop
                    break
                else:
                    j += 1

            if array_lines:
                # Preserve the array as raw multiline text
                # Store the full array structure in text field
                text = "\n" + "\n".join(array_lines)
                raw_value = ""  # Keep raw_value empty to signal array
                entries.append(FrontMatterEntry(key=key, raw_value=raw_value, quote=None, text=text))
                i = j  # Skip past array items
                continue

        # Handle simple scalar values
        quote = None
        text = raw_value
        if raw_value.startswith('"') and raw_value.endswith('"'):
            quote = '"'
            text = raw_value[1:-1].replace('\\"', '"')
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            quote = "'"
            text = raw_value[1:-1].replace("''", "'")

        entries.append(FrontMatterEntry(key=key, raw_value=raw_value, quote=quote, text=text))
        i += 1

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
        if (line.startswith("    ") or line.startswith("\t")) and line.strip():
            code_lines = []
            # Collect all consecutive indented lines (4+ spaces or tab)
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
        elif token.type == "table":
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
                print(f"\n  File exists: {output_path}")
                print("   Skipping (use --overwrite to replace)")
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        if verbose:
            print(f"\n  HTML file copied to: {output_path}")

        return True

    except Exception as exc:
        print(f"\n  Error copying {source_path}: {exc}", file=sys.stderr)
        import traceback
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return False


def translate_file(
    source_path: Path,
    target_lang: str,
    translator,
    output_root: Path,
    source_lang: str = "en",
    dry_run: bool = False,
    overwrite: bool = False,
    verbose: bool = True,
    copy_html: bool = False,
    use_cache: bool = True,
    segment_cache: Optional[Dict] = None,
    validate: bool = True
) -> tuple[bool, int, int]:
    """Translate a single markdown file or copy an HTML file.

    Args:
        source_path: Path to source file
        target_lang: Target language code
        translator: ClaudeTranslator or TogetherTranslator instance
        output_root: Root directory for output
        source_lang: Source language code
        dry_run: If True, don't write files
        overwrite: If True, overwrite existing files
        verbose: If True, print progress
        copy_html: If True, copy HTML files without translation
        use_cache: If True, use segment-level caching
        segment_cache: Shared segment cache dict (modified in place)
        validate: If True, validate translations and retry on failure

    Returns:
        Tuple of (success, cache_hits, cache_misses)
    """
    # Handle HTML files
    if source_path.suffix.lower() == '.html':
        if copy_html:
            success = copy_html_file(
                source_path=source_path,
                target_lang=target_lang,
                output_root=output_root,
                source_lang=source_lang,
                dry_run=dry_run,
                overwrite=overwrite,
                verbose=verbose
            )
            return (success, 0, 0)
        else:
            if verbose:
                print(f"\n  Skipping HTML file: {source_path}")
                print("   Use --copy-html to copy HTML files without translation")
            return (False, 0, 0)

    # Handle markdown files
    if verbose:
        print(f"\n{'='*60}")
        print(f"Source: {source_path}")
        print(f"Target language: {target_lang.upper()}")
        print(f"Model: {translator.model}")
        print(f"Segment caching: {'enabled' if use_cache else 'disabled'}")
        print(f"{'='*60}\n")

    cache_hits = 0
    cache_misses = 0

    try:
        content = source_path.read_text(encoding="utf-8")
        fm_entries, body = split_front_matter(content)
        tokens = tokenize_markdown(body)

        # Assign segment IDs for caching
        assign_segment_ids(fm_entries, tokens)

        # Calculate file path for cache key
        # IMPORTANT: Must match the key format used in build_cache_from_existing()
        # which uses paths relative to content/ dir (e.g., "en/blog/post.md")
        # not relative to repo root (e.g., "content/en/blog/post.md")
        try:
            # First try to get path relative to content/ directory
            content_dir = output_root / "content"
            rel_path = source_path.relative_to(content_dir)
        except ValueError:
            # Fallback: try relative to output_root
            try:
                rel_path = source_path.relative_to(output_root)
            except ValueError:
                rel_path = source_path
        file_path_str = str(rel_path).replace("\\", "/")

        # Build list of translatable segments
        segments = []
        for entry in fm_entries:
            if entry.key not in NO_TRANSLATE_KEYS:
                segments.append(("frontmatter", entry))

        for token in tokens:
            if token.type == "heading":
                segments.append(("heading", token))
            elif token.type == "paragraph":
                segments.append(("paragraph", token))
            elif token.type == "list":
                segments.append(("list", token))
            elif token.type == "table":
                segments.append(("table", token))

        if verbose:
            print(f"Processing {len(segments)} segments -> {target_lang.upper()}\n")

        # Auto-warm segment cache from existing translations on disk
        if use_cache and segment_cache is not None:
            file_cache = segment_cache.get("files", {}).get(file_path_str, {})
            existing_segments = file_cache.get("segments", {})

            if len(existing_segments) < len(segments) // 2:
                if verbose:
                    print(f"  Cache cold for {file_path_str} ({len(existing_segments)} cached vs {len(segments)} total)")
                    print(f"  Auto-building cache from existing translations on disk...")

                content_dir = output_root / "content"
                if content_dir.exists():
                    cached_count = build_cache_for_file(
                        cache=segment_cache,
                        file_path_str=file_path_str,
                        source_fm=fm_entries,
                        source_tokens=tokens,
                        content_dir=content_dir,
                        source_lang=source_lang,
                        verbose=verbose
                    )
                    if verbose:
                        print(f"  Pre-cached {cached_count} segment translations from disk\n")

        # Translate segments (with caching)
        for idx, (seg_type, seg) in enumerate(segments, start=1):
            segment_id = seg.segment_id if hasattr(seg, 'segment_id') else None

            if seg_type == "frontmatter":
                entry = seg
                source_text = entry.text
                source_hash = calculate_segment_hash(source_text)

                # Check cache
                cached = None
                if use_cache and segment_cache is not None and segment_id:
                    cached = get_cached_translation(
                        segment_cache, file_path_str, segment_id, source_hash, target_lang
                    )

                if cached is not None:
                    entry.translated = cached
                    cache_hits += 1
                    if verbose:
                        print(f"[{idx}/{len(segments)}] frontmatter:{entry.key}: {source_text[:40]!r} [CACHED]")
                else:
                    if verbose:
                        print(f"[{idx}/{len(segments)}] frontmatter:{entry.key}: {source_text[:40]!r}")
                    if validate:
                        translated = translate_with_validation(
                            translator, source_text, target_lang, source_lang,
                            "frontmatter", verbose=verbose
                        )
                    else:
                        translated = translator.translate(source_text, target_lang, source_lang)
                    entry.translated = translated
                    cache_misses += 1
                    if verbose:
                        print(f"  -> {translated[:60]!r}\n")

                    # Update cache
                    if use_cache and segment_cache is not None and segment_id:
                        update_segment_cache(
                            segment_cache, file_path_str, segment_id, source_hash, target_lang, translated
                        )

            elif seg_type == "heading":
                token = seg
                source_text = token.text
                source_hash = calculate_segment_hash(source_text)

                cached = None
                if use_cache and segment_cache is not None and segment_id:
                    cached = get_cached_translation(
                        segment_cache, file_path_str, segment_id, source_hash, target_lang
                    )

                if cached is not None:
                    token.translated = cached
                    cache_hits += 1
                    if verbose:
                        print(f"[{idx}/{len(segments)}] heading ({segment_id}): {source_text[:40]!r} [CACHED]")
                else:
                    if verbose:
                        print(f"[{idx}/{len(segments)}] heading ({segment_id}): {source_text[:40]!r}")
                    if validate:
                        translated = translate_with_validation(
                            translator, source_text, target_lang, source_lang,
                            "heading", verbose=verbose
                        )
                    else:
                        translated = translator.translate(source_text, target_lang, source_lang)
                    token.translated = translated
                    cache_misses += 1
                    if verbose:
                        print(f"  -> {translated[:60]!r}\n")

                    if use_cache and segment_cache is not None and segment_id:
                        update_segment_cache(
                            segment_cache, file_path_str, segment_id, source_hash, target_lang, translated
                        )

            elif seg_type == "paragraph":
                token = seg
                source_text = token.text
                source_hash = calculate_segment_hash(source_text)

                cached = None
                if use_cache and segment_cache is not None and segment_id:
                    cached = get_cached_translation(
                        segment_cache, file_path_str, segment_id, source_hash, target_lang
                    )

                if cached is not None:
                    token.translated = cached
                    cache_hits += 1
                    if verbose:
                        print(f"[{idx}/{len(segments)}] paragraph ({segment_id}): {source_text[:40]!r} [CACHED]")
                else:
                    if verbose:
                        print(f"[{idx}/{len(segments)}] paragraph ({segment_id}): {source_text[:40]!r}")
                    if validate:
                        translated = translate_with_validation(
                            translator, source_text, target_lang, source_lang,
                            "paragraph", verbose=verbose
                        )
                    else:
                        translated = translator.translate(source_text, target_lang, source_lang)
                    token.translated = translated
                    cache_misses += 1
                    if verbose:
                        print(f"  -> {translated[:60]!r}\n")

                    if use_cache and segment_cache is not None and segment_id:
                        update_segment_cache(
                            segment_cache, file_path_str, segment_id, source_hash, target_lang, translated
                        )

            elif seg_type == "list":
                token = seg
                source_text = "\n".join(token.lines)
                source_hash = calculate_segment_hash(source_text)

                cached = None
                if use_cache and segment_cache is not None and segment_id:
                    cached = get_cached_translation(
                        segment_cache, file_path_str, segment_id, source_hash, target_lang
                    )

                if cached is not None:
                    token.lines = cached.split("\n")
                    cache_hits += 1
                    if verbose:
                        print(f"[{idx}/{len(segments)}] list ({segment_id}): {source_text[:40]!r} [CACHED]")
                else:
                    if verbose:
                        print(f"[{idx}/{len(segments)}] list ({segment_id}): {source_text[:40]!r}")
                    if validate:
                        translated = translate_with_validation(
                            translator, source_text, target_lang, source_lang,
                            "list", verbose=verbose
                        )
                    else:
                        translated = translator.translate(source_text, target_lang, source_lang)
                    token.lines = translated.split("\n")
                    cache_misses += 1
                    if verbose:
                        print(f"  -> {translated[:60]!r}\n")

                    if use_cache and segment_cache is not None and segment_id:
                        update_segment_cache(
                            segment_cache, file_path_str, segment_id, source_hash, target_lang, translated
                        )

            elif seg_type == "table":
                token = seg
                source_text = "\n".join(token.lines)
                source_hash = calculate_segment_hash(source_text)

                cached = None
                if use_cache and segment_cache is not None and segment_id:
                    cached = get_cached_translation(
                        segment_cache, file_path_str, segment_id, source_hash, target_lang
                    )

                if cached is not None:
                    token.lines = cached.split("\n")
                    cache_hits += 1
                    if verbose:
                        print(f"[{idx}/{len(segments)}] table ({segment_id}): {source_text[:40]!r} [CACHED]")
                else:
                    if verbose:
                        print(f"[{idx}/{len(segments)}] table ({segment_id}): {source_text[:40]!r}")
                    if validate:
                        translated = translate_with_validation(
                            translator, source_text, target_lang, source_lang,
                            "table", verbose=verbose
                        )
                    else:
                        translated = translator.translate(source_text, target_lang, source_lang)
                    token.lines = translated.split("\n")
                    cache_misses += 1
                    if verbose:
                        print(f"  -> {translated[:60]!r}\n")

                    if use_cache and segment_cache is not None and segment_id:
                        update_segment_cache(
                            segment_cache, file_path_str, segment_id, source_hash, target_lang, translated
                        )

        # Clean up stale segment entries for this file to prevent unbounded
        # cache growth from shifted sequential IDs (e.g., old p_005 still cached
        # after content was removed and it became p_004)
        if use_cache and segment_cache is not None:
            current_ids = set()
            for _, seg in segments:
                sid = getattr(seg, "segment_id", None)
                if sid:
                    current_ids.add(sid)
            file_segments = (
                segment_cache.get("files", {})
                .get(file_path_str, {})
                .get("segments", {})
            )
            stale_ids = [sid for sid in file_segments if sid not in current_ids]
            for sid in stale_ids:
                del file_segments[sid]

        output_text = reconstruct_markdown(fm_entries, tokens)

        # Determine output path
        rel_path = source_path.relative_to(output_root / "content" / source_lang)
        output_path = output_root / "content" / target_lang / rel_path

        if dry_run:
            if verbose:
                print(f"\n[DRY RUN] Would write to: {output_path}")
                print(f"Cache stats: {cache_hits} hits, {cache_misses} misses")
                print(f"\nPreview (first 500 chars):\n{output_text[:500]}\n")
            return (True, cache_hits, cache_misses)

        # Check if file exists
        if output_path.exists() and not overwrite:
            if verbose:
                print(f"\n  File exists: {output_path}")
                print("   Skipping (use --overwrite to replace)")
            return (False, cache_hits, cache_misses)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")

        if verbose:
            print(f"\n  Translated file written to: {output_path}")
            print(f"  Cache stats: {cache_hits} hits, {cache_misses} misses (API calls)")

        # Log the translation
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": str(source_path),
            "target": str(output_path),
            "source_lang": source_lang,
            "target_lang": target_lang,
            "model": translator.model,
            "segments": len(segments),
            "cache_hits": cache_hits,
            "cache_misses": cache_misses
        }

        if TRANSLATION_LOG.exists():
            try:
                log_data = json.loads(TRANSLATION_LOG.read_text(encoding="utf-8"))
                if not isinstance(log_data, list):
                    log_data = []
            except (json.JSONDecodeError, FileNotFoundError):
                log_data = []
        else:
            log_data = []

        log_data.append(log_entry)
        TRANSLATION_LOG.write_text(json.dumps(log_data, indent=2, ensure_ascii=False), encoding="utf-8")

        return (True, cache_hits, cache_misses)

    except Exception as exc:
        print(f"\n  Error translating {source_path}: {exc}", file=sys.stderr)
        import traceback
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return (False, cache_hits, cache_misses)


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate Hugo markdown using Claude API (realtime)")

    # File selection (not required when using --build-cache or --cache-stats)
    file_group = parser.add_mutually_exclusive_group(required=False)
    file_group.add_argument("--source", help="Source markdown file path (for single file)")
    file_group.add_argument("--source-dir", help="Source directory (for multiple files)")

    parser.add_argument("--pattern", help="File pattern for source-dir (e.g., '2025-*.md')")
    parser.add_argument("--target-lang", help="Target language code (e.g., de, ko, es)")
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Claude model (default: claude-sonnet-4-20250514)")
    parser.add_argument("--output-root", help="Output root directory (default: auto-detect)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing translated files")
    parser.add_argument("--check-hashes", action="store_true", default=True, help="Only translate files that changed (default: True)")
    parser.add_argument("--no-check-hashes", dest="check_hashes", action="store_false", help="Translate all files regardless of hash")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    parser.add_argument("--update-hashes", action="store_true", default=True, help="Update translation hashes after successful translation (default: True)")
    parser.add_argument("--no-update-hashes", dest="update_hashes", action="store_false", help="Don't update translation hashes")
    parser.add_argument("--copy-html", action="store_true", help="Copy HTML files without translation (for data files like papers.html)")

    # Provider options
    parser.add_argument("--provider", choices=["claude", "together", "openrouter"], default="claude",
                        help="Translation provider (default: claude)")
    parser.add_argument("--together-model",
                        default="Qwen/Qwen3-235B-A22B-Instruct-2507-tput",
                        help="Together AI model (default: Qwen/Qwen3-235B-A22B-Instruct-2507-tput)")
    parser.add_argument("--openrouter-model",
                        default="qwen/qwen3-235b-a22b-2507",
                        help="OpenRouter model (default: qwen/qwen3-235b-a22b-2507)")
    parser.add_argument("--no-validate", dest="validate", action="store_false", default=True,
                        help="Disable post-translation validation")

    # Segment caching options
    parser.add_argument("--no-cache", dest="use_cache", action="store_false", default=True,
                        help="Disable segment-level caching (translate all segments)")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Clear segment cache before translating")
    parser.add_argument("--cache-stats", action="store_true",
                        help="Show cache statistics and exit")
    parser.add_argument("--build-cache", action="store_true",
                        help="Build segment cache from existing translations (no API calls)")
    parser.add_argument("--content-root", help="Content root directory for --build-cache (default: ./content)")

    args = parser.parse_args()

    # Handle cache-stats (doesn't require API key)
    if args.cache_stats:
        cache = load_segment_cache()
        files = cache.get("files", {})
        total_segments = 0
        total_translations = 0
        for file_path, file_data in files.items():
            segments = file_data.get("segments", {})
            total_segments += len(segments)
            for seg_id, seg_data in segments.items():
                total_translations += len(seg_data.get("translations", {}))

        print(f"\n{'='*60}")
        print(f"Segment Cache Statistics")
        print(f"{'='*60}")
        print(f"Cache file: {SEGMENT_CACHE_FILE}")
        print(f"Files cached: {len(files)}")
        print(f"Total segments: {total_segments}")
        print(f"Total translations: {total_translations}")
        if total_segments > 0:
            print(f"Avg translations/segment: {total_translations / total_segments:.1f}")
        print(f"{'='*60}\n")
        return 0

    # Handle build-cache (doesn't require API key)
    if args.build_cache:
        content_root = Path(args.content_root) if args.content_root else Path.cwd() / "content"
        if not content_root.exists():
            print(f"Error: Content root not found: {content_root}", file=sys.stderr)
            print("Use --content-root to specify the content directory", file=sys.stderr)
            return 1
        result = build_cache_from_existing(
            content_root=content_root,
            source_lang=args.source_lang,
            verbose=not args.quiet
        )
        return 0 if result > 0 else 1

    # Validate required args for translation mode
    if not args.source and not args.source_dir:
        print("Error: --source or --source-dir is required for translation", file=sys.stderr)
        return 1
    if not args.target_lang:
        print("Error: --target-lang is required for translation", file=sys.stderr)
        return 1

    # Get API key based on provider
    if args.provider in ("together", "openrouter"):
        env_name = "TOGETHER_API_KEY" if args.provider == "together" else "OPENROUTER_API_KEY"
        api_key = os.getenv(env_name)
        if not api_key:
            print(f"Error: {env_name} environment variable is required "
                  f"when using --provider {args.provider}", file=sys.stderr)
            return 1
    else:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable is required", file=sys.stderr)
            return 1

    # Handle clear-cache
    if args.clear_cache:
        if SEGMENT_CACHE_FILE.exists():
            SEGMENT_CACHE_FILE.unlink()
            if not args.quiet:
                print(f"Cleared segment cache: {SEGMENT_CACHE_FILE}")
        else:
            if not args.quiet:
                print("No segment cache to clear")

    # Collect files
    files = []
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

    # Load segment cache early (needed for file hash checks and segment caching)
    segment_cache = load_segment_cache()

    # Filter by hash if requested
    if args.check_hashes and not args.dry_run:
        base_dir = Path(args.output_root).resolve() if args.output_root else Path.cwd()

        original_count = len(files)
        files = get_files_to_translate(files, base_dir=base_dir, segment_cache=segment_cache)

        if not files:
            if not args.quiet:
                print("No files need translation (all files already translated)")
            return 0
        if len(files) < original_count:
            if not args.quiet:
                print(f"Filtered {original_count - len(files)} file(s) that don't need translation")

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
            print(f"  File path: {files[0]}", file=sys.stderr)
            return 1

    if args.provider == "together":
        translator = TogetherTranslator(api_key=api_key, model=args.together_model)
        provider_label = f"Together AI ({args.together_model})"
    elif args.provider == "openrouter":
        translator = OpenRouterTranslator(api_key=api_key, model=args.openrouter_model)
        provider_label = f"OpenRouter ({args.openrouter_model})"
    else:
        translator = ClaudeTranslator(api_key=api_key, model=args.model)
        provider_label = f"Claude ({args.model})"

    if not args.quiet:
        print(f"\n{'='*60}")
        print(f"Real-time Translation")
        print(f"{'='*60}")
        print(f"Files: {len(files)}")
        print(f"Target language: {args.target_lang.upper()}")
        print(f"Provider: {provider_label}")
        print(f"Segment caching: {'enabled' if args.use_cache else 'disabled'}")
        print(f"Validation: {'enabled' if args.validate else 'disabled'}")
        print(f"{'='*60}\n")

    # Translate files
    successful = []
    failed = []
    total_cache_hits = 0
    total_cache_misses = 0

    for file_path in files:
        success, cache_hits, cache_misses = translate_file(
            source_path=file_path,
            target_lang=args.target_lang,
            translator=translator,
            output_root=output_root,
            source_lang=args.source_lang,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
            verbose=not args.quiet,
            copy_html=args.copy_html,
            use_cache=args.use_cache,
            segment_cache=segment_cache if args.use_cache else None,
            validate=args.validate
        )

        total_cache_hits += cache_hits
        total_cache_misses += cache_misses

        if success:
            successful.append(file_path)
        else:
            failed.append(file_path)

    # Update file hashes in segment cache for successfully translated files
    if args.update_hashes and successful and not args.dry_run:
        base_dir = output_root if args.output_root else Path.cwd()
        update_translation_hashes(successful, base_dir=base_dir, segment_cache=segment_cache)

    # Save segment cache (includes file hashes and segment translations)
    if segment_cache is not None and not args.dry_run:
        save_segment_cache(segment_cache)

    # Summary
    if not args.quiet:
        print(f"\n{'='*60}")
        print(f"Summary")
        print(f"{'='*60}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        if args.use_cache:
            total_segments = total_cache_hits + total_cache_misses
            if total_segments > 0:
                hit_rate = (total_cache_hits / total_segments) * 100
                print(f"\nCache Performance:")
                print(f"  Hits: {total_cache_hits} ({hit_rate:.1f}%)")
                print(f"  Misses (API calls): {total_cache_misses}")
                print(f"  Total segments: {total_segments}")
        if isinstance(translator, TogetherTranslator):
            usage_label = "OpenRouter" if isinstance(translator, OpenRouterTranslator) else "Together AI"
            print(f"\n{usage_label} Token Usage:")
            print(f"  Input tokens: {translator.total_input_tokens:,}")
            print(f"  Output tokens: {translator.total_output_tokens:,}")
            # Qwen3-235B pricing: $0.20/M input, $0.60/M output
            input_cost = translator.total_input_tokens * 0.20 / 1_000_000
            output_cost = translator.total_output_tokens * 0.60 / 1_000_000
            print(f"  Estimated cost: ${input_cost + output_cost:.6f}")
        if failed:
            print(f"\nFailed files:")
            for f in failed:
                print(f"  - {f}")
        print()

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
