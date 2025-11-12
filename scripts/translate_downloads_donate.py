#!/usr/bin/env python3
"""Submit batch translation jobs for downloads and donate pages."""
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BATCH_SCRIPT = SCRIPT_DIR / "translate_openai_batch.py"

# Files to translate
FILES_TO_TRANSLATE = [
    "content/en/downloads/_index.md",
    "content/en/donate/download.md",
]

# Target languages
TARGET_LANGUAGES = ["ar", "cs", "de", "es", "fr", "hi", "ko", "pt", "ru", "tr", "vi", "zh"]

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable required", file=sys.stderr)
        return 1

    batch_ids = {}

    for file_path in FILES_TO_TRANSLATE:
        full_path = REPO_ROOT / file_path
        if not full_path.exists():
            print(f"Warning: File not found: {full_path}", file=sys.stderr)
            continue

        for lang in TARGET_LANGUAGES:
            print(f"\n{'='*60}")
            print(f"Submitting: {file_path} -> {lang}")
            print(f"{'='*60}")

            cmd = [
                "python3", str(BATCH_SCRIPT),
                "--submit",
                "--source", str(full_path),
                "--target-lang", lang,
                "--model", "gpt-5",
                "--output-root", str(REPO_ROOT)
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(result.stdout)

                # Extract batch ID from output
                for line in result.stdout.splitlines():
                    if line.startswith("Batch ID:"):
                        batch_id = line.split(":", 1)[1].strip()
                        key = f"{file_path}_{lang}"
                        batch_ids[key] = batch_id
                        print(f"✓ Submitted as batch {batch_id}")
                        break

            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to submit: {e}", file=sys.stderr)
                print(e.stderr, file=sys.stderr)
                return 1

    # Save batch IDs
    batch_id_file = SCRIPT_DIR / "downloads_donate_batch_ids.txt"
    with open(batch_id_file, 'w') as f:
        for key, batch_id in batch_ids.items():
            f.write(f"{key}={batch_id}\n")

    print(f"\n{'='*60}")
    print(f"All batches submitted successfully!")
    print(f"Batch IDs saved to: {batch_id_file}")
    print(f"Total batches: {len(batch_ids)}")
    print(f"{'='*60}\n")
    print("To check status and retrieve results:")
    print(f"  python3 scripts/process_downloads_donate.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
