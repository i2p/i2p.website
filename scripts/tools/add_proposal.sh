#!/bin/bash
#
# I2P Proposal Tool
# Creates new proposal files for the I2P website with preview support
# Generates both .md (Hugo content) and .txt (RST source) files
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROPOSALS_MD_DIR="$PROJECT_ROOT/content/en/proposals"
PROPOSALS_TXT_DIR="$PROJECT_ROOT/static/proposals"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables for proposal data
PROP_NUMBER=""
PROP_NAME=""
PROP_DATE=""
PROP_AUTHOR=""
PROP_STATUS=""
PROP_THREAD=""
PROP_TARGET=""
PROP_CONTENT=""
HUGO_PID=""
TEMP_MD_FILE=""
TEMP_TXT_FILE=""

# Valid proposal statuses
STATUSES=(
    "Open"
    "Closed"
    "Rejected"
    "Draft"
    "Needs-Research"
    "Dead"
    "Meta"
    "Reserve"
)

show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║       I2P Proposal Tool                ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if we have a display (GUI environment)
has_display() {
    [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ] || [ "$OS" = "Windows_NT" ] || [ "$(uname)" = "Darwin" ]
}

# Generate slug from name
generate_slug() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | \
        sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//'
}

# Open URL in browser (cross-platform)
open_browser() {
    local url="$1"
    if [ "$OS" = "Windows_NT" ]; then
        start "$url" 2>/dev/null || cmd /c start "$url"
    elif [ "$(uname)" = "Darwin" ]; then
        open "$url"
    elif command -v xdg-open &>/dev/null; then
        xdg-open "$url"
    elif command -v gnome-open &>/dev/null; then
        gnome-open "$url"
    else
        echo -e "${YELLOW}Could not detect browser. Please open manually: $url${NC}"
        return 1
    fi
}

# Cleanup function
cleanup() {
    # Kill Hugo server if running
    if [ -n "$HUGO_PID" ] && kill -0 "$HUGO_PID" 2>/dev/null; then
        kill "$HUGO_PID" 2>/dev/null || true
    fi
    # Remove temp files if they exist and weren't saved
    if [ -n "$TEMP_MD_FILE" ] && [ -f "$TEMP_MD_FILE" ]; then
        rm -f "$TEMP_MD_FILE"
    fi
    if [ -n "$TEMP_TXT_FILE" ] && [ -f "$TEMP_TXT_FILE" ]; then
        rm -f "$TEMP_TXT_FILE"
    fi
    rm -rf /tmp/i2p-proposal-preview-* 2>/dev/null || true
}
trap cleanup EXIT

