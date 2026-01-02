#!/bin/bash
set -euo pipefail

# CI Translation Script
# Automatically translates changed content/en/ files using OpenAI API (realtime)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/translate_openai_realtime.py"

cd "$REPO_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Portable realpath relative function (Alpine doesn't support --relative-to)
relpath() {
    python3 -c "import os.path; print(os.path.relpath('$1', '$2'))"
}

# Check required environment variables
if [ -z "${OPENAI_API_KEY:-}" ]; then
    log_error "OPENAI_API_KEY environment variable is required"
    exit 1
fi

# Get target languages from Python script
TARGET_LANGUAGES=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from translate_openai_realtime import TARGET_LANGUAGES
print(' '.join(TARGET_LANGUAGES))
")

if [ -z "$TARGET_LANGUAGES" ]; then
    log_error "Failed to read TARGET_LANGUAGES from script"
    exit 1
fi

log_info "Target languages: $TARGET_LANGUAGES"

# Detect changed files in content/en/
log_info "Detecting changed files in content/en/..."

# Get the previous commit (CI_COMMIT_BEFORE_SHA or HEAD~1)
PREV_COMMIT="${CI_COMMIT_BEFORE_SHA:-HEAD~1}"
CURRENT_COMMIT="${CI_COMMIT_SHA:-HEAD}"

# Find changed .md and .html files in content/en/
CHANGED_FILES=$(git diff --name-only --diff-filter=ACMR "$PREV_COMMIT" "$CURRENT_COMMIT" | grep -E '^content/en/.*\.(md|html)$' || true)

if [ -z "$CHANGED_FILES" ]; then
    log_info "No changed .md or .html files found in content/en/"
    exit 0
fi

log_info "Found changed files:"
echo "$CHANGED_FILES" | while read -r file; do
    echo "  - $file"
done

# Convert changed files to absolute paths
FILES_TO_TRANSLATE=()
while IFS= read -r file; do
    if [ -n "$file" ]; then
        FILES_TO_TRANSLATE+=("$REPO_ROOT/$file")
    fi
done <<< "$CHANGED_FILES"

