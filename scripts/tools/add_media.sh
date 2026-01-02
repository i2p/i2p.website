#!/bin/bash
#
# I2P Media/Press Tool
# Adds media entries (interviews, articles, presentations) to the I2P website
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEDIA_FILE="$PROJECT_ROOT/content/en/about/media.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables for media data
MEDIA_TITLE=""
MEDIA_DATE=""
MEDIA_DATE_DISPLAY=""
MEDIA_YEAR=""
MEDIA_URL=""
MEDIA_TYPE=""
MEDIA_TYPE_NAME=""
MEDIA_EMOJI=""
MEDIA_BUTTON_LABEL=""
MEDIA_NOTES=""
declare -a EXTRA_LINKS=()
declare -a EXTRA_LABELS=()

show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║      I2P Media/Press Tool              ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Convert month number to name
num_to_month() {
    local num="$1"
    case "$num" in
        01|1) echo "January" ;;
        02|2) echo "February" ;;
        03|3) echo "March" ;;
        04|4) echo "April" ;;
        05|5) echo "May" ;;
        06|6) echo "June" ;;
        07|7) echo "July" ;;
        08|8) echo "August" ;;
        09|9) echo "September" ;;
        10) echo "October" ;;
        11) echo "November" ;;
        12) echo "December" ;;
        *) echo "" ;;
    esac
}

# Parse date input (m/y or m/d/y)
parse_date() {
    local input="$1"
    local parts
    
    IFS='/' read -ra parts <<< "$input"
    
    if [ ${#parts[@]} -eq 2 ]; then
        # m/y format
        local month=$(num_to_month "${parts[0]}")
        MEDIA_YEAR="${parts[1]}"
        MEDIA_DATE_DISPLAY="$month ${parts[1]}"
    elif [ ${#parts[@]} -eq 3 ]; then
        # m/d/y format
        local month=$(num_to_month "${parts[0]}")
        MEDIA_YEAR="${parts[2]}"
        MEDIA_DATE_DISPLAY="$month ${parts[1]}, ${parts[2]}"
    else
        return 1
    fi
    
    # Validate year
    if ! [[ "$MEDIA_YEAR" =~ ^[0-9]{4}$ ]]; then
        return 1
    fi
    
    return 0
}

# Set type info based on selection
set_type_info() {
    local type="$1"
    
    case "$type" in
        1)
            MEDIA_TYPE="article"
            MEDIA_TYPE_NAME="Article"
            MEDIA_EMOJI="📄"
            MEDIA_BUTTON_LABEL="Read Article"
            ;;
        2)
            MEDIA_TYPE="interview"
            MEDIA_TYPE_NAME="Interview"
            MEDIA_EMOJI="📄"
            MEDIA_BUTTON_LABEL="Read Interview"
            ;;
        3)
            MEDIA_TYPE="video"
            MEDIA_TYPE_NAME="Presentation"
            MEDIA_EMOJI="🎥"
            MEDIA_BUTTON_LABEL="Watch Video"
            ;;
        4)
            MEDIA_TYPE="podcast"
            MEDIA_TYPE_NAME="Podcast"
            MEDIA_EMOJI="🎙️"
            MEDIA_BUTTON_LABEL="Listen"
            ;;
        5)
            MEDIA_TYPE="conference"
            MEDIA_TYPE_NAME="Conference"
            MEDIA_EMOJI="🎪"
            MEDIA_BUTTON_LABEL="Details"
            ;;
        *)
            return 1
            ;;
    esac
    
    return 0
}

