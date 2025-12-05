#!/usr/bin/env python3
"""Check status of all batch translation jobs at once.

Usage:
    python3 check_all_batches.py
    python3 check_all_batches.py --wait
    python3 check_all_batches.py --wait --interval 120
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

# Import from the main script
sys.path.insert(0, str(Path(__file__).parent))
from translate_claude_batch import load_batch_state, save_batch_state, BATCH_STATE_FILE

def check_all_batches(wait: bool = False, interval: int = 60) -> None:
    """Check status of all batch jobs."""
    
    batches = load_batch_state()
    
    if not batches:
        print("No batch jobs found")
        return
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable required", file=sys.stderr)
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*80}")
    print(f"Batch Status Summary - {len(batches)} batch(es)")
    print(f"{'='*80}\n")
    
    all_completed = True
    all_ended = True
    
    while True:
        all_completed = True
        all_ended = True
        
        for batch_id, batch_state in batches.items():
            try:
                batch = client.messages.batches.retrieve(batch_id)
                batch_state.status = batch.processing_status
                
                # Print status
                status_icon = "✅" if batch.processing_status == "ended" else "⏳" if batch.processing_status == "processing" else "❌"
                print(f"{status_icon} {batch_id[:20]}... | {batch_state.target_lang.upper():3s} | {batch.processing_status:12s} | ", end="")
                
                if batch.request_counts:
                    print(f"Succeeded: {batch.request_counts.succeeded:4d} | Errored: {batch.request_counts.errored:4d} | Processing: {batch.request_counts.processing:4d}")
                else:
                    print("No request counts available")
                
                if batch.processing_status not in ("ended", "canceled", "canceling"):
                    all_completed = False
                    all_ended = False
                elif batch.processing_status == "ended":
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
    parser = argparse.ArgumentParser(description="Check status of all batch translation jobs")
    parser.add_argument("--wait", action="store_true", help="Poll until all batches complete")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds (default: 60)")
    
    args = parser.parse_args()
    
    check_all_batches(wait=args.wait, interval=args.interval)
    return 0

if __name__ == "__main__":
    sys.exit(main())


