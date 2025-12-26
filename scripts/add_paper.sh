#!/bin/bash
#
# I2P Research Paper Tool
# Adds research papers to the I2P website papers page
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PAPERS_FILE="$PROJECT_ROOT/content/en/papers.html"
RESEARCH_DIR="$PROJECT_ROOT/static/docs/research"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables for paper data
PAPER_TITLE=""
PAPER_AUTHORS=""
PAPER_YEAR=""
PAPER_MONTH=""
PAPER_VENUE=""
PAPER_PDF_URL=""
PAPER_EXTERNAL_URL=""
PAPER_BIBTEX=""
PAPER_BIBTEX_KEY=""
PAPER_BIBTEX_TYPE=""
LOCAL_PDF_PATH=""

show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║      I2P Research Paper Tool           ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Convert month name to number
month_to_num() {
    local month="$1"
    case "${month,,}" in
        january|jan) echo "01" ;;
        february|feb) echo "02" ;;
        march|mar) echo "03" ;;
        april|apr) echo "04" ;;
        may) echo "05" ;;
        june|jun) echo "06" ;;
        july|jul) echo "07" ;;
        august|aug) echo "08" ;;
        september|sep|sept) echo "09" ;;
        october|oct) echo "10" ;;
        november|nov) echo "11" ;;
        december|dec) echo "12" ;;
        *) echo "" ;;
    esac
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

# Extract first author's last name for filename
get_first_author_lastname() {
    local authors="$1"
    local first_author
    
    # Get first author (before first "and" or comma for multiple authors)
    first_author=$(echo "$authors" | sed 's/ and .*//;s/,.*$//' | xargs)
    
    # Handle "Last, First" format
    if [[ "$first_author" == *","* ]]; then
        first_author=$(echo "$first_author" | cut -d',' -f1 | xargs)
    else
        # Handle "First Last" format - get last word
        first_author=$(echo "$first_author" | awk '{print $NF}')
    fi
    
    # Convert to lowercase and remove special characters
    echo "$first_author" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z]//g'
}

# Generate unique filename for PDF
generate_pdf_filename() {
    local lastname="$1"
    local year="$2"
    local base="${lastname}${year}"
    local filename="${base}.pdf"
    local counter=0
    local letters="abcdefghijklmnopqrstuvwxyz"
    
    while [ -f "$RESEARCH_DIR/$filename" ]; do
        filename="${base}${letters:$counter:1}.pdf"
        ((counter++))
        if [ $counter -ge 26 ]; then
            echo -e "${RED}Error: Too many papers with same author/year${NC}" >&2
            return 1
        fi
    done
    
    echo "$filename"
}