# Collect entry information
collect_info() {
    echo ""
    echo -e "${YELLOW}Enter media entry details:${NC}"
    echo ""
    
    # Title
    read -p "1. Title: " MEDIA_TITLE
    if [ -z "$MEDIA_TITLE" ]; then
        echo -e "${RED}Error: Title is required${NC}"
        return 1
    fi
    
    # Date
    while true; do
        read -p "2. Date (m/y or m/d/y, e.g., 7/2024 or 3/6/2022): " MEDIA_DATE
        if parse_date "$MEDIA_DATE"; then
            echo -e "   ${GREEN}→ Parsed as: $MEDIA_DATE_DISPLAY${NC}"
            break
        else
            echo -e "   ${RED}Invalid date format. Please use m/y or m/d/y${NC}"
        fi
    done
    
    # URL
    read -p "3. Link URL: " MEDIA_URL
    if [ -z "$MEDIA_URL" ]; then
        echo -e "${RED}Error: URL is required${NC}"
        return 1
    fi
    
    # Type
    echo ""
    echo -e "4. Type:"
    echo -e "   ${CYAN}1)${NC} Article"
    echo -e "   ${CYAN}2)${NC} Interview"
    echo -e "   ${CYAN}3)${NC} Presentation/Video"
    echo -e "   ${CYAN}4)${NC} Podcast"
    echo -e "   ${CYAN}5)${NC} Conference"
    echo ""
    
    while true; do
        read -p "   Select type: " type_choice
        if set_type_info "$type_choice"; then
            echo -e "   ${GREEN}→ $MEDIA_EMOJI $MEDIA_TYPE_NAME${NC}"
            break
        else
            echo -e "   ${RED}Invalid selection. Please choose 1-5${NC}"
        fi
    done
    
    # Notes
    echo ""
    read -p "5. Additional notes (optional, e.g., 'Two-part series', 'German'): " MEDIA_NOTES
    
    # Extra links
    echo ""
    while true; do
        read -p "6. Add additional link? (y/n): " add_link
        if [[ "$add_link" =~ ^[Yy] ]]; then
            read -p "   Label (e.g., 'Part 2', 'YouTube', 'Slides'): " link_label
            read -p "   URL: " link_url
            if [ -n "$link_label" ] && [ -n "$link_url" ]; then
                EXTRA_LINKS+=("$link_url")
                EXTRA_LABELS+=("$link_label")
                echo -e "   ${GREEN}→ Added: $link_label${NC}"
            fi
        else
            break
        fi
    done
    
    return 0
}

# Generate HTML for the media entry
generate_html() {
    local html="<div class=\"content-entry\">
<div class=\"content-entry-title\">
<a href=\"$MEDIA_URL\" target=\"_blank\">$MEDIA_TITLE</a>
</div>
<div class=\"content-entry-meta\">$MEDIA_EMOJI $MEDIA_TYPE_NAME • $MEDIA_DATE_DISPLAY"

    if [ -n "$MEDIA_NOTES" ]; then
        html+=" • $MEDIA_NOTES"
    fi
    
    html+="</div>
<div class=\"content-entry-actions\">
<a href=\"$MEDIA_URL\" target=\"_blank\" class=\"content-btn\">$MEDIA_BUTTON_LABEL</a>"

    # Add extra links
    for i in "${!EXTRA_LINKS[@]}"; do
        html+="
<a href=\"${EXTRA_LINKS[$i]}\" target=\"_blank\" class=\"content-btn-secondary\">${EXTRA_LABELS[$i]}</a>"
    done
    
    html+="
</div>
</div>"

    echo "$html"
}

