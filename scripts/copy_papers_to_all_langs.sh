#!/bin/bash
# Helper script to copy papers.html to all target languages
# This is useful when papers.html content is updated in English

set -e

# Target languages
LANGS="de es ko ru cs fr tr zh vi hi ar pt"

# Check if OPENAI_API_KEY is set (required by script, even though not used for copying)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable must be set"
    exit 1
fi

echo "Copying papers.html to all languages..."
echo ""

for lang in $LANGS; do
    echo "→ Copying to $lang..."
    python3 scripts/translate_openai_realtime.py \
        --source content/en/papers.html \
        --target-lang "$lang" \
        --copy-html \
        --overwrite \
        --quiet
done

echo ""
echo "✅ Done! Papers.html copied to all 12 languages"
echo ""
echo "Verify with: ls -lh content/*/papers.html"
