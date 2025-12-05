#!/bin/bash
# Submit translation batches for all remaining languages
# Usage: ./submit_all_languages.sh <source_file>

SOURCE_FILE="${1:-..//content/en/proposals/112-addressbook-subscription-feed-commands.md}"

# Languages already translated
DONE_LANGS="zh ko ru cs fr tr vi ar pt de es"

# All target languages
ALL_LANGS="hi"

echo "Submitting translation batches for: $ALL_LANGS"
echo "Source file: $SOURCE_FILE"
echo ""

for lang in $ALL_LANGS; do
    echo "=========================================="
    echo "Submitting batch for: $lang"
    echo "=========================================="
    
    python3 translate_claude_batch.py --submit \
        --source "$SOURCE_FILE" \
        --target-lang "$lang" \
        --model claude-sonnet-4-20250514
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully submitted batch for $lang"
    else
        echo "❌ Failed to submit batch for $lang"
    fi
    
    echo ""
    sleep 2  # Small delay between submissions
done

echo "=========================================="
echo "All batches submitted!"
echo "=========================================="
echo ""
echo "To check all batches, run:"
echo "  python3 translate_claude_batch.py --check-all"