# Check if URL is likely a PDF
# Checks: file extension, common PDF URL patterns, and Content-Type header
is_pdf_url() {
    local url="$1"
    
    # Check common URL patterns that indicate PDF
    # 1. Ends with .pdf (with optional query string)
    if [[ "$url" == *.pdf ]] || [[ "$url" == *.pdf\?* ]] || [[ "$url" == *.pdf\#* ]]; then
        return 0
    fi
    
    # 2. Contains /pdf/ in path (arxiv, many academic sites)
    if [[ "$url" == */pdf/* ]]; then
        return 0
    fi
    
    # 3. Known PDF hosting patterns
    if [[ "$url" == *"arxiv.org/pdf/"* ]] || \
       [[ "$url" == *"ieee.org"*"/stamp/stamp.jsp"* ]] || \
       [[ "$url" == *"acm.org"*"/doi/pdf/"* ]] || \
       [[ "$url" == *"researchgate.net"*".pdf"* ]] || \
       [[ "$url" == *"semantic"*"scholar"*"/paper/"* ]]; then
        return 0
    fi
    
    # 4. Check Content-Type header with curl (quick HEAD request)
    local content_type
    content_type=$(curl -sI -L --max-time 5 "$url" 2>/dev/null | grep -i "^content-type:" | tail -1)
    if [[ "$content_type" == *"application/pdf"* ]]; then
        return 0
    fi
    
    return 1
}

# Download PDF from URL
download_pdf() {
    local url="$1"
    local filename="$2"
    local dest="$RESEARCH_DIR/$filename"
    
    echo -e "${CYAN}Downloading PDF...${NC}"
    
    if curl -L -f -s -o "$dest" "$url"; then
        # Verify it's actually a PDF
        if file "$dest" | grep -q "PDF"; then
            echo -e "${GREEN}✓ PDF downloaded successfully${NC}"
            LOCAL_PDF_PATH="/docs/research/$filename"
            return 0
        else
            echo -e "${YELLOW}Warning: Downloaded file is not a PDF${NC}"
            rm -f "$dest"
            return 1
        fi
    else
        echo -e "${YELLOW}Warning: Failed to download PDF${NC}"
        return 1
    fi
}

# Detect BibTeX entry type from venue
detect_bibtex_type() {
    local venue="$1"
    local venue_lower="${venue,,}"
    
    if [[ "$venue_lower" == *"thesis"* ]]; then
        if [[ "$venue_lower" == *"phd"* ]] || [[ "$venue_lower" == *"doctoral"* ]]; then
            echo "phdthesis"
        else
            echo "mastersthesis"
        fi
    elif [[ "$venue_lower" == *"university"* ]] || [[ "$venue_lower" == *"institute"* ]] || [[ "$venue_lower" == *"technical report"* ]]; then
        echo "techreport"
    elif [[ "$venue_lower" == *"conference"* ]] || [[ "$venue_lower" == *"proceedings"* ]] || [[ "$venue_lower" == *"symposium"* ]] || [[ "$venue_lower" == *"workshop"* ]]; then
        echo "inproceedings"
    elif [[ "$venue_lower" == *"journal"* ]] || [[ "$venue_lower" =~ [0-9]+\([0-9]+\) ]]; then
        echo "article"
    elif [[ "$venue_lower" == *"book"* ]] || [[ "$venue_lower" == *"press"* ]]; then
        echo "book"
    else
        echo "misc"
    fi
}

# Generate BibTeX from manual input
generate_bibtex() {
    local lastname=$(get_first_author_lastname "$PAPER_AUTHORS")
    PAPER_BIBTEX_KEY="${lastname}${PAPER_YEAR}"
    PAPER_BIBTEX_TYPE=$(detect_bibtex_type "$PAPER_VENUE")
    
    # Format authors for BibTeX (replace ", " with " and " between authors)
    local bibtex_authors=$(echo "$PAPER_AUTHORS" | sed 's/, \([A-Z]\)/ and \1/g')
    
    local bibtex="@${PAPER_BIBTEX_TYPE}{${PAPER_BIBTEX_KEY},
  title = {${PAPER_TITLE}}, 
  author = {${bibtex_authors}}, "
    
    # Add venue-specific fields
    case "$PAPER_BIBTEX_TYPE" in
        techreport)
            # Extract institution from venue
            local institution=$(echo "$PAPER_VENUE" | sed 's/ technical report.*//i')
            bibtex+="
  institution = {${institution}}, "
            ;;
        inproceedings)
            bibtex+="
  booktitle = {${PAPER_VENUE}}, "
            ;;
        article)
            bibtex+="
  journal = {${PAPER_VENUE}}, "
            ;;
        mastersthesis|phdthesis)
            local school=$(echo "$PAPER_VENUE" | sed "s/.*thesis[,]*[ ]*//i;s/,.*//")
            bibtex+="
  school = {${school}}, "
            ;;
        book)
            bibtex+="
  publisher = {${PAPER_VENUE}}, "
            ;;
        *)
            if [ -n "$PAPER_VENUE" ]; then
                bibtex+="
  howpublished = {${PAPER_VENUE}}, "
            fi
            ;;
    esac
    
    bibtex+="
  year = {${PAPER_YEAR}}, "
    
    if [ -n "$PAPER_MONTH" ]; then
        bibtex+="
  month = {${PAPER_MONTH}}, "
    fi
    
    if [ -n "$PAPER_EXTERNAL_URL" ]; then
        bibtex+="
  url = {${PAPER_EXTERNAL_URL}}, "
    fi
    
    bibtex+="
  www_section = {Traffic analysis}, 
}"
    
    PAPER_BIBTEX="$bibtex"
}

