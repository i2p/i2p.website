#!/bin/bash
# Simple script to translate downloads and donate pages using realtime API
# Since batch API had duplicate ID issues, use realtime for these 2 files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check API key
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "Error: OPENAI_API_KEY required"
    exit 1
fi

# Target languages
LANGS=("ar" "cs" "de" "es" "fr" "hi" "ko" "pt" "ru" "tr" "vi" "zh")

# Files to translate
FILES=(
    "content/en/downloads/_index.md"
    "content/en/donate/download.md"
)

total_files=$((${#FILES[@]} * ${#LANGS[@]}))
current=0

echo "Translating ${#FILES[@]} files to ${#LANGS[@]} languages (${total_files} total)"
echo ""

for file in "${FILES[@]}"; do
    for lang in "${LANGS[@]}"; do
        current=$((current + 1))
        echo "[$current/$total_files] Translating $file -> $lang"

        python3 "$SCRIPT_DIR/translate_openai_realtime.py" \
            --source "$REPO_ROOT/$file" \
            --target-lang "$lang" \
            --model gpt-4o \
            --overwrite \
            --output-root "$REPO_ROOT" \
            --quiet

        if [ $? -eq 0 ]; then
            echo "  ✓ Success"
        else
            echo "  ✗ Failed"
            exit 1
        fi
    done
done

echo ""
echo "✅ All translations completed!"
echo ""
echo "Files created:"
for lang in "${LANGS[@]}"; do
    echo "  content/$lang/downloads/_index.md"
    echo "  content/$lang/donate/download.md"
done
