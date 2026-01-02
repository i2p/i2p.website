#!/bin/bash
#
# I2P Blog Post Tool
# Creates new blog posts for the I2P website with preview support
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BLOG_DIR="$PROJECT_ROOT/content/en/blog"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables for post data
POST_TITLE=""
POST_DATE=""
POST_AUTHOR=""
POST_CATEGORIES=()
POST_DESCRIPTION=""
POST_SLUG=""
POST_CONTENT=""
HUGO_PID=""
TEMP_POST_FILE=""

# Available categories
CATEGORIES=(
    "release"
    "news"
    "meeting"
    "status"
    "development"
    "community"
    "security"
    "tutorial"
    "conferences"
    "press"
    "roadmap"
    "general"
)

show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║       I2P Blog Post Tool               ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if we have a display (GUI environment)
has_display() {
    [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ] || [ "$OS" = "Windows_NT" ] || [ "$(uname)" = "Darwin" ]
}

# Generate slug from title
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

# Wait for Hugo server to be ready
wait_for_hugo() {
    local max_attempts=30
    local attempt=0
    echo -n "Waiting for Hugo server"
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:1313 >/dev/null 2>&1; then
            echo -e " ${GREEN}ready!${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        ((attempt++))
    done
    echo -e " ${RED}timeout${NC}"
    return 1
}

# Cleanup function
cleanup() {
    # Kill Hugo server if running
    if [ -n "$HUGO_PID" ] && kill -0 "$HUGO_PID" 2>/dev/null; then
        kill "$HUGO_PID" 2>/dev/null || true
    fi
    # Remove temp files
    if [ -n "$TEMP_POST_FILE" ] && [ -f "$TEMP_POST_FILE" ]; then
        rm -f "$TEMP_POST_FILE"
    fi
    rm -rf /tmp/i2p-blog-preview-* 2>/dev/null || true
}
trap cleanup EXIT

