#!/usr/bin/env python3
"""Process batch translation results for downloads and donate pages."""
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BATCH_SCRIPT = SCRIPT_DIR / "translate_openai_batch.py"
BATCH_ID_FILE = SCRIPT_DIR / "downloads_donate_batch_ids.txt"

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable required", file=sys.stderr)
        return 1

    if not BATCH_ID_FILE.exists():
        print(f"Error: Batch ID file not found: {BATCH_ID_FILE}", file=sys.stderr)
        print("Run translate_downloads_donate.py first to submit batches", file=sys.stderr)
        return 1

    # Load batch IDs
    batch_ids = {}
    with open(BATCH_ID_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, batch_id = line.split('=', 1)
                batch_ids[key] = batch_id

    if not batch_ids:
        print("No batch IDs found in file", file=sys.stderr)
        return 1

    print(f"Found {len(batch_ids)} batch jobs to process\n")

    # Check status of all batches
    completed = 0
    failed = 0
    pending = 0

    for key, batch_id in batch_ids.items():
        print(f"Checking {key} ({batch_id})...")

        cmd = [
            "python3", str(BATCH_SCRIPT),
            "--check", batch_id,
            "--wait"  # Wait for completion
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)

            if "Status: completed" in result.stdout:
                completed += 1
                print(f"✓ Completed: {key}\n")
            elif "Status: failed" in result.stdout or "Status: error" in result.stdout:
                failed += 1
                print(f"✗ Failed: {key}\n")
            else:
                pending += 1
                print(f"⧗ Pending: {key}\n")

        except subprocess.CalledProcessError as e:
            print(f"Error checking {key}: {e}", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Batch Processing Summary")
    print(f"{'='*60}")
    print(f"Total batches: {len(batch_ids)}")
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Pending: {pending}")
    print(f"{'='*60}\n")

    if completed == len(batch_ids):
        print("✓ All translations completed successfully!")
        print("\nNext steps:")
        print("  1. Review translated files in content/{lang}/downloads/ and content/{lang}/donate/")
        print("  2. Commit and push changes")
        return 0
    elif failed > 0:
        print("✗ Some batches failed. Check the errors above.")
        return 1
    else:
        print("⧗ Some batches still pending. Run this script again later.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