if [ ${#FILES_TO_TRANSLATE[@]} -eq 0 ]; then
    log_info "No files to translate"
    exit 0
fi

log_info "Files to process:"
for file in "${FILES_TO_TRANSLATE[@]}"; do
    echo "  - $(relpath "$file" "$REPO_ROOT")"
done

# Process each target language
SUCCESSFULLY_TRANSLATED_FILES=()
FAILED_LANGUAGES=()

for TARGET_LANG in $TARGET_LANGUAGES; do
    log_info "Processing translations for language: $TARGET_LANG"
    
    TRANSLATION_FAILED=0
    
    # Process each file individually
    for FILE_PATH in "${FILES_TO_TRANSLATE[@]}"; do
        if [ ! -f "$FILE_PATH" ]; then
            continue
        fi

        REL_PATH=$(relpath "$FILE_PATH" "$REPO_ROOT")
        log_info "  Translating: $REL_PATH"
        log_info "  Debug: FILE_PATH=$FILE_PATH"
        log_info "  Debug: TARGET_LANG=$TARGET_LANG"
        log_info "  Debug: REPO_ROOT=$REPO_ROOT"

        # Translate file using realtime API
        # Hash checking ensures we only translate if content actually changed
        # For HTML files, add --copy-html flag to copy instead of translate
        COPY_HTML_FLAG=""
        if [[ "$FILE_PATH" == *.html ]]; then
            COPY_HTML_FLAG="--copy-html"
            log_info "  HTML file detected - will copy without translation"
        fi

        log_info "  Running translation command..."
        log_info "  Command: python3 $PYTHON_SCRIPT --source \"$FILE_PATH\" --target-lang \"$TARGET_LANG\" --model gpt-5 --overwrite --check-hashes --output-root \"$REPO_ROOT\" --quiet $COPY_HTML_FLAG"

        # Test if Python script exists and is readable
        if [ ! -f "$PYTHON_SCRIPT" ]; then
            log_error "  Python script not found: $PYTHON_SCRIPT"
            exit 1
        fi

        # Test if Python can import required modules
        log_info "  Testing Python environment..."
        python3 --version 2>&1 | while IFS= read -r line; do
            log_info "    $line"
        done

        python3 -c "from openai import OpenAI; print('OpenAI module: OK')" 2>&1 | while IFS= read -r line; do
            log_info "    $line"
        done

        # Run translation WITHOUT capturing output first, so we can see errors in real-time
        log_info "  Starting translation (output will stream below)..."
        python3 "$PYTHON_SCRIPT" \
            --source "$FILE_PATH" \
            --target-lang "$TARGET_LANG" \
            --model gpt-5 \
            --overwrite \
            --check-hashes \
            --output-root "$REPO_ROOT" \
            --quiet \
            $COPY_HTML_FLAG

        TRANSLATE_EXIT=$?
        log_info "  Translation exit code: $TRANSLATE_EXIT"

        if [ $TRANSLATE_EXIT -eq 0 ]; then
            # Check if translated file actually exists
            REL_PATH_FOR_TRANS=$(relpath "$FILE_PATH" "$REPO_ROOT")
            TRANSLATED_PATH=$(echo "$REL_PATH_FOR_TRANS" | sed "s|^content/en/|content/$TARGET_LANG/|")
            if [ -f "$REPO_ROOT/$TRANSLATED_PATH" ]; then
                # Track successfully translated file
                FILE_ABS_PATH=$(realpath "$FILE_PATH")
                if [[ ! " ${SUCCESSFULLY_TRANSLATED_FILES[@]} " =~ " ${FILE_ABS_PATH} " ]]; then
                    SUCCESSFULLY_TRANSLATED_FILES+=("$FILE_ABS_PATH")
                fi
                log_info "    Successfully translated: $REL_PATH"
            else
                log_warn "    Translation completed but output file not found: $TRANSLATED_PATH"
            fi
        else
            log_error "    Failed to translate: $REL_PATH"
            log_error "    Exit code: $TRANSLATE_EXIT"
            TRANSLATION_FAILED=1
        fi
    done
    
    if [ $TRANSLATION_FAILED -eq 1 ]; then
        FAILED_LANGUAGES+=("$TARGET_LANG")
    fi
done

# Commit and push translated files
if [ ${#FAILED_LANGUAGES[@]} -eq 0 ]; then
    log_info "Committing translated files..."
    
    # Configure git
    git config user.name "GitLab CI"
    git config user.email "ci@i2p.www"
    
    # Add translated files and hash file
    git add scripts/translation_hashes.json
    
    # Find and add all translated files for each target language
    for TARGET_LANG in $TARGET_LANGUAGES; do
        for FILE_PATH in "${FILES_TO_TRANSLATE[@]}"; do
            if [ -f "$FILE_PATH" ]; then
                REL_PATH=$(relpath "$FILE_PATH" "$REPO_ROOT")
                TRANSLATED_PATH=$(echo "$REL_PATH" | sed "s|^content/en/|content/$TARGET_LANG/|")
                if [ -f "$TRANSLATED_PATH" ]; then
                    git add "$TRANSLATED_PATH"
                    log_info "  Added: $TRANSLATED_PATH"
                fi
            fi
        done
    done
    
    # Check if there are changes to commit
    if git diff --staged --quiet; then
        log_info "No changes to commit"
    else
        # Commit translations - CI will detect this was made by GitLab CI and skip translate stage
        git commit -m "Auto-translate: Update translations for changed content/en/ files" || {
            log_error "Failed to commit translated files"
            exit 1
        }
        
        # Push to the same branch
        CURRENT_BRANCH="${CI_COMMIT_REF_NAME:-$(git branch --show-current)}"
        log_info "Pushing to branch: $CURRENT_BRANCH"
        
        # Try to push using available tokens
        # Option 1: Use Project Access Token (if configured as CI variable)
        if [ -n "${CI_PROJECT_TOKEN:-}" ]; then
            log_info "Using CI_PROJECT_TOKEN for authentication"
            git push "https://oauth2:${CI_PROJECT_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_PROJECT_TOKEN"
                exit 1
            }
        # Option 2: Use CI_JOB_TOKEN (requires write permissions to be enabled)
        elif [ -n "${CI_JOB_TOKEN:-}" ] && [ -n "${CI_SERVER_HOST:-}" ] && [ -n "${CI_PROJECT_PATH:-}" ]; then
            log_info "Using CI_JOB_TOKEN for authentication"
            git push "https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_JOB_TOKEN"
                log_error "CI_JOB_TOKEN may not have write permissions. Check Settings → CI/CD → Token Access"
                exit 1
            }
        else
            log_error "No authentication token available for pushing"
            log_error "Options:"
            log_error "  1. Enable CI_JOB_TOKEN write permissions: Settings → CI/CD → Token Access"
            log_error "  2. Create a Project Access Token and set it as CI_PROJECT_TOKEN variable"
            exit 1
        fi
        
        log_info "Successfully committed and pushed translated files"
    fi
elif [ ${#FAILED_LANGUAGES[@]} -gt 0 ]; then
    log_error "Some translations failed for languages: ${FAILED_LANGUAGES[*]}"
    log_error "Not committing partial translations"
    exit 1
fi

log_info "Translation process completed"

