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

# Preview with surge.sh
preview_surge() {
    echo ""

    # Check for required tools
    if ! command -v hugo &>/dev/null; then
        echo -e "${RED}Error: Hugo is required to build the preview${NC}"
        echo -e "${YELLOW}Install Hugo: https://gohugo.io/installation/${NC}"
        show_terminal_preview
        return 1
    fi

    if ! command -v surge &>/dev/null; then
        echo -e "${RED}Error: surge is required for preview hosting${NC}"
        echo -e "${YELLOW}Install with: npm install -g surge${NC}"
        show_terminal_preview
        return 1
    fi

    echo -e "${CYAN}Building site with Hugo...${NC}"

    # Write temp post
    write_temp_post

    local preview_dir="/tmp/i2p-blog-preview-$$"

    cd "$PROJECT_ROOT"
    if ! hugo --buildDrafts --destination "$preview_dir" 2>&1; then
        echo -e "${RED}Hugo build failed${NC}"
        show_terminal_preview
        rm -rf "$preview_dir"
        return 1
    fi

    local domain="i2p-preview-$(date +%s).surge.sh"
    echo -e "${CYAN}Uploading to surge.sh...${NC}"

    if surge "$preview_dir" --domain "$domain"; then
        local year=$(echo "$POST_DATE" | cut -d'-' -f1)
        local month=$(echo "$POST_DATE" | cut -d'-' -f2)
        local day=$(echo "$POST_DATE" | cut -d'-' -f3)
        echo ""
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}Preview URL: https://$domain/en/blog/$year/$month/$day/$POST_SLUG/${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo ""

        # Try to open in browser if we have a display
        if has_display; then
            open_browser "https://$domain/en/blog/$year/$month/$day/$POST_SLUG/"
        fi
    else
        echo -e "${RED}Failed to upload to surge.sh${NC}"
        show_terminal_preview
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

# Start preview - uses surge.sh for hosting
start_preview() {
    preview_surge
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
