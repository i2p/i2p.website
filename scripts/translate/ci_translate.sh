#!/bin/bash
set -euo pipefail

# CI Translation Script
# Automatically translates changed content/en/ files using OpenRouter (Qwen3-235B)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/translate_claude_realtime.py"

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
if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    log_error "OPENROUTER_API_KEY environment variable is required"
    exit 1
fi

# Get target languages from Python script
TARGET_LANGUAGES=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from translate_claude_realtime import TARGET_LANGUAGES
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

# Find ALL changed .md and .html files (en + translations)
ALL_CHANGED_FILES=$(git diff --name-only --diff-filter=ACMR "$PREV_COMMIT" "$CURRENT_COMMIT" | grep -E '^content/.*\.(md|html)$' || true)

# Extract only English source changes
CHANGED_FILES=$(echo "$ALL_CHANGED_FILES" | grep -E '^content/en/' || true)

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

# Process each target language (in parallel)
SUCCESSFULLY_TRANSLATED_FILES=()
FAILED_LANGUAGES=()

# Max parallel translation jobs
# Keep low to avoid API rate limits — each job makes many API calls per segment
MAX_PARALLEL=${MAX_PARALLEL_TRANSLATIONS:-12}

# Test if Python script exists and is readable
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log_error "Python script not found: $PYTHON_SCRIPT"
    exit 1
fi

# Create temp directory for per-language results
RESULT_DIR=$(mktemp -d)
trap "rm -rf $RESULT_DIR" EXIT

# Function to translate all files for a single language
translate_language() {
    local TARGET_LANG="$1"
    local RESULT_FILE="$RESULT_DIR/$TARGET_LANG"

    log_info "Processing translations for language: $TARGET_LANG"

    local TRANSLATION_FAILED=0

    for FILE_PATH in "${FILES_TO_TRANSLATE[@]}"; do
        if [ ! -f "$FILE_PATH" ]; then
            continue
        fi

        local REL_PATH
        REL_PATH=$(relpath "$FILE_PATH" "$REPO_ROOT")

        # Skip if the translated file was already updated in the same commit
        local TRANSLATED_REL
        TRANSLATED_REL=$(echo "$REL_PATH" | sed "s|^content/en/|content/$TARGET_LANG/|")
        if echo "$ALL_CHANGED_FILES" | grep -qF "$TRANSLATED_REL"; then
            log_info "  [$TARGET_LANG] Skipping (already updated in this commit): $REL_PATH"
            echo "$FILE_PATH" >> "$RESULT_FILE.success"
            continue
        fi

        local COPY_HTML_FLAG=""
        if [[ "$FILE_PATH" == *.html ]]; then
            COPY_HTML_FLAG="--copy-html"
        fi

        if python3 "$PYTHON_SCRIPT" \
            --source "$FILE_PATH" \
            --target-lang "$TARGET_LANG" \
            --provider openrouter \
            --overwrite \
            --output-root "$REPO_ROOT" \
            --quiet \
            $COPY_HTML_FLAG; then

            local REL_PATH_FOR_TRANS
            REL_PATH_FOR_TRANS=$(relpath "$FILE_PATH" "$REPO_ROOT")
            local TRANSLATED_PATH
            TRANSLATED_PATH=$(echo "$REL_PATH_FOR_TRANS" | sed "s|^content/en/|content/$TARGET_LANG/|")
            if [ -f "$REPO_ROOT/$TRANSLATED_PATH" ]; then
                log_info "  [$TARGET_LANG] Translated: $REL_PATH"
                echo "$FILE_PATH" >> "$RESULT_FILE.success"
            else
                log_warn "  [$TARGET_LANG] Output not found: $TRANSLATED_PATH"
            fi
        else
            log_error "  [$TARGET_LANG] Failed: $REL_PATH"
            TRANSLATION_FAILED=1
        fi
    done

    if [ $TRANSLATION_FAILED -eq 1 ]; then
        echo "failed" > "$RESULT_FILE.status"
    else
        echo "ok" > "$RESULT_FILE.status"
    fi
}

export -f translate_language relpath log_info log_warn log_error
export PYTHON_SCRIPT REPO_ROOT FILES_TO_TRANSLATE RESULT_DIR ALL_CHANGED_FILES
export RED GREEN YELLOW NC

# Launch translations in parallel, limited to MAX_PARALLEL at a time
log_info "Translating to $( echo $TARGET_LANGUAGES | wc -w | tr -d ' ') languages with up to $MAX_PARALLEL parallel jobs..."
RUNNING_PIDS=()