# Display status selection menu
select_status() {
    echo ""
    echo -e "${YELLOW}Select proposal status:${NC}"
    echo ""

    local i=1
    for status in "${STATUSES[@]}"; do
        echo -e "  ${CYAN}$i)${NC} $status"
        i=$((i + 1))
    done
    echo ""

    read -p "Status [1]: " status_input

    if [ -z "$status_input" ]; then
        status_input=1
    fi

    if [[ "$status_input" =~ ^[0-9]+$ ]] && [ "$status_input" -ge 1 ] && [ "$status_input" -le ${#STATUSES[@]} ]; then
        PROP_STATUS="${STATUSES[$((status_input-1))]}"
        echo -e "${GREEN}Selected: $PROP_STATUS${NC}"
        return 0
    else
        echo -e "${RED}Invalid selection. Defaulting to 'Open'${NC}"
        PROP_STATUS="Open"
        return 0
    fi
}

# Collect proposal metadata
collect_metadata() {
    echo ""
    echo -e "${YELLOW}Enter proposal details:${NC}"
    echo ""

    # Proposal Number (required)
    read -p "1. Proposal Number (e.g., 170): " PROP_NUMBER
    if [ -z "$PROP_NUMBER" ]; then
        echo -e "${RED}Error: Proposal number is required${NC}"
        return 1
    fi

    # Validate number format
    if ! [[ "$PROP_NUMBER" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}Error: Proposal number must be numeric${NC}"
        return 1
    fi

    # Proposal Name (required)
    read -p "2. Proposal Name: " PROP_NAME
    if [ -z "$PROP_NAME" ]; then
        echo -e "${RED}Error: Proposal name is required${NC}"
        return 1
    fi

    # Date (default: today)
    local default_date=$(date +%Y-%m-%d)
    read -p "3. Date [$default_date]: " PROP_DATE
    if [ -z "$PROP_DATE" ]; then
        PROP_DATE="$default_date"
    fi

    # Validate date format
    if ! [[ "$PROP_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}Error: Invalid date format. Use YYYY-MM-DD${NC}"
        return 1
    fi

    # Author(s) (required)
    read -p "4. Author(s) (comma-separated): " PROP_AUTHOR
    if [ -z "$PROP_AUTHOR" ]; then
        echo -e "${RED}Error: Author is required${NC}"
        return 1
    fi

    # Status (selection)
    if ! select_status; then
        return 1
    fi

    # Thread URL (optional)
    echo ""
    read -p "6. Thread URL (optional, e.g., http://zzz.i2p/topics/xxxx): " PROP_THREAD

    # Target version (optional)
    read -p "7. Target version (optional, e.g., 0.9.65): " PROP_TARGET

    return 0
}

# Collect proposal content - reads until two consecutive blank lines
collect_content() {
    echo ""
    echo -e "${YELLOW}Paste your proposal content (Markdown format).${NC}"
    echo -e "${YELLOW}Press Enter on a blank line ${CYAN}twice${YELLOW} when done:${NC}"
    echo ""

    PROP_CONTENT=""
    local empty_count=0
    local line

    while IFS= read -r line; do
        if [ -z "$line" ]; then
            empty_count=$((empty_count + 1))
            if [ $empty_count -ge 2 ]; then
                break
            fi
            # Add the single blank line to content (might be paragraph break)
            PROP_CONTENT+=$'\n'
        else
            empty_count=0
            PROP_CONTENT+="$line"$'\n'
        fi
    done

    # Trim trailing newlines
    PROP_CONTENT=$(printf '%s' "$PROP_CONTENT" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')

    if [ -z "$PROP_CONTENT" ]; then
        echo -e "${YELLOW}Warning: No content provided${NC}"
    else
        local line_count=$(printf '%s' "$PROP_CONTENT" | wc -l)
        echo -e "${GREEN}✓ Content captured: $line_count lines${NC}"
    fi

    return 0
}

# Generate the RST title line (equals signs matching title length)
generate_rst_title_line() {
    local title="$1"
    local len=${#title}
    printf '=%.0s' $(seq 1 $len)
}

# Generate the proposal .txt file content (RST format)
generate_txt() {
    local title_line=$(generate_rst_title_line "$PROP_NAME")

    cat << EOF
$title_line
$PROP_NAME
$title_line
.. meta::
    :author: $PROP_AUTHOR
    :created: $PROP_DATE
EOF

    # Add optional thread
    if [ -n "$PROP_THREAD" ]; then
        echo "    :thread: $PROP_THREAD"
    fi

    # Always add lastupdated (same as created initially)
    echo "    :lastupdated: $PROP_DATE"
    echo "    :status: $PROP_STATUS"

    # Add optional target
    if [ -n "$PROP_TARGET" ]; then
        echo "    :target: $PROP_TARGET"
    fi

    echo ""
    echo ".. contents::"
    echo ""
    echo ""

    # Convert markdown content to RST-style (basic conversion)
    # This is a simplified conversion - complex markdown may need manual adjustment
    echo "$PROP_CONTENT" | sed \
        -e 's/^## \(.*\)$/\1\n----------------------------------------/g' \
        -e 's/^### \(.*\)$/\1\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/g' \
        -e 's/^# \(.*\)$/\1\n========================================/g'
}

# Generate the proposal .md file content (Hugo format)
generate_md() {
    cat << EOF
---
title: "$PROP_NAME"
number: "$PROP_NUMBER"
author: "$PROP_AUTHOR"
created: "$PROP_DATE"
lastupdated: "$PROP_DATE"
status: "$PROP_STATUS"
EOF

    # Add optional thread
    if [ -n "$PROP_THREAD" ]; then
        echo "thread: \"$PROP_THREAD\""
    fi

    # Add optional target
    if [ -n "$PROP_TARGET" ]; then
        echo "target: \"$PROP_TARGET\""
    fi

    echo "toc: true"
    echo "---"
    echo ""
    echo "$PROP_CONTENT"
}

# Write temporary proposal files for preview
write_temp_files() {
    local slug=$(generate_slug "$PROP_NAME")
    TEMP_MD_FILE="$PROPOSALS_MD_DIR/$PROP_NUMBER-$slug.md"
    TEMP_TXT_FILE="$PROPOSALS_TXT_DIR/$PROP_NUMBER-$slug.txt"

    generate_md > "$TEMP_MD_FILE"
    generate_txt > "$TEMP_TXT_FILE"
}

# Check if pico.sh/pgs.sh account exists and prompt to create if needed
check_pgs_account() {
    # Try to connect to pgs.sh quietly - if it fails, user needs to set up account
    if ! ssh -o BatchMode=yes -o ConnectTimeout=5 pgs.sh ls >/dev/null 2>&1; then
        echo -e "${YELLOW}You need to set up a pico.sh account for preview hosting.${NC}"
        echo -e "${CYAN}This is a one-time setup using your SSH key.${NC}"
        echo ""
        read -p "Would you like to set up your account now? (y/n): " do_setup
        if [[ "$do_setup" =~ ^[Yy] ]]; then
            echo -e "${BLUE}Connecting to pico.sh...${NC}"
            echo -e "${YELLOW}Follow the prompts to choose a username, then exit when done.${NC}"
            echo ""
            ssh pico.sh
            echo ""
            # Verify it worked
            if ssh -o BatchMode=yes -o ConnectTimeout=5 pgs.sh ls >/dev/null 2>&1; then
                echo -e "${GREEN}Account setup successful!${NC}"
                return 0
            else
                echo -e "${RED}Account setup may have failed. Try running: ssh pico.sh${NC}"
                return 1
            fi
        else
            echo -e "${YELLOW}Skipping preview. You can set up later with: ssh pico.sh${NC}"
            return 1
        fi
    fi
    return 0
}

# Convert markdown to HTML (basic conversion)
markdown_to_html() {
    local content="$1"

    echo "$content" | sed \
        -e 's/^### \(.*\)$/<h3>\1<\/h3>/g' \
        -e 's/^## \(.*\)$/<h2>\1<\/h2>/g' \
        -e 's/^# \(.*\)$/<h1>\1<\/h1>/g' \
        -e 's/^---$/<hr>/g' \
        -e 's/^- \(.*\)$/<li>\1<\/li>/g' \
        -e 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g' \
        -e 's/\*\([^*]*\)\*/<em>\1<\/em>/g' \
        -e 's/`\([^`]*\)`/<code>\1<\/code>/g' | \
    awk '
        BEGIN { in_list = 0; in_p = 0 }
        /<li>/ {
            if (!in_list) { print "<ul>"; in_list = 1 }
            print; next
        }
        !/<li>/ && in_list { print "</ul>"; in_list = 0 }
        /^$/ {
            if (in_p) { print "</p>"; in_p = 0 }
            next
        }
        /^<h[1-6]>/ || /^<hr>/ || /^<ul>/ || /^<\/ul>/ { print; next }
        {
            if (!in_p && !/^</) { print "<p>"; in_p = 1 }
            print
        }
        END {
            if (in_list) print "</ul>"
            if (in_p) print "</p>"
        }
    '
}

# Generate TOC entries from markdown content
generate_toc_entries() {
    local content="$1"
    echo "$content" | awk '
        /^# [^#]/ {
            text = substr($0, 3)
            gsub(/^[ \t]+|[ \t]+$/, "", text)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<li><a href=\"#" id "\">" text "</a></li>"
        }
        /^## / {
            text = substr($0, 4)
            gsub(/^[ \t]+|[ \t]+$/, "", text)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<li><a href=\"#" id "\">" text "</a></li>"
        }
        /^### / {
            text = substr($0, 5)
            gsub(/^[ \t]+|[ \t]+$/, "", text)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<li><a href=\"#" id "\" class=\"toc-h3\">" text "</a></li>"
        }
    '
}

# Convert markdown to HTML with heading IDs for TOC links
markdown_to_html_with_ids() {
    local content="$1"
    echo "$content" | awk '
        BEGIN { in_code = 0; list_type = 0; in_p = 0 }

        # Helper to close current list
        function close_list() {
            if (list_type == 1) { print "</ul>"; list_type = 0 }
            else if (list_type == 2) { print "</ol>"; list_type = 0 }
        }

        # Code blocks
        /^```/ {
            if (in_code) {
                print "</code></pre>"
                in_code = 0
            } else {
                if (in_p) { print "</p>"; in_p = 0 }
                close_list()
                print "<pre><code>"
                in_code = 1
            }
            next
        }
        in_code { print; next }

        # Horizontal rules
        /^---+$/ || /^\*\*\*+$/ || /^___+$/ {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            print "<hr>"
            next
        }

        # Empty lines
        /^$/ {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            next
        }

        # H1 headings
        /^# / {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            text = substr($0, 3)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<h1 id=\"" id "\">" text "</h1>"
            next
        }

        # H2 headings
        /^## / {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            text = substr($0, 4)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<h2 id=\"" id "\">" text "</h2>"
            next
        }

        # H3 headings
        /^### / {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            text = substr($0, 5)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<h3 id=\"" id "\">" text "</h3>"
            next
        }

        # H4 headings
        /^#### / {
            if (in_p) { print "</p>"; in_p = 0 }
            close_list()
            text = substr($0, 6)
            id = tolower(text)
            gsub(/[^a-z0-9 -]/, "", id)
            gsub(/ +/, "-", id)
            print "<h4 id=\"" id "\">" text "</h4>"
            next
        }

        # Unordered list items
        /^- / || /^\* / {
            if (in_p) { print "</p>"; in_p = 0 }
            # Switch list type if needed
            if (list_type == 2) { print "</ol>"; list_type = 0 }
            if (list_type != 1) { print "<ul>"; list_type = 1 }
            text = substr($0, 3)
            gsub(/\*\*([^*]+)\*\*/, "<strong>\\1</strong>", text)
            gsub(/\*([^*]+)\*/, "<em>\\1</em>", text)
            gsub(/`([^`]+)`/, "<code>\\1</code>", text)
            print "<li>" text "</li>"
            next
        }

        # Ordered list items
        /^[0-9]+\. / {
            if (in_p) { print "</p>"; in_p = 0 }
            # Switch list type if needed
            if (list_type == 1) { print "</ul>"; list_type = 0 }
            if (list_type != 2) { print "<ol>"; list_type = 2 }
            match($0, /^[0-9]+\. /)
            text = substr($0, RLENGTH + 1)
            gsub(/\*\*([^*]+)\*\*/, "<strong>\\1</strong>", text)
            gsub(/\*([^*]+)\*/, "<em>\\1</em>", text)
            gsub(/`([^`]+)`/, "<code>\\1</code>", text)
            print "<li>" text "</li>"
            next
        }

        # Regular paragraphs
        {
            close_list()
            # Apply inline formatting
            gsub(/\*\*([^*]+)\*\*/, "<strong>\\1</strong>")
            gsub(/\*([^*]+)\*/, "<em>\\1</em>")
            gsub(/`([^`]+)`/, "<code>\\1</code>")
            if (!in_p) { print "<p>"; in_p = 1 }
            print
        }

        END {
            close_list()
            if (in_p) print "</p>"
        }
    '
}

# Generate full-site HTML preview with header, nav, and footer for proposals
generate_preview_html() {
    local content_html=$(markdown_to_html_with_ids "$PROP_CONTENT")
    local toc_entries=$(generate_toc_entries "$PROP_CONTENT")
    local formatted_date=$(date -j -f "%Y-%m-%d" "$PROP_DATE" "+%B %d, %Y" 2>/dev/null || echo "$PROP_DATE")

    # Build HTML with full site layout
    cat << EOF
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposal $PROP_NUMBER: $PROP_NAME | I2P Preview</title>
    <style>
        /* CSS Variables - Design Tokens */
        :root {
            --color-primary: #1e40af;
            --color-primary-hover: #1e3a8a;
            --color-secondary: #7c3aed;
            --color-accent: #0891b2;
            --color-bg: #ffffff;
            --color-bg-secondary: #f8fafc;
            --color-bg-tertiary: #e2e8f0;
            --color-text: #1e293b;
            --color-text-secondary: #475569;
            --color-text-muted: #64748b;
            --color-border: #e2e8f0;
            --color-border-hover: #cbd5e1;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
            --spacing-2xl: 3rem;
            --spacing-3xl: 4rem;
            --radius-sm: 0.25rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --transition-fast: 150ms ease-in-out;
            --transition-base: 250ms ease-in-out;
            --container-max: 1280px;
            --header-height: 88px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { font-size: 16px; scroll-behavior: smooth; }
        body {
            font-family: var(--font-sans);
            font-size: 1.1rem;
            line-height: 1.6;
            color: var(--color-text);
            background-color: var(--color-bg);
        }
        h1, h2, h3, h4, h5, h6 { font-weight: 700; line-height: 1.2; margin-bottom: var(--spacing-md); }
        a { color: var(--color-primary); text-decoration: none; }
        a:hover { color: var(--color-primary-hover); }
        .container { max-width: var(--container-max); margin: 0 auto; padding: 0 var(--spacing-lg); }
        main { min-height: calc(100vh - var(--header-height) - 300px); }

        /* Preview Banner */
        .preview-banner {
            background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
            color: white;
            padding: var(--spacing-sm) var(--spacing-md);
            text-align: center;
            font-size: 0.875rem;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 1002;
        }

        /* Header */
        .site-header {
            background-color: rgba(255, 255, 255, 0.9);
            border-bottom: 1px solid var(--color-border);
            position: sticky;
            top: 35px;
            z-index: 1000;
            height: var(--header-height);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-md);
        }
        .main-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: var(--header-height);
        }
        .nav-brand { display: flex; align-items: center; }
        .logo-link { display: flex; align-items: center; text-decoration: none; }
        .logo { height: 70px; width: auto; padding: 10px; }
        .nav-menu { display: flex; align-items: center; gap: var(--spacing-2xl); }
        .nav-links { display: flex; gap: var(--spacing-sm); list-style: none; }
        .nav-links a {
            color: var(--color-text-secondary);
            font-weight: 500;
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--radius-md);
            transition: color var(--transition-fast), background-color var(--transition-fast);
        }
        .nav-links a:hover, .nav-links a.active {
            color: var(--color-primary);
            background-color: var(--color-bg-secondary);
        }
        .nav-actions { display: flex; align-items: center; gap: var(--spacing-sm); }
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.625rem 1.5rem;
            font-weight: 600;
            border-radius: var(--radius-md);
            cursor: pointer;
            border: none;
            font-size: 0.9375rem;
            text-decoration: none;
        }
        .btn-primary {
            background-color: #3D83F7;
            color: white;
            height: 39px;
            padding: 0 1.25rem;
        }
        .btn-primary:hover { background-color: #2563eb; color: white; }
        .btn-donate {
            background-color: #8b5cf6;
            color: white;
            height: 39px;
            padding: 0 1.25rem;
        }
        .btn-donate:hover { background-color: #7c3aed; color: white; }
        .language-toggle, .theme-toggle {
            background: none;
            border: 1px solid var(--color-border);
            width: 40px;
            height: 40px;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--color-text);
        }
        .language-toggle {
            width: auto;
            padding: 0 var(--spacing-md);
            gap: var(--spacing-sm);
            font-weight: 600;
            font-size: 0.875rem;
        }

        /* Proposal Page Styles */
        .single-page { padding: var(--spacing-2xl) 0; }
        .page-header {
            margin-bottom: var(--spacing-2xl);
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
        }
        .breadcrumb {
            font-size: 0.875rem;
            color: var(--color-text-muted);
            margin-bottom: var(--spacing-lg);
        }
        .breadcrumb a { color: var(--color-text-muted); }
        .breadcrumb a:hover { color: var(--color-primary); }
        .breadcrumb .separator { margin: 0 var(--spacing-sm); }
        .page-title { font-size: 2.5rem; margin-bottom: var(--spacing-md); line-height: 1.2; }
        .proposal-number {
            color: var(--color-text-muted);
            font-size: 1rem;
            font-weight: normal;
            display: block;
            margin-bottom: var(--spacing-xs);
        }
        .page-meta {
            display: flex;
            gap: var(--spacing-lg);
            font-size: 0.9375rem;
            color: var(--color-text-muted);
            margin-bottom: var(--spacing-md);
        }
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background-color: var(--color-primary);
            color: white;
            border-radius: var(--radius-sm);
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        /* Two-column layout with TOC sidebar */
        .content-wrapper {
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: var(--spacing-2xl);
            align-items: start;
            max-width: 1200px;
            margin: 0 auto;
        }
        .toc-sidebar {
            position: sticky;
            top: 140px;
            max-height: calc(100vh - 160px);
            overflow-y: auto;
        }
        .toc-nav {
            background: var(--color-bg-secondary);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            padding: var(--spacing-md);
        }
        .toc-header {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            font-weight: 700;
            font-size: 0.875rem;
            color: var(--color-text);
            padding-bottom: var(--spacing-md);
            margin-bottom: var(--spacing-md);
            border-bottom: 1px solid var(--color-border);
        }
        .toc-header svg {
            flex-shrink: 0;
        }
        .toc-content {
            max-height: calc(100vh - 280px);
            overflow-y: auto;
        }
        .toc-content::-webkit-scrollbar { width: 4px; }
        .toc-content::-webkit-scrollbar-track { background: transparent; }
        .toc-content::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 2px; }
        .toc-content::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
        .toc-nav ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .toc-nav li {
            margin-bottom: 0.25rem;
        }
        .toc-nav ul ul {
            padding-left: var(--spacing-md);
            margin-top: 0.25rem;
        }
        .toc-nav a {
            color: var(--color-text-secondary);
            text-decoration: none;
            font-size: 0.8125rem;
            display: block;
            padding: 0.25rem 0.5rem;
            border-radius: var(--radius-sm);
            transition: all var(--transition-fast);
            line-height: 1.4;
        }
        .toc-nav a:hover {
            color: var(--color-primary);
            background: var(--color-bg-tertiary);
        }
        .toc-nav a.active {
            color: var(--color-primary);
            background: var(--color-bg-tertiary);
            font-weight: 600;
        }
        .toc-nav .toc-h3 {
            padding-left: var(--spacing-md);
            font-size: 0.75rem;
        }

        .page-content {
            flex: 1;
            min-width: 0;
            max-width: 800px;
            line-height: 1.8;
            font-size: 1.0625rem;
        }
        .page-content h1, .page-content h2, .page-content h3, .page-content h4 {
            margin-top: var(--spacing-2xl);
            margin-bottom: var(--spacing-md);
            scroll-margin-top: 150px;
        }
        .page-content h1 {
            font-size: 2rem;
            padding-bottom: var(--spacing-sm);
            border-bottom: 3px solid var(--color-primary);
        }
        .page-content h1:first-child { margin-top: 0; }
        .page-content h2 {
            font-size: 1.875rem;
            padding-bottom: var(--spacing-sm);
            border-bottom: 2px solid var(--color-border);
        }
        .page-content h3 { font-size: 1.5rem; }
        .page-content h4 { font-size: 1.25rem; }
        .page-content p { margin-bottom: var(--spacing-md); }
        .page-content hr {
            border: none;
            border-top: 1px solid var(--color-border);
            margin: var(--spacing-2xl) 0;
        }
        .page-content ul, .page-content ol {
            margin-bottom: var(--spacing-md);
            padding-left: var(--spacing-xl);
        }
        .page-content li { margin-bottom: var(--spacing-sm); }
        .page-content pre {
            background-color: var(--color-bg-secondary);
            padding: var(--spacing-lg);
            border-radius: var(--radius-md);
            overflow-x: auto;
            margin: var(--spacing-lg) 0;
            border: 1px solid var(--color-border);
        }
        .page-content code {
            font-family: var(--font-mono);
            font-size: 0.875em;
            background-color: var(--color-bg-tertiary);
            padding: 0.125rem 0.375rem;
            border-radius: var(--radius-sm);
        }
        .page-content pre code { background-color: transparent; padding: 0; }

        /* Footer */
        .site-footer {
            background-color: var(--color-bg-secondary);
            border-top: 1px solid var(--color-border);
            padding: var(--spacing-3xl) 0 var(--spacing-xl);
            margin-top: var(--spacing-3xl);
        }
        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: var(--spacing-2xl);
            margin-bottom: var(--spacing-2xl);
        }
        .footer-col h3 { font-size: 1rem; margin-bottom: var(--spacing-md); }
        .footer-col ul { list-style: none; }
        .footer-col li { margin-bottom: var(--spacing-sm); }
        .footer-col a { color: var(--color-text-secondary); font-size: 0.9375rem; }
        .footer-col a:hover { color: var(--color-primary); }
        .footer-tagline { font-weight: 600; margin-bottom: var(--spacing-sm); }
        .footer-description { color: var(--color-text-secondary); font-size: 0.9375rem; margin-bottom: var(--spacing-lg); }
        .footer-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: var(--spacing-xl);
            border-top: 1px solid var(--color-border);
        }
        .copyright { color: var(--color-text-muted); font-size: 0.875rem; }
        .footer-links { display: flex; gap: var(--spacing-lg); }
        .footer-links a { color: var(--color-text-muted); font-size: 0.875rem; }

        @media (max-width: 968px) {
            .footer-grid { grid-template-columns: 1fr 1fr; }
            .footer-brand { grid-column: 1 / -1; }
        }
        @media (max-width: 1024px) {
            .content-wrapper { grid-template-columns: 1fr; }
            .toc-sidebar {
                position: static;
                max-height: none;
                margin-bottom: var(--spacing-xl);
            }
            .toc-content { max-height: 300px; }
        }
        @media (max-width: 768px) {
            .nav-menu { display: none; }
            .page-title { font-size: 2rem; }
            .page-content { font-size: 1rem; }
            .page-meta { flex-direction: column; gap: var(--spacing-sm); }
            .footer-grid { grid-template-columns: 1fr; }
            .footer-bottom { flex-direction: column; gap: var(--spacing-md); text-align: center; }
        }
    </style>
</head>
<body>
    <!-- Preview Banner -->
    <div class="preview-banner">
        PREVIEW MODE - This is how your proposal will look on the live site
    </div>

    <!-- Site Header -->
    <header class="site-header">
        <div class="container">
            <nav class="main-nav">
                <div class="nav-brand">
                    <a href="#" class="logo-link">
                        <svg class="logo" viewBox="0 0 505.38 142.54" xmlns="http://www.w3.org/2000/svg">
                            <g><rect x="12.71" y="14.08" width="24.44" height="116.65"/><path d="M134.16,110.17l-.3,20.56H52.5v-17.62c29-29.06,53.83-48.73,53.83-65.12,0-11-4.74-15.97-15.8-15.97-8.4,0-19.27,6.55-25.24,12.52l-13.23-15.52c10.95-11.93,24.21-16.09,36.68-17.03,25.27-1.91,41.15,11.57,41.15,33.47,0,19.16-27.93,45.52-48.39,64.71h52.66Z"/><path d="M147.62,14.08h38.39c23.48,0,41.73,8.73,41.73,37.09s-20.03,38.47-41.74,38.65l-13.89-.09v41.01h-24.49V14.08ZM184.58,70.21c13.42,0,19.79-6.48,19.79-18.61s-6.9-16.56-19.79-16.56h-12.48v35.17h12.48Z"/></g>
                            <g><circle fill="#60ab60" cx="271.21" cy="40" r="27.06"/><circle fill="#ffc434" cx="336.68" cy="40" r="27.06"/><circle fill="#60ab60" cx="401.15" cy="40" r="27.06"/><circle fill="#e15647" cx="465.62" cy="40" r="27.06"/><circle fill="#ffc434" cx="271.21" cy="102.54" r="27.06"/><circle fill="#e15647" cx="336.68" cy="102.54" r="27.06"/><circle fill="#ffc434" cx="401.15" cy="102.54" r="27.06"/><circle fill="#60ab60" cx="465.62" cy="102.54" r="27.06"/></g>
                        </svg>
                    </a>
                </div>
                <div class="nav-menu">
                    <ul class="nav-links">
                        <li><a href="#">About</a></li>
                        <li><a href="#" class="active">Docs</a></li>
                        <li><a href="#">Downloads</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Get Involved</a></li>
                    </ul>
                    <div class="nav-actions">
                        <button class="language-toggle">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" stroke="currentColor" stroke-width="2"/></svg>
                            <span>en</span>
                        </button>
                        <button class="theme-toggle">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
                        </button>
                        <a href="#" class="btn btn-donate">Donate</a>
                        <a href="#" class="btn btn-primary">Get I2P</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main id="main-content">
        <article class="single-page">
            <div class="container">
                <div class="page-header">
                    <nav class="breadcrumb" aria-label="breadcrumb">
                        <a href="#">Home</a>
                        <span class="separator">&rarr;</span>
                        <a href="#">Docs</a>
                        <span class="separator">&rarr;</span>
                        <a href="#">Proposals</a>
                        <span class="separator">&rarr;</span>
                        <span class="current">Proposal $PROP_NUMBER</span>
                    </nav>
                    <h1 class="page-title">
                        <span class="proposal-number">Proposal #$PROP_NUMBER</span>
                        $PROP_NAME
                    </h1>
                    <div class="page-meta">
                        <span>$formatted_date</span>
                        <span>By $PROP_AUTHOR</span>
                        <span class="status-badge">$PROP_STATUS</span>
                    </div>
                </div>
                <div class="content-wrapper">
                    <aside class="toc-sidebar">
                        <nav class="toc-nav">
                            <div class="toc-header">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                                    <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                </svg>
                                On This Page
                            </div>
                            <div class="toc-content">
                                <ul>
                                    $toc_entries
                                </ul>
                            </div>
                        </nav>
                    </aside>
                    <div class="page-content">
                        $content_html
                    </div>
                </div>
            </div>
        </article>
    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col footer-brand">
                    <p class="footer-tagline">The Invisible Internet Project</p>
                    <p class="footer-description">A privacy-focused anonymous network layer.</p>
                </div>
                <div class="footer-col">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="#">Donate</a></li>
                        <li><a href="#">I2P Introduction</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Community</h3>
                    <ul>
                        <li><a href="#">Get Involved</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Forums</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Resources</h3>
                    <ul>
                        <li><a href="#">I2P Metrics</a></li>
                        <li><a href="#">Research</a></li>
                        <li><a href="#">GitLab</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p class="copyright">&copy; 2025 The I2P Project</p>
                <div class="footer-links">
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                    <a href="#">Press</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Highlight active TOC item on scroll
        document.addEventListener('DOMContentLoaded', function() {
            const tocLinks = document.querySelectorAll('.toc-sidebar a');
            const headings = document.querySelectorAll('.page-content h2[id], .page-content h3[id], .page-content h4[id]');

            function updateActiveTocItem() {
                let current = '';
                headings.forEach(heading => {
                    const rect = heading.getBoundingClientRect();
                    if (rect.top <= 160) {
                        current = heading.getAttribute('id');
                    }
                });

                tocLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + current) {
                        link.classList.add('active');
                    }
                });
            }

            window.addEventListener('scroll', updateActiveTocItem);
            updateActiveTocItem();
        });
    </script>
</body>
</html>
EOF
}

# Preview with pgs.sh (uses rsync over SSH)
preview_pgs() {
    echo ""

    # Check for SSH
    if ! command -v ssh &>/dev/null; then
        echo -e "${RED}Error: SSH is required for pgs.sh hosting${NC}"
        return 1
    fi

    # Check pgs.sh account - only prompt after user confirms they want preview
    if ! check_pgs_account; then
        echo -e "${YELLOW}pgs.sh account required for preview.${NC}"
        return 1
    fi

    echo -e "${CYAN}Generating and uploading preview...${NC}"

    local preview_dir="/tmp/i2p-proposal-preview-$$"
    local project_name="i2p-prop-preview"
    mkdir -p "$preview_dir"

    # Generate standalone HTML preview
    generate_preview_html > "$preview_dir/index.html"

    # Upload using rsync to pgs.sh - capture output to extract URL
    local rsync_output
    if rsync_output=$(rsync -r "$preview_dir/" "pgs.sh:/$project_name/" 2>&1); then
        # Extract the URL from rsync output (looks for https://...pgs.sh/...)
        local preview_url=$(echo "$rsync_output" | grep -o 'https://[^[:space:]]*pgs\.sh[^[:space:]]*' | head -1)

        echo ""
        echo -e "${GREEN}════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Preview Ready!${NC}"
        echo -e "${GREEN}════════════════════════════════════════${NC}"
        echo ""
        if [ -n "$preview_url" ]; then
            echo -e "  ${CYAN}$preview_url${NC}"
        else
            echo -e "  ${CYAN}https://YOUR-USERNAME-${project_name}.pgs.sh/${NC}"
        fi
        echo ""
    else
        echo -e "${RED}Failed to upload to pgs.sh${NC}"
        echo -e "${YELLOW}Make sure you have an account: ssh pico.sh${NC}"
    fi

    # Cleanup preview dir
    rm -rf "$preview_dir"
}

# Show terminal preview (fallback)
show_terminal_preview() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Terminal Preview (Markdown):${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    generate_md | head -50
    echo ""
    if [ $(generate_md | wc -l) -gt 50 ]; then
        echo -e "${YELLOW}... (content truncated)${NC}"
    fi
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Terminal Preview (RST):${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    generate_txt | head -30
    echo ""
    if [ $(generate_txt | wc -l) -gt 30 ]; then
        echo -e "${YELLOW}... (content truncated)${NC}"
    fi
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

# Start preview - uses pgs.sh for hosting
start_preview() {
    preview_pgs
}

# Show proposal summary
show_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Proposal Summary:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Number:      ${GREEN}$PROP_NUMBER${NC}"
    echo -e "  Name:        ${GREEN}$PROP_NAME${NC}"
    echo -e "  Date:        ${GREEN}$PROP_DATE${NC}"
    echo -e "  Author(s):   ${GREEN}$PROP_AUTHOR${NC}"
    echo -e "  Status:      ${GREEN}$PROP_STATUS${NC}"
    if [ -n "$PROP_THREAD" ]; then
        echo -e "  Thread:      ${GREEN}$PROP_THREAD${NC}"
    fi
    if [ -n "$PROP_TARGET" ]; then
        echo -e "  Target:      ${GREEN}$PROP_TARGET${NC}"
    fi
    local slug=$(generate_slug "$PROP_NAME")
    echo -e "  MD File:     ${GREEN}$PROP_NUMBER-$slug.md${NC}"
    echo -e "  TXT File:    ${GREEN}$PROP_NUMBER-$slug.txt${NC}"
    local content_lines=$(echo "$PROP_CONTENT" | wc -l)
    echo -e "  Content:     ${GREEN}$content_lines lines${NC}"
    echo ""
}

# Save the final proposal files
save_proposal() {
    local slug=$(generate_slug "$PROP_NAME")
    local md_filename="$PROP_NUMBER-$slug.md"
    local txt_filename="$PROP_NUMBER-$slug.txt"
    local md_filepath="$PROPOSALS_MD_DIR/$md_filename"
    local txt_filepath="$PROPOSALS_TXT_DIR/$txt_filename"

    # Check for existing files
    local overwrite_needed=false
    if [ -f "$md_filepath" ] && [ "$md_filepath" != "$TEMP_MD_FILE" ]; then
        overwrite_needed=true
    fi
    if [ -f "$txt_filepath" ] && [ "$txt_filepath" != "$TEMP_TXT_FILE" ]; then
        overwrite_needed=true
    fi

    if [ "$overwrite_needed" = true ]; then
        read -p "Proposal files already exist. Overwrite? (y/n): " confirm
        if [[ ! "$confirm" =~ ^[Yy] ]]; then
            echo -e "${YELLOW}Save cancelled${NC}"
            return 1
        fi
    fi

    # Write the final files
    generate_md > "$md_filepath"
    generate_txt > "$txt_filepath"

    # Clear temp file references since they're now the real files
    TEMP_MD_FILE=""
    TEMP_TXT_FILE=""

    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Proposal files saved successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  MD File:  ${CYAN}$md_filepath${NC}"
    echo -e "  TXT File: ${CYAN}$txt_filepath${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review changes: ${YELLOW}git diff content/en/proposals/ static/proposals/${NC}"
    echo -e "  2. Rebuild site:   ${YELLOW}hugo${NC}"
    echo -e "  3. Commit changes: ${YELLOW}git add -A && git commit -m \"Add proposal $PROP_NUMBER: $PROP_NAME\"${NC}"
    echo ""

    return 0
}

# Edit metadata
edit_metadata() {
    echo ""
    echo -e "${YELLOW}Which field to edit?${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} Number"
    echo -e "  ${CYAN}2)${NC} Name"
    echo -e "  ${CYAN}3)${NC} Date"
    echo -e "  ${CYAN}4)${NC} Author(s)"
    echo -e "  ${CYAN}5)${NC} Status"
    echo -e "  ${CYAN}6)${NC} Thread URL"
    echo -e "  ${CYAN}7)${NC} Target version"
    echo -e "  ${CYAN}8)${NC} Back"
    echo ""

    read -p "Select: " field

    case $field in
        1)
            read -p "New number [$PROP_NUMBER]: " new_val
            if [ -n "$new_val" ]; then
                if [[ "$new_val" =~ ^[0-9]+$ ]]; then
                    PROP_NUMBER="$new_val"
                else
                    echo -e "${RED}Invalid number format${NC}"
                fi
            fi
            ;;
        2)
            read -p "New name [$PROP_NAME]: " new_val
            [ -n "$new_val" ] && PROP_NAME="$new_val"
            ;;
        3)
            read -p "New date [$PROP_DATE]: " new_val
            if [ -n "$new_val" ]; then
                if [[ "$new_val" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                    PROP_DATE="$new_val"
                else
                    echo -e "${RED}Invalid date format${NC}"
                fi
            fi
            ;;
        4)
            read -p "New author(s) [$PROP_AUTHOR]: " new_val
            [ -n "$new_val" ] && PROP_AUTHOR="$new_val"
            ;;
        5)
            select_status
            ;;
        6)
            read -p "New thread URL: " new_val
            PROP_THREAD="$new_val"
            ;;
        7)
            read -p "New target version: " new_val
            PROP_TARGET="$new_val"
            ;;
        8)
            return 0
            ;;
    esac
}

# Post-preview menu loop
preview_menu() {
    while true; do
        echo ""
        echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║         Proposal Actions               ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${CYAN}1)${NC} Save Proposal"
        echo -e "  ${CYAN}2)${NC} Edit Content (re-paste)"
        echo -e "  ${CYAN}3)${NC} Edit Metadata"
        echo -e "  ${CYAN}4)${NC} Preview Again"
        echo -e "  ${CYAN}5)${NC} Show Summary"
        echo -e "  ${CYAN}6)${NC} Discard and Exit"
        echo ""

        read -p "Select option: " choice

        case $choice in
            1)
                if save_proposal; then
                    return 0
                fi
                ;;
            2)
                collect_content
                ;;
            3)
                edit_metadata
                ;;
            4)
                start_preview
                ;;
            5)
                show_summary
                ;;
            6)
                read -p "Are you sure you want to discard? (y/n): " confirm
                if [[ "$confirm" =~ ^[Yy] ]]; then
                    echo -e "${YELLOW}Discarded.${NC}"
                    return 0
                fi
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
    done
}

# Main function
main() {
    show_header

    # Check for hugo
    if ! command -v hugo &>/dev/null; then
        echo -e "${YELLOW}Warning: Hugo not found. Preview will be limited.${NC}"
    fi

    # Collect metadata
    if ! collect_metadata; then
        exit 1
    fi

    # Collect content
    collect_content

    # Show summary
    show_summary

    # Ask to preview
    read -p "Would you like to preview? (y/n): " do_preview
    if [[ "$do_preview" =~ ^[Yy] ]]; then
        start_preview
    fi

    # Enter the action menu
    preview_menu
}

main
