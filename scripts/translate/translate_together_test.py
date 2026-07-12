#!/usr/bin/env python3
"""Test translation using Together AI API for cost/quality comparison.

Uses the same system prompt, segmentation, artifact cleaning, and reconstruction
logic as translate_claude_realtime.py, but calls Together AI's OpenAI-compatible API.

Usage:
    pip install openai

    TOGETHER_API_KEY=... python3 scripts/translate/translate_together_test.py \
        --source content/en/docs/overview/alternative-clients.md \
        --target-lang fr \
        --output-root .
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Import shared logic from the existing translation script
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from translate_claude_realtime import (
    SYSTEM_PROMPT,
    FrontMatterEntry,
    Token,
    clean_translation_artifacts,
    split_front_matter,
    tokenize_markdown,
    assign_segment_ids,
    reconstruct_markdown,
    NO_TRANSLATE_KEYS,
)


# ---------------------------------------------------------------------------
# Together AI translator
# ---------------------------------------------------------------------------
class TogetherTranslator:
    """Translate text segments using Together AI's OpenAI-compatible API."""

    def __init__(self, api_key: str, model: str = "Qwen/Qwen3-235B-A22B-Instruct-2507-tput") -> None:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: openai package required. Install with: pip install openai",
                  file=sys.stderr)
            sys.exit(1)

        self.client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
        self.model = model
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def translate(
        self, text: str, target_lang: str, source_lang: str = "en",
        max_retries: int = 5
    ) -> str:
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

                # Track token usage
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


# ---------------------------------------------------------------------------
# Translation logic (mirrors translate_file from the Claude script)
# ---------------------------------------------------------------------------
def translate_file(
    source_path: Path,
    target_lang: str,
    translator: TogetherTranslator,
    output_root: Path,
    source_lang: str = "en",
    verbose: bool = True,
) -> bool:
    """Translate a single file using Together AI."""

    content = source_path.read_text(encoding="utf-8")
    fm_entries, body = split_front_matter(content)
    tokens = tokenize_markdown(body)
    assign_segment_ids(fm_entries, tokens)

    # Build segment list
    segments = []
    for entry in fm_entries:
        if entry.key not in NO_TRANSLATE_KEYS:
            segments.append(("frontmatter", entry))
    for token in tokens:
        if token.type in ("heading", "paragraph", "list", "table"):
            segments.append((token.type, token))

    if verbose:
        print(f"\nTranslating: {source_path}")
        print(f"Target: {target_lang.upper()}")
        print(f"Model: {translator.model}")
        print(f"Segments to translate: {len(segments)}")
        print(f"{'='*60}\n")

    api_calls = 0

    for idx, (seg_type, seg) in enumerate(segments, start=1):
        segment_id = seg.segment_id if hasattr(seg, "segment_id") else None

        if seg_type == "frontmatter":
            entry = seg
            source_text = entry.text
            if verbose:
                print(f"[{idx}/{len(segments)}] frontmatter:{entry.key}: "
                      f"{source_text[:50]!r}")
            translated = translator.translate(source_text, target_lang, source_lang)
            entry.translated = translated
            api_calls += 1
            if verbose:
                print(f"  -> {translated[:60]!r}\n")

        elif seg_type == "heading":
            token = seg
            source_text = token.text
            if verbose:
                print(f"[{idx}/{len(segments)}] heading ({segment_id}): "
                      f"{source_text[:50]!r}")
            translated = translator.translate(source_text, target_lang, source_lang)
            token.translated = translated
            api_calls += 1
            if verbose:
                print(f"  -> {translated[:60]!r}\n")

        elif seg_type == "paragraph":
            token = seg
            source_text = token.text
            if verbose:
                print(f"[{idx}/{len(segments)}] paragraph ({segment_id}): "
                      f"{source_text[:50]!r}")
            translated = translator.translate(source_text, target_lang, source_lang)
            token.translated = translated
            api_calls += 1
            if verbose:
                print(f"  -> {translated[:60]!r}\n")

        elif seg_type == "list":
            token = seg
            source_text = "\n".join(token.lines)
            if verbose:
                print(f"[{idx}/{len(segments)}] list ({segment_id}): "
                      f"{source_text[:50]!r}")
            translated = translator.translate(source_text, target_lang, source_lang)
            token.lines = translated.split("\n")
            api_calls += 1
            if verbose:
                print(f"  -> {translated[:60]!r}\n")

        elif seg_type == "table":
            token = seg
            source_text = "\n".join(token.lines)
            if verbose:
                print(f"[{idx}/{len(segments)}] table ({segment_id}): "
                      f"{source_text[:50]!r}")
            translated = translator.translate(source_text, target_lang, source_lang)
            token.lines = translated.split("\n")
            api_calls += 1
            if verbose:
                print(f"  -> {translated[:60]!r}\n")

    output_text = reconstruct_markdown(fm_entries, tokens)

    # Determine output path
    rel_path = source_path.relative_to(output_root / "content" / source_lang)
    output_path = output_root / "content" / target_lang / rel_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")

    if verbose:
        print(f"\n{'='*60}")
        print(f"Output: {output_path}")
        print(f"API calls: {api_calls}")
        print(f"Input tokens: {translator.total_input_tokens:,}")
        print(f"Output tokens: {translator.total_output_tokens:,}")
        print(f"{'='*60}\n")

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Test Together AI translation")
    parser.add_argument("--source", required=True, help="Source file path")
    parser.add_argument("--target-lang", required=True, help="Target language code")
    parser.add_argument("--model", default="Qwen/Qwen3-235B-A22B-Instruct-2507-tput",
                        help="Together AI model (default: Qwen/Qwen3-235B-A22B-Instruct-2507-tput)")
    parser.add_argument("--output-root", default=".",
                        help="Output root directory")
    parser.add_argument("--api-key", default=None,
                        help="Together API key (or set TOGETHER_API_KEY env)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        print("Error: Set TOGETHER_API_KEY or use --api-key", file=sys.stderr)
        return 1

    source = Path(args.source).resolve()
    if not source.exists():
        print(f"Error: Source file not found: {source}", file=sys.stderr)
        return 1

    output_root = Path(args.output_root).resolve()

    translator = TogetherTranslator(api_key=api_key, model=args.model)

    start_time = time.time()
    success = translate_file(
        source_path=source,
        target_lang=args.target_lang,
        translator=translator,
        output_root=output_root,
        verbose=not args.quiet,
    )
    elapsed = time.time() - start_time

    if not args.quiet:
        print(f"\nTotal time: {elapsed:.1f}s")
        # Qwen3-235B pricing on Together: $0.20/M input, $0.60/M output
        input_cost = translator.total_input_tokens * 0.20 / 1_000_000
        output_cost = translator.total_output_tokens * 0.60 / 1_000_000
        total_cost = input_cost + output_cost
        print(f"Estimated cost: ${total_cost:.6f} "
              f"(input: ${input_cost:.6f}, output: ${output_cost:.6f})")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