for TARGET_LANG in $TARGET_LANGUAGES; do
    # Wait if we've hit the parallel limit
    while [ ${#RUNNING_PIDS[@]} -ge $MAX_PARALLEL ]; do
        # Wait for any one job to finish
        wait -n 2>/dev/null || true
        # Clean up finished PIDs
        NEW_PIDS=()
        for pid in "${RUNNING_PIDS[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then
                NEW_PIDS+=("$pid")
            fi
        done
        RUNNING_PIDS=("${NEW_PIDS[@]}")
    done

    translate_language "$TARGET_LANG" &
    RUNNING_PIDS+=($!)
done

# Wait for all remaining jobs
wait

# Collect results
for TARGET_LANG in $TARGET_LANGUAGES; do
    STATUS_FILE="$RESULT_DIR/$TARGET_LANG.status"
    SUCCESS_FILE="$RESULT_DIR/$TARGET_LANG.success"

    if [ -f "$STATUS_FILE" ] && [ "$(cat "$STATUS_FILE")" = "failed" ]; then
        FAILED_LANGUAGES+=("$TARGET_LANG")
    fi

    if [ -f "$SUCCESS_FILE" ]; then
        while IFS= read -r file; do
            FILE_ABS_PATH=$(realpath "$file")
            if [[ ! " ${SUCCESSFULLY_TRANSLATED_FILES[@]:-} " =~ " ${FILE_ABS_PATH} " ]]; then
                SUCCESSFULLY_TRANSLATED_FILES+=("$FILE_ABS_PATH")
            fi
        done < "$SUCCESS_FILE"
    fi
done

log_info "Parallel translation complete. Success: ${#SUCCESSFULLY_TRANSLATED_FILES[@]} files, Failed languages: ${#FAILED_LANGUAGES[@]}"

# STRICT: All languages must succeed. Any failure = job failure, no partial commits.
if [ ${#FAILED_LANGUAGES[@]} -gt 0 ]; then
    log_error "Translation failed for ${#FAILED_LANGUAGES[@]} language(s): ${FAILED_LANGUAGES[*]}"
    log_error "All languages must succeed. Not committing partial translations."
    exit 1
fi

if [ ${#SUCCESSFULLY_TRANSLATED_FILES[@]} -gt 0 ]; then
    log_info "All languages succeeded. Committing translated files..."

    # Configure git (works for both GitHub Actions and GitLab CI)
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"

    # Add segment cache (includes file hashes and segment translations)
    git add scripts/translate/claude_segment_cache.json 2>/dev/null || true

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
        COMMIT_MSG="Auto-translate: Update translations for changed content/en/ files"

        # Commit translations
        git commit -m "$COMMIT_MSG" || {
            log_error "Failed to commit translated files"
            exit 1
        }

        # Push to the same branch
        CURRENT_BRANCH="${CI_COMMIT_REF_NAME:-$(git branch --show-current)}"
        log_info "Pushing to branch: $CURRENT_BRANCH"

        # Rebase on top of any commits that landed while we were translating
        # (e.g. Gitea mirror pushing back a previous translation commit)
        log_info "Rebasing on latest origin/$CURRENT_BRANCH before pushing..."
        git fetch origin "$CURRENT_BRANCH"
        git rebase "origin/$CURRENT_BRANCH" || {
            log_error "Failed to rebase on origin/$CURRENT_BRANCH"
            git rebase --abort 2>/dev/null || true
            exit 1
        }

        # GitHub Actions: GITHUB_TOKEN is already configured via checkout action
        # The checkout action with token sets up authentication automatically
        if [ -n "${GITHUB_ACTIONS:-}" ]; then
            log_info "Using GitHub Actions authentication"
            git push origin "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files"
                log_error "Make sure the workflow has 'contents: write' permission"
                exit 1
            }
        # GitLab CI: Use project token or job token
        elif [ -n "${CI_PROJECT_TOKEN:-}" ]; then
            log_info "Using CI_PROJECT_TOKEN for authentication"
            git push "https://oauth2:${CI_PROJECT_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_PROJECT_TOKEN"
                exit 1
            }
        elif [ -n "${CI_JOB_TOKEN:-}" ] && [ -n "${CI_SERVER_HOST:-}" ] && [ -n "${CI_PROJECT_PATH:-}" ]; then
            log_info "Using CI_JOB_TOKEN for authentication"
            git push "https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" "HEAD:$CURRENT_BRANCH" || {
                log_error "Failed to push translated files with CI_JOB_TOKEN"
                exit 1
            }
        else
            log_error "No authentication method available for pushing"
            exit 1
        fi

        log_info "Successfully committed and pushed translated files"
    fi
else
    log_info "No files needed translation"
fi

log_info "Translation process completed"

