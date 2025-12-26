#!/bin/bash
#
# I2P Website Tools - All-in-One Menu
# Provides easy access to various website update utilities
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_header() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║       I2P Website Tools                ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_menu() {
    echo ""
    echo -e "${YELLOW}What would you like to do?${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} Update Site Banner"
    echo -e "  ${CYAN}2)${NC} Add Research Paper"
    echo -e "  ${CYAN}3)${NC} Add Media/Press Entry"
    echo -e "  ${CYAN}4)${NC} Exit"
    echo ""
}

main() {
    while true; do
        show_header
        show_menu
        
        read -p "Select option: " choice
        
        case $choice in
            1)
                echo ""
                echo -e "${BLUE}Launching Banner Update Tool...${NC}"
                echo ""
                if [ -x "$SCRIPT_DIR/update_banner.sh" ]; then
                    "$SCRIPT_DIR/update_banner.sh"
                else
                    echo -e "${RED}Error: update_banner.sh not found or not executable${NC}"
                    echo "Expected location: $SCRIPT_DIR/update_banner.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            2)
                echo ""
                echo -e "${BLUE}Launching Research Paper Tool...${NC}"
                echo ""
                if [ -x "$SCRIPT_DIR/add_paper.sh" ]; then
                    "$SCRIPT_DIR/add_paper.sh"
                else
                    echo -e "${RED}Error: add_paper.sh not found or not executable${NC}"
                    echo "Expected location: $SCRIPT_DIR/add_paper.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            3)
                echo ""
                echo -e "${BLUE}Launching Media/Press Tool...${NC}"
                echo ""
                if [ -x "$SCRIPT_DIR/add_media.sh" ]; then
                    "$SCRIPT_DIR/add_media.sh"
                else
                    echo -e "${RED}Error: add_media.sh not found or not executable${NC}"
                    echo "Expected location: $SCRIPT_DIR/add_media.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            4)
                echo ""
                echo -e "${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo ""
                echo -e "${RED}Invalid option. Please select 1-4.${NC}"
                sleep 1
                ;;
        esac
    done
}

main