# Helper function to extract field value from BibTeX (macOS compatible)
# Usage: extract_bibtex_field "bibtex_string" "field_name"
extract_bibtex_field() {
    local bibtex="$1"
    local field="$2"
    
    # Match field = {value} or field = "value" patterns
    # Using sed since macOS grep doesn't support -P
    local value=$(echo "$bibtex" | tr '\n' ' ' | sed -n "s/.*${field}[[:space:]]*=[[:space:]]*{\([^}]*\)}.*/\1/p" | head -1)
    
    # If not found with braces, try without (for bare values like year = 2025)
    if [ -z "$value" ]; then
        value=$(echo "$bibtex" | tr '\n' ' ' | sed -n "s/.*${field}[[:space:]]*=[[:space:]]*\([^,}]*\)[,}].*/\1/p" | head -1 | sed 's/[{}]//g' | xargs)
    fi
    
    # Clean up nested braces and extra whitespace
    echo "$value" | sed 's/{//g;s/}//g' | xargs
}

# Parse BibTeX entry
parse_bibtex() {
    local bibtex="$1"
    
    # Extract entry type (e.g., @techreport{key, -> techreport)
    PAPER_BIBTEX_TYPE=$(echo "$bibtex" | sed -n 's/^@\([a-zA-Z]*\){.*/\1/p' | head -1 | tr '[:upper:]' '[:lower:]')
    
    # Extract key (e.g., @techreport{wang2025, -> wang2025)
    PAPER_BIBTEX_KEY=$(echo "$bibtex" | sed -n 's/^@[a-zA-Z]*{\([^,]*\),.*/\1/p' | head -1)
    
    # Extract title
    PAPER_TITLE=$(extract_bibtex_field "$bibtex" "title")
    
    # Extract authors and convert BibTeX "and" to display format
    PAPER_AUTHORS=$(extract_bibtex_field "$bibtex" "author")
    PAPER_AUTHORS=$(echo "$PAPER_AUTHORS" | sed 's/ and /, /g')
    
    # Extract year
    PAPER_YEAR=$(extract_bibtex_field "$bibtex" "year")
    
    # Extract month
    PAPER_MONTH=$(extract_bibtex_field "$bibtex" "month")
    
    # Extract venue based on type
    case "$PAPER_BIBTEX_TYPE" in
        techreport)
            PAPER_VENUE=$(extract_bibtex_field "$bibtex" "institution")
            if [ -n "$PAPER_VENUE" ]; then
                PAPER_VENUE="$PAPER_VENUE technical report"
            fi
            ;;
        inproceedings)
            PAPER_VENUE=$(extract_bibtex_field "$bibtex" "booktitle")
            ;;
        article)
            PAPER_VENUE=$(extract_bibtex_field "$bibtex" "journal")
            ;;
        mastersthesis)
            local school=$(extract_bibtex_field "$bibtex" "school")
            if [ -n "$school" ]; then
                PAPER_VENUE="Masters's thesis, $school"
            fi
            ;;
        phdthesis)
            local school=$(extract_bibtex_field "$bibtex" "school")
            if [ -n "$school" ]; then
                PAPER_VENUE="Ph.D. thesis, $school"
            fi
            ;;
        book)
            PAPER_VENUE=$(extract_bibtex_field "$bibtex" "publisher")
            ;;
        *)
            PAPER_VENUE=$(extract_bibtex_field "$bibtex" "howpublished")
            ;;
    esac
    
    # Extract URL
    PAPER_EXTERNAL_URL=$(extract_bibtex_field "$bibtex" "url")
    if [ -z "$PAPER_EXTERNAL_URL" ]; then
        PAPER_EXTERNAL_URL=$(extract_bibtex_field "$bibtex" "www_pdf_url")
    fi
    
    PAPER_BIBTEX="$bibtex"
}