# Display category selection menu
select_categories() {
    echo ""
    echo -e "${YELLOW}Select categories (enter numbers separated by commas, e.g., 1,3,5):${NC}"
    echo ""

    local i=1
    for cat in "${CATEGORIES[@]}"; do
        echo -e "  ${CYAN}$i)${NC} $cat"
        ((i++))
    done
    echo -e "  ${CYAN}0)${NC} Enter custom category"
    echo ""

    read -p "Categories: " cat_input

    if [ -z "$cat_input" ]; then
        echo -e "${RED}Error: At least one category is required${NC}"
        return 1
    fi

    POST_CATEGORIES=()
    IFS=',' read -ra SELECTIONS <<< "$cat_input"

    for sel in "${SELECTIONS[@]}"; do
        sel=$(echo "$sel" | tr -d ' ')
        if [ "$sel" = "0" ]; then
            read -p "Enter custom category: " custom_cat
            if [ -n "$custom_cat" ]; then
                POST_CATEGORIES+=("$custom_cat")
            fi
        elif [[ "$sel" =~ ^[0-9]+$ ]] && [ "$sel" -ge 1 ] && [ "$sel" -le ${#CATEGORIES[@]} ]; then
            POST_CATEGORIES+=("${CATEGORIES[$((sel-1))]}")
        else
            echo -e "${YELLOW}Warning: Invalid selection '$sel' ignored${NC}"
        fi
    done

    if [ ${#POST_CATEGORIES[@]} -eq 0 ]; then
        echo -e "${RED}Error: No valid categories selected${NC}"
        return 1
    fi

    echo -e "${GREEN}Selected: ${POST_CATEGORIES[*]}${NC}"
    return 0
}

# Collect post metadata
collect_metadata() {
    echo ""
    echo -e "${YELLOW}Enter blog post details:${NC}"
    echo ""

    # Title (required)
    read -p "1. Title: " POST_TITLE
    if [ -z "$POST_TITLE" ]; then
        echo -e "${RED}Error: Title is required${NC}"
        return 1
    fi

    # Date (default: today)
    local default_date=$(date +%Y-%m-%d)
    read -p "2. Date [$default_date]: " POST_DATE
    if [ -z "$POST_DATE" ]; then
        POST_DATE="$default_date"
    fi

    # Validate date format
    if ! [[ "$POST_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}Error: Invalid date format. Use YYYY-MM-DD${NC}"
        return 1
    fi

    # Author (required)
    read -p "3. Author: " POST_AUTHOR
    if [ -z "$POST_AUTHOR" ]; then
        echo -e "${RED}Error: Author is required${NC}"
        return 1
    fi

    # Categories (multi-select)
    if ! select_categories; then
        return 1
    fi

    # Description (optional)
    echo ""
    read -p "5. Description (1-2 sentences, optional): " POST_DESCRIPTION

    # Slug (auto-generated with override option)
    local auto_slug=$(generate_slug "$POST_TITLE")
    echo ""
    read -p "6. Slug [$auto_slug]: " POST_SLUG
    if [ -z "$POST_SLUG" ]; then
        POST_SLUG="$auto_slug"
    fi

    return 0
}

# Collect post content - reads until two consecutive blank lines
collect_content() {
    echo ""
    echo -e "${YELLOW}Paste your blog post content (Markdown format).${NC}"
    echo -e "${YELLOW}Press Enter on a blank line ${CYAN}twice${YELLOW} when done:${NC}"
    echo ""

    POST_CONTENT=""
    local empty_count=0
    local line

    while IFS= read -r line; do
        if [ -z "$line" ]; then
            empty_count=$((empty_count + 1))
            if [ $empty_count -ge 2 ]; then
                break
            fi
            # Add the single blank line to content (might be paragraph break)
            POST_CONTENT+=$'\n'
        else
            empty_count=0
            POST_CONTENT+="$line"$'\n'
        fi
    done

    # Trim trailing newlines
    POST_CONTENT=$(printf '%s' "$POST_CONTENT" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')

    if [ -z "$POST_CONTENT" ]; then
        echo -e "${YELLOW}Warning: No content provided${NC}"
    else
        local line_count=$(printf '%s' "$POST_CONTENT" | wc -l)
        echo -e "${GREEN}✓ Content captured: $line_count lines${NC}"
    fi

    return 0
}

# Generate the blog post file content
generate_post() {
    local categories_yaml=""
    for cat in "${POST_CATEGORIES[@]}"; do
        categories_yaml+="\"$cat\", "
    done
    categories_yaml=$(echo "$categories_yaml" | sed 's/, $//')

    cat << EOF
---
title: "$POST_TITLE"
date: $POST_DATE
author: $POST_AUTHOR
categories: [$categories_yaml]
description: "$POST_DESCRIPTION"
---

$POST_CONTENT
EOF
}

# Write temporary post file for preview
write_temp_post() {
    TEMP_POST_FILE="$BLOG_DIR/$POST_DATE-$POST_SLUG.md"
    generate_post > "$TEMP_POST_FILE"
}

# Preview with local Hugo server (GUI)
preview_local() {
    echo ""
    echo -e "${CYAN}Starting Hugo preview server...${NC}"

    # Kill any existing Hugo server
    if [ -n "$HUGO_PID" ] && kill -0 "$HUGO_PID" 2>/dev/null; then
        kill "$HUGO_PID" 2>/dev/null || true
        sleep 1
    fi

    # Write temp post
    write_temp_post

    # Start Hugo server in background
    cd "$PROJECT_ROOT"
    hugo server -D --navigateToChanged >/dev/null 2>&1 &
    HUGO_PID=$!

    if ! wait_for_hugo; then
        echo -e "${RED}Failed to start Hugo server${NC}"
        return 1
    fi

    # Generate preview URL
    local year=$(echo "$POST_DATE" | cut -d'-' -f1)
    local month=$(echo "$POST_DATE" | cut -d'-' -f2)
    local day=$(echo "$POST_DATE" | cut -d'-' -f3)
    local preview_url="http://localhost:1313/en/blog/$year/$month/$day/$POST_SLUG/"

    echo -e "${GREEN}Preview URL: $preview_url${NC}"

    if has_display; then
        echo -e "${CYAN}Opening in browser...${NC}"
        open_browser "$preview_url"
    fi

    return 0
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

    # Process the markdown line by line
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

# Generate full-site HTML preview with header, nav, and footer
generate_preview_html() {
    local content_html=$(markdown_to_html "$POST_CONTENT")
    local formatted_date=$(date -j -f "%Y-%m-%d" "$POST_DATE" "+%B %d, %Y" 2>/dev/null || echo "$POST_DATE")

    local categories_html=""
    for cat in "${POST_CATEGORIES[@]}"; do
        categories_html+="<span class=\"category-badge\">$cat</span> "
    done

    # Build HTML with full site layout
    cat << EOF
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$POST_TITLE | I2P Blog Preview</title>
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

        /* Blog Post Styles */
        .blog-post { padding: var(--spacing-2xl) 0; }
        .post-header {
            margin-bottom: var(--spacing-2xl);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            padding-bottom: var(--spacing-xl);
            border-bottom: 1px solid var(--color-border);
        }
        .post-meta-row {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-md);
        }
        .post-date {
            font-size: 0.8125rem;
            color: var(--color-text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .post-categories { display: flex; gap: var(--spacing-xs); }
        .category-badge {
            padding: 0.25rem 0.625rem;
            background-color: var(--color-primary);
            color: white;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .post-title { font-size: 2.5rem; margin-bottom: var(--spacing-sm); line-height: 1.2; }
        .post-author { font-size: 0.9375rem; color: var(--color-text-secondary); }
        .post-content {
            max-width: 800px;
            margin: 0 auto var(--spacing-2xl);
            line-height: 1.8;
            font-size: 1.0625rem;
        }
        .post-content h2, .post-content h3, .post-content h4 {
            margin-top: var(--spacing-2xl);
            margin-bottom: var(--spacing-md);
        }
        .post-content h2 {
            font-size: 1.875rem;
            padding-bottom: var(--spacing-sm);
            border-bottom: 2px solid var(--color-border);
        }
        .post-content h3 { font-size: 1.5rem; }
        .post-content h4 { font-size: 1.25rem; }
        .post-content p { margin-bottom: var(--spacing-md); }
        .post-content ul, .post-content ol {
            margin-bottom: var(--spacing-md);
            padding-left: var(--spacing-xl);
        }
        .post-content li { margin-bottom: var(--spacing-sm); }
        .post-content pre {
            background-color: var(--color-bg-secondary);
            padding: var(--spacing-lg);
            border-radius: var(--radius-md);
            overflow-x: auto;
            margin: var(--spacing-lg) 0;
            border: 1px solid var(--color-border);
        }
        .post-content code {
            font-family: var(--font-mono);
            font-size: 0.875em;
            background-color: var(--color-bg-tertiary);
            padding: 0.125rem 0.375rem;
            border-radius: var(--radius-sm);
        }
        .post-content pre code { background-color: transparent; padding: 0; }
        .post-navigation {
            max-width: 800px;
            margin: var(--spacing-2xl) auto 0;
            padding-top: var(--spacing-xl);
            border-top: 1px solid var(--color-border);
        }
        .back-to-blog {
            color: var(--color-primary);
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-xs);
        }

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
        @media (max-width: 768px) {
            .nav-menu { display: none; }
            .post-meta-row { flex-direction: column; align-items: flex-start; gap: var(--spacing-xs); }
            .post-title { font-size: 2rem; }
            .post-content { font-size: 1rem; }
            .footer-grid { grid-template-columns: 1fr; }
            .footer-bottom { flex-direction: column; gap: var(--spacing-md); text-align: center; }
        }
    </style>
</head>
<body>
    <!-- Preview Banner -->
    <div class="preview-banner">
        PREVIEW MODE - This is how your blog post will look on the live site
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
                        <li><a href="#">Docs</a></li>
                        <li><a href="#">Downloads</a></li>
                        <li><a href="#" class="active">Blog</a></li>
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
        <article class="blog-post">
            <div class="container">
                <div class="post-header">
                    <div class="post-meta-row">
                        <time class="post-date" datetime="$POST_DATE">$formatted_date</time>
                        <div class="post-categories">
                            $categories_html
                        </div>
                    </div>
                    <h1 class="post-title">$POST_TITLE</h1>
                    <div class="post-author">By $POST_AUTHOR</div>
                </div>
                <div class="post-content">
                    $content_html
                </div>
                <div class="post-navigation">
                    <a href="#" class="back-to-blog">&larr; Back to Blog</a>
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

    local preview_dir="/tmp/i2p-blog-preview-$$"
    local project_name="i2p-preview"
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
    echo -e "${YELLOW}Terminal Preview:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    generate_post | head -50
    echo ""
    if [ $(generate_post | wc -l) -gt 50 ]; then
        echo -e "${YELLOW}... (content truncated)${NC}"
    fi
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

# Start preview - uses pgs.sh for hosting
start_preview() {
    preview_pgs
}

# Show post summary
show_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Post Summary:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Title:       ${GREEN}$POST_TITLE${NC}"
    echo -e "  Date:        ${GREEN}$POST_DATE${NC}"
    echo -e "  Author:      ${GREEN}$POST_AUTHOR${NC}"
    echo -e "  Categories:  ${GREEN}${POST_CATEGORIES[*]}${NC}"
    echo -e "  Slug:        ${GREEN}$POST_SLUG${NC}"
    if [ -n "$POST_DESCRIPTION" ]; then
        echo -e "  Description: ${GREEN}$POST_DESCRIPTION${NC}"
    fi
    echo -e "  Filename:    ${GREEN}$POST_DATE-$POST_SLUG.md${NC}"
    local content_lines=$(echo "$POST_CONTENT" | wc -l)
    echo -e "  Content:     ${GREEN}$content_lines lines${NC}"
    echo ""
}

# Save the final post
save_post() {
    local filename="$POST_DATE-$POST_SLUG.md"
    local filepath="$BLOG_DIR/$filename"

    # Check for existing file (that isn't our temp file)
    if [ -f "$filepath" ] && [ "$filepath" != "$TEMP_POST_FILE" ]; then
        read -p "File '$filename' already exists. Overwrite? (y/n): " confirm
        if [[ ! "$confirm" =~ ^[Yy] ]]; then
            echo -e "${YELLOW}Save cancelled${NC}"
            return 1
        fi
    fi

    # Write the final file
    generate_post > "$filepath"

    # Clear temp file reference since it's now the real file
    TEMP_POST_FILE=""

    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Blog post saved successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  File: ${CYAN}$filepath${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review changes: ${YELLOW}git diff content/en/blog/${NC}"
    echo -e "  2. Rebuild site:   ${YELLOW}hugo${NC}"
    echo -e "  3. Commit changes: ${YELLOW}git add -A && git commit -m \"Add blog post: $POST_TITLE\"${NC}"
    echo ""

    return 0
}

# Edit metadata
edit_metadata() {
    echo ""
    echo -e "${YELLOW}Which field to edit?${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} Title"
    echo -e "  ${CYAN}2)${NC} Date"
    echo -e "  ${CYAN}3)${NC} Author"
    echo -e "  ${CYAN}4)${NC} Categories"
    echo -e "  ${CYAN}5)${NC} Description"
    echo -e "  ${CYAN}6)${NC} Slug"
    echo -e "  ${CYAN}7)${NC} Back"
    echo ""

    read -p "Select: " field

    case $field in
        1)
            read -p "New title [$POST_TITLE]: " new_val
            [ -n "$new_val" ] && POST_TITLE="$new_val"
            ;;
        2)
            read -p "New date [$POST_DATE]: " new_val
            if [ -n "$new_val" ]; then
                if [[ "$new_val" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                    POST_DATE="$new_val"
                else
                    echo -e "${RED}Invalid date format${NC}"
                fi
            fi
            ;;
        3)
            read -p "New author [$POST_AUTHOR]: " new_val
            [ -n "$new_val" ] && POST_AUTHOR="$new_val"
            ;;
        4)
            select_categories
            ;;
        5)
            read -p "New description: " new_val
            POST_DESCRIPTION="$new_val"
            ;;
        6)
            read -p "New slug [$POST_SLUG]: " new_val
            [ -n "$new_val" ] && POST_SLUG="$new_val"
            ;;
        7)
            return 0
            ;;
    esac
}

# Post-preview menu loop
preview_menu() {
    while true; do
        echo ""
        echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║         Blog Post Actions              ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${CYAN}1)${NC} Save Blog Post"
        echo -e "  ${CYAN}2)${NC} Edit Content (re-paste)"
        echo -e "  ${CYAN}3)${NC} Edit Metadata"
        echo -e "  ${CYAN}4)${NC} Preview Again"
        echo -e "  ${CYAN}5)${NC} Show Summary"
        echo -e "  ${CYAN}6)${NC} Discard and Exit"
        echo ""

        read -p "Select option: " choice

        case $choice in
            1)
                if save_post; then
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
