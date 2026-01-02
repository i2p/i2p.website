#!/bin/bash
#
# Interactive Banner Update Script
# Updates the site banner across all languages using Claude API
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║       I2P Banner Update Tool           ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY environment variable not set${NC}"
    echo ""
    echo "Please set it first:"
    echo "  export ANTHROPIC_API_KEY=\"your-key-here\""
    exit 1
fi

# Check for Python and anthropic package
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo -e "${RED}Error: anthropic Python package not installed${NC}"
    echo ""
    echo "Please install it first:"
    echo "  pip install anthropic"
    exit 1
fi

echo ""

# Question 1: Banner message
echo -e "${YELLOW}1. What do you want the banner to say?${NC}"
echo -e "   (This is the main announcement text)"
echo ""
read -p "   Banner message: " BANNER_MESSAGE

if [ -z "$BANNER_MESSAGE" ]; then
    echo -e "${RED}Error: Banner message cannot be empty${NC}"
    exit 1
fi

echo ""

# Question 2: Is this for a poll?
echo -e "${YELLOW}2. Is this banner for a new poll?${NC}"
read -p "   (y/n): " IS_POLL

LINK_TEXT=""
LINK_URL=""

if [[ "$IS_POLL" =~ ^[Yy] ]]; then
    LINK_TEXT="Take our poll"
    LINK_URL="#poll"
    echo -e "   ${GREEN}✓ Will link to poll modal${NC}"
else
    echo ""
    # Question 3: Is there a link?
    echo -e "${YELLOW}3. Should the banner have a link?${NC}"
    read -p "   (y/n): " HAS_LINK
    
    if [[ "$HAS_LINK" =~ ^[Yy] ]]; then
        echo ""
        echo -e "${YELLOW}   What should the link text say?${NC}"
        echo -e "   (e.g., \"Learn more\", \"Download now\", \"Read the announcement\")"
        read -p "   Link text: " LINK_TEXT
        
        echo ""
        echo -e "${YELLOW}   What URL should the link go to?${NC}"
        echo -e "   (e.g., \"/downloads/\", \"/blog/2025/...\", \"https://...\")"
        read -p "   Link URL: " LINK_URL
    fi
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${YELLOW}Summary:${NC}"
echo ""
echo -e "  Message:   ${GREEN}$BANNER_MESSAGE${NC}"
if [ -n "$LINK_TEXT" ]; then
    echo -e "  Link text: ${GREEN}$LINK_TEXT${NC}"
    echo -e "  Link URL:  ${GREEN}$LINK_URL${NC}"
else
    echo -e "  Link:      ${GREEN}(none)${NC}"
fi
echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# Confirm
echo -e "${YELLOW}This will update all 13 language files and increment the banner ID.${NC}"
read -p "Proceed? (y/n): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy] ]]; then
    echo -e "${RED}Cancelled.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Updating banner...${NC}"
echo ""

# Build the command
CMD="python3 \"$SCRIPT_DIR/update_banner.py\" \"$BANNER_MESSAGE\""

if [ -n "$LINK_TEXT" ]; then
    CMD="$CMD --link-text \"$LINK_TEXT\""
fi

if [ -n "$LINK_URL" ]; then
    CMD="$CMD --link-url \"$LINK_URL\""
fi

# Run the Python script
eval $CMD

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Banner updated successfully!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Review the changes: ${YELLOW}git diff i18n/ hugo.toml${NC}"
echo -e "  2. Rebuild the site:   ${YELLOW}hugo${NC}"
echo -e "  3. Commit the changes: ${YELLOW}git add -A && git commit -m \"Update banner\"${NC}"
echo ""