# Manual entry mode
manual_entry() {
    echo ""
    echo -e "${YELLOW}Enter paper details:${NC}"
    echo ""
    
    read -p "1. Title: " PAPER_TITLE
    if [ -z "$PAPER_TITLE" ]; then
        echo -e "${RED}Error: Title is required${NC}"
        return 1
    fi
    
    read -p "2. Authors (comma-separated): " PAPER_AUTHORS
    if [ -z "$PAPER_AUTHORS" ]; then
        echo -e "${RED}Error: Authors are required${NC}"
        return 1
    fi
    
    read -p "3. Year: " PAPER_YEAR
    if ! [[ "$PAPER_YEAR" =~ ^[0-9]{4}$ ]]; then
        echo -e "${RED}Error: Invalid year format${NC}"
        return 1
    fi
    
    read -p "4. Month (optional, press Enter to skip): " PAPER_MONTH
    
    read -p "5. Venue/Publication (e.g., 'University of Example technical report'): " PAPER_VENUE
    
    read -p "6. URL to paper (PDF or webpage): " PAPER_EXTERNAL_URL
    
    # Auto-detect if URL is a PDF
    if [ -n "$PAPER_EXTERNAL_URL" ]; then
        if is_pdf_url "$PAPER_EXTERNAL_URL"; then
            PAPER_PDF_URL="$PAPER_EXTERNAL_URL"
            echo -e "   ${GREEN}PDF detected - will download${NC}"
        else
            echo -e "   ${CYAN}Not a PDF - will use as external link${NC}"
        fi
    fi
    
    # Generate BibTeX
    generate_bibtex
    
    echo ""
    echo -e "${CYAN}Generated BibTeX:${NC}"
    echo ""
    echo "$PAPER_BIBTEX"
    echo ""
    
    read -p "Is this correct? (y/n): " confirm
    if [[ ! "$confirm" =~ ^[Yy] ]]; then
        echo -e "${YELLOW}You can edit the BibTeX manually. Paste corrected version (end with empty line):${NC}"
        local bibtex_input=""
        local line
        while IFS= read -r line; do
            [ -z "$line" ] && break
            bibtex_input+="$line"$'\n'
        done
        if [ -n "$bibtex_input" ]; then
            PAPER_BIBTEX="$bibtex_input"
        fi
    fi
    
    return 0
}

# BibTeX paste mode - can optionally receive first line as argument
bibtex_entry() {
    local first_line="$1"
    local bibtex_input=""
    
    if [ -n "$first_line" ]; then
        # We already have the first line (detected from menu)
        echo ""
        echo -e "${CYAN}BibTeX detected! Continue pasting (press Enter twice when done):${NC}"
        bibtex_input="$first_line"$'\n'
    else
        echo ""
        echo -e "${YELLOW}Paste your BibTeX entry (press Enter twice when done):${NC}"
        echo ""
    fi
    
    local line
    local empty_count=0
    
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            ((empty_count++))
            [ $empty_count -ge 1 ] && break
        else
            empty_count=0
        fi
        bibtex_input+="$line"$'\n'
    done
    
    if [ -z "$bibtex_input" ]; then
        echo -e "${RED}Error: No BibTeX provided${NC}"
        return 1
    fi
    
    # Parse the BibTeX
    parse_bibtex "$bibtex_input"
    
    echo ""
    echo -e "${CYAN}Parsed information:${NC}"
    echo -e "  Title:   ${GREEN}$PAPER_TITLE${NC}"
    echo -e "  Authors: ${GREEN}$PAPER_AUTHORS${NC}"
    echo -e "  Year:    ${GREEN}$PAPER_YEAR${NC}"
    if [ -n "$PAPER_MONTH" ]; then
        echo -e "  Month:   ${GREEN}$PAPER_MONTH${NC}"
    fi
    if [ -n "$PAPER_VENUE" ]; then
        echo -e "  Venue:   ${GREEN}$PAPER_VENUE${NC}"
    fi
    if [ -n "$PAPER_EXTERNAL_URL" ]; then
        echo -e "  URL:     ${GREEN}$PAPER_EXTERNAL_URL${NC}"
    fi
    echo ""
    
    read -p "Is this correct? (y/n): " confirm
    if [[ ! "$confirm" =~ ^[Yy] ]]; then
        echo -e "${RED}Please try again with corrected BibTeX${NC}"
        return 1
    fi
    
    # Auto-detect if URL is a PDF - no prompting
    if [ -n "$PAPER_EXTERNAL_URL" ]; then
        if is_pdf_url "$PAPER_EXTERNAL_URL"; then
            PAPER_PDF_URL="$PAPER_EXTERNAL_URL"
            echo -e "${GREEN}PDF URL detected - will download${NC}"
        else
            echo -e "${CYAN}URL is not a PDF - will use as external link${NC}"
        fi
    fi
    
    return 0
}