# Insert entry into media.md
insert_entry() {
    local html="$1"
    local year="$MEDIA_YEAR"
    local temp_file=$(mktemp)
    
    # Check if this year should go in the collapsed section (2012 and earlier)
    local in_collapsed=false
    if [ "$year" -le 2012 ]; then
        in_collapsed=true
    fi
    
    # Check if year header exists
    if grep -q "<h2 class=\"content-year\">$year</h2>" "$MEDIA_FILE"; then
        # Year exists - insert after the year header (and blank line)
        local year_line=$(grep -n "<h2 class=\"content-year\">$year</h2>" "$MEDIA_FILE" | cut -d: -f1)
        
        # Find next non-empty line after year header
        local insert_line=$((year_line + 1))
        
        # Insert after the year header
        head -n "$year_line" "$MEDIA_FILE" > "$temp_file"
        echo "" >> "$temp_file"
        echo "$html" >> "$temp_file"
        tail -n +"$insert_line" "$MEDIA_FILE" >> "$temp_file"
    else
        # Year doesn't exist - find correct position and create header
        local inserted=false
        local in_details=false
        local details_start_line=0
        
        # Read file line by line
        local line_num=0
        while IFS= read -r line; do
            ((line_num++))
            
            # Track if we're inside the details/collapsed section
            if [[ "$line" == *"<details"* ]]; then
                in_details=true
                details_start_line=$line_num
            fi
            if [[ "$line" == *"</details>"* ]]; then
                in_details=false
            fi
            
            # Look for year headers to find insertion point
            if [[ "$line" =~ \<h2\ class=\"content-year\"\>([0-9]+)\</h2\> ]]; then
                local existing_year="${BASH_REMATCH[1]}"
                
                # For collapsed years (<=2012), only compare with other collapsed years
                if [ "$in_collapsed" = true ] && [ "$in_details" = true ]; then
                    if [ "$inserted" = false ] && [ "$year" -gt "$existing_year" ]; then
                        # Insert new year header and entry before this year
                        echo "" >> "$temp_file"
                        echo "<h2 class=\"content-year\">$year</h2>" >> "$temp_file"
                        echo "" >> "$temp_file"
                        echo "$html" >> "$temp_file"
                        inserted=true
                    fi
                # For non-collapsed years (>2012), compare with non-collapsed years
                elif [ "$in_collapsed" = false ] && [ "$in_details" = false ]; then
                    if [ "$inserted" = false ] && [ "$year" -gt "$existing_year" ]; then
                        # Insert new year header and entry before this year
                        echo "" >> "$temp_file"
                        echo "<h2 class=\"content-year\">$year</h2>" >> "$temp_file"
                        echo "" >> "$temp_file"
                        echo "$html" >> "$temp_file"
                        inserted=true
                    fi
                fi
            fi
            
            # If entry should go in collapsed section and we just entered it
            if [ "$in_collapsed" = true ] && [ "$inserted" = false ] && [[ "$line" == *"<summary>"* ]]; then
                echo "$line" >> "$temp_file"
                # Check if this is the oldest year in collapsed section
                continue
            fi
            
            echo "$line" >> "$temp_file"
        done < "$MEDIA_FILE"
        
        # If not inserted yet
        if [ "$inserted" = false ]; then
            if [ "$in_collapsed" = true ]; then
                # Need to insert in the collapsed section at the end
                # Re-process to find the right spot
                rm "$temp_file"
                temp_file=$(mktemp)
                
                while IFS= read -r line; do
                    # Insert before </details>
                    if [[ "$line" == *"</details>"* ]] && [ "$inserted" = false ]; then
                        echo "" >> "$temp_file"
                        echo "<h2 class=\"content-year\">$year</h2>" >> "$temp_file"
                        echo "" >> "$temp_file"
                        echo "$html" >> "$temp_file"
                        echo "" >> "$temp_file"
                        inserted=true
                    fi
                    echo "$line" >> "$temp_file"
                done < "$MEDIA_FILE"
            else
                # Year is newer than all existing non-collapsed - insert after front matter
                rm "$temp_file"
                temp_file=$(mktemp)
                local frontmatter_end=0
                local line_num=0
                local fm_count=0
                
                while IFS= read -r line; do
                    ((line_num++))
                    echo "$line" >> "$temp_file"
                    
                    if [[ "$line" == "---" ]]; then
                        ((fm_count++))
                        if [ $fm_count -eq 2 ]; then
                            frontmatter_end=$line_num
                        fi
                    fi
                    
                    # Insert after the intro div
                    if [[ "$line" == *"</div>"* ]] && [ $frontmatter_end -gt 0 ] && [ "$inserted" = false ]; then
                        # Check if next line is a year header
                        local next_check=$(sed -n "$((line_num+2))p" "$MEDIA_FILE")
                        if [[ "$next_check" =~ \<h2\ class=\"content-year\" ]]; then
                            echo "" >> "$temp_file"
                            echo "<h2 class=\"content-year\">$year</h2>" >> "$temp_file"
                            echo "" >> "$temp_file"
                            echo "$html" >> "$temp_file"
                            inserted=true
                        fi
                    fi
                done < "$MEDIA_FILE"
            fi
        fi
    fi
    
    mv "$temp_file" "$MEDIA_FILE"
}

# Show summary and confirm
show_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Summary:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Title: ${GREEN}$MEDIA_TITLE${NC}"
    echo -e "  Date:  ${GREEN}$MEDIA_DATE_DISPLAY${NC}"
    echo -e "  Type:  ${GREEN}$MEDIA_EMOJI $MEDIA_TYPE_NAME${NC}"
    echo -e "  URL:   ${GREEN}$MEDIA_URL${NC}"
    if [ -n "$MEDIA_NOTES" ]; then
        echo -e "  Notes: ${GREEN}$MEDIA_NOTES${NC}"
    fi
    if [ ${#EXTRA_LINKS[@]} -gt 0 ]; then
        echo -e "  Extra links:"
        for i in "${!EXTRA_LINKS[@]}"; do
            echo -e "    ${GREEN}${EXTRA_LABELS[$i]}${NC} → ${EXTRA_LINKS[$i]}"
        done
    fi
    echo ""
}

main() {
    show_header
    
    if ! collect_info; then
        exit 1
    fi
    
    # Show summary
    show_summary
    
    read -p "Proceed? (y/n): " confirm
    if [[ ! "$confirm" =~ ^[Yy] ]]; then
        echo -e "${RED}Cancelled.${NC}"
        exit 0
    fi
    
    # Generate and insert HTML
    local html=$(generate_html)
    insert_entry "$html"
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Media entry added successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review changes: ${YELLOW}git diff content/en/about/media.md${NC}"
    echo -e "  2. Rebuild site:   ${YELLOW}hugo${NC}"
    echo -e "  3. Commit changes: ${YELLOW}git add -A && git commit -m \"Add media: $MEDIA_TITLE\"${NC}"
    echo ""
}

main