# Generate HTML for the paper entry
generate_html() {
    local pdf_link="$LOCAL_PDF_PATH"
    if [ -z "$pdf_link" ] && [ -n "$PAPER_PDF_URL" ]; then
        pdf_link="$PAPER_PDF_URL"
    fi
    
    local title_html
    local pdf_button=""
    
    # Determine title link - prefer local PDF, then external URL, then no link
    if [ -n "$pdf_link" ]; then
        title_html="<a href=\"$pdf_link\" target=\"_blank\">$PAPER_TITLE</a>"
        pdf_button="        <a href=\"$pdf_link\" target=\"_blank\" class=\"paper-link\">
            <svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\">
                <path d=\"M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z\" stroke-width=\"2\"/>
                <path d=\"M14 2v6h6M16 13H8M16 17H8M10 9H8\" stroke-width=\"2\"/>
            </svg>
            PDF
        </a>"
    elif [ -n "$PAPER_EXTERNAL_URL" ]; then
        # Has external URL but not a PDF - link title to external URL, no PDF button
        title_html="<a href=\"$PAPER_EXTERNAL_URL\" target=\"_blank\">$PAPER_TITLE</a>"
    else
        title_html="<span class=\"no-link\">$PAPER_TITLE</span>"
    fi
    
    # Format venue line
    local venue_line=""
    if [ -n "$PAPER_VENUE" ]; then
        venue_line="$PAPER_VENUE"
        if [ -n "$PAPER_MONTH" ]; then
            venue_line="$venue_line, $PAPER_MONTH $PAPER_YEAR."
        else
            venue_line="$venue_line, $PAPER_YEAR."
        fi
    else
        if [ -n "$PAPER_MONTH" ]; then
            venue_line="$PAPER_MONTH $PAPER_YEAR."
        else
            venue_line="$PAPER_YEAR."
        fi
    fi
    
    # Escape special characters in BibTeX for HTML
    local escaped_bibtex=$(echo "$PAPER_BIBTEX" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    
    local html="<div class=\"paper-entry\" data-year=\"$PAPER_YEAR\" data-title=\"$PAPER_TITLE\" data-authors=\"$PAPER_AUTHORS\">
    <div class=\"paper-title\">$title_html</div>
    <div class=\"paper-authors\">$PAPER_AUTHORS</div>
    <div class=\"paper-venue\">$venue_line</div>
    <div class=\"paper-actions\">"
    
    if [ -n "$pdf_button" ]; then
        html+="
$pdf_button"
    fi
    
    html+="
        <div class=\"bibtex-wrapper\">
            <button class=\"bibtex-toggle\">Show BibTeX</button>
            <div class=\"bibtex-content\">$escaped_bibtex</div>
        </div>
    </div>
</div>"
    
    echo "$html"
}

# Insert paper into papers.html
insert_paper() {
    local html="$1"
    local year="$PAPER_YEAR"
    local temp_file=$(mktemp)
    
    # Check if year header exists
    if grep -q "<h2 class=\"paper-year\" data-year=\"$year\">$year</h2>" "$PAPERS_FILE"; then
        # Year exists - insert after the year header
        local year_line=$(grep -n "<h2 class=\"paper-year\" data-year=\"$year\">$year</h2>" "$PAPERS_FILE" | cut -d: -f1)
        
        # Insert after the year header line
        head -n "$year_line" "$PAPERS_FILE" > "$temp_file"
        echo "$html" >> "$temp_file"
        tail -n +"$((year_line + 1))" "$PAPERS_FILE" >> "$temp_file"
    else
        # Year doesn't exist - find correct position and create header
        local inserted=false
        local in_content=false
        
        while IFS= read -r line; do
            # Check if we're past the frontmatter
            if [[ "$line" == "---" ]] && [ "$in_content" = false ]; then
                echo "$line" >> "$temp_file"
                in_content=true
                continue
            fi
            
            # Look for year headers to find insertion point
            if [[ "$line" =~ \<h2\ class=\"paper-year\"\ data-year=\"([0-9]+)\"\> ]]; then
                local existing_year="${BASH_REMATCH[1]}"
                if [ "$inserted" = false ] && [ "$year" -gt "$existing_year" ]; then
                    # Insert new year header and entry before this year
                    echo "" >> "$temp_file"
                    echo "<h2 class=\"paper-year\" data-year=\"$year\">$year</h2>" >> "$temp_file"
                    echo "$html" >> "$temp_file"
                    echo "" >> "$temp_file"
                    inserted=true
                fi
            fi
            
            echo "$line" >> "$temp_file"
        done < "$PAPERS_FILE"
        
        # If not inserted (year is older than all existing), append at end
        if [ "$inserted" = false ]; then
            # Find last paper entry and insert after it
            echo "" >> "$temp_file"
            echo "<h2 class=\"paper-year\" data-year=\"$year\">$year</h2>" >> "$temp_file"
            echo "$html" >> "$temp_file"
        fi
    fi
    
    mv "$temp_file" "$PAPERS_FILE"
}

# Show summary and confirm
show_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Summary:${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Title:   ${GREEN}$PAPER_TITLE${NC}"
    echo -e "  Authors: ${GREEN}$PAPER_AUTHORS${NC}"
    echo -e "  Year:    ${GREEN}$PAPER_YEAR${NC}"
    if [ -n "$PAPER_MONTH" ]; then
        echo -e "  Month:   ${GREEN}$PAPER_MONTH${NC}"
    fi
    if [ -n "$PAPER_VENUE" ]; then
        echo -e "  Venue:   ${GREEN}$PAPER_VENUE${NC}"
    fi
    if [ -n "$LOCAL_PDF_PATH" ]; then
        echo -e "  PDF:     ${GREEN}$LOCAL_PDF_PATH${NC} (downloaded)"
    elif [ -n "$PAPER_PDF_URL" ]; then
        echo -e "  PDF:     ${GREEN}$PAPER_PDF_URL${NC} (external)"
    else
        echo -e "  PDF:     ${YELLOW}(none)${NC}"
    fi
    echo ""
}

main() {
    show_header
    
    echo ""
    echo -e "${YELLOW}How would you like to add the paper?${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} Enter details manually"
    echo -e "  ${CYAN}2)${NC} Paste BibTeX entry"
    echo ""
    echo -e "  ${CYAN}Or just paste your BibTeX directly:${NC}"
    echo ""
    
    read -p "Select option (1/2) or paste BibTeX: " mode
    
    # Check if the input looks like BibTeX (starts with @)
    if [[ "$mode" == @* ]]; then
        echo -e "${GREEN}BibTeX detected!${NC}"
        if ! bibtex_entry "$mode"; then
            exit 1
        fi
    else
        case $mode in
            1)
                if ! manual_entry; then
                    exit 1
                fi
                ;;
            2)
                if ! bibtex_entry; then
                    exit 1
                fi
                ;;
            *)
                echo -e "${RED}Invalid option. Please enter 1, 2, or paste BibTeX starting with @${NC}"
                exit 1
                ;;
        esac
    fi
    
    # Download PDF if URL provided
    if [ -n "$PAPER_PDF_URL" ]; then
        local lastname=$(get_first_author_lastname "$PAPER_AUTHORS")
        local filename=$(generate_pdf_filename "$lastname" "$PAPER_YEAR")
        
        if [ -n "$filename" ]; then
            if ! download_pdf "$PAPER_PDF_URL" "$filename"; then
                echo -e "${YELLOW}Continuing without local PDF...${NC}"
            fi
        fi
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
    insert_paper "$html"
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Paper added successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review changes: ${YELLOW}git diff content/en/papers.html${NC}"
    echo -e "  2. Rebuild site:   ${YELLOW}hugo${NC}"
    echo -e "  3. Commit changes: ${YELLOW}git add -A && git commit -m \"Add research paper: $PAPER_TITLE\"${NC}"
    echo ""
}

main
