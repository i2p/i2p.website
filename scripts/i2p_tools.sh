#!/bin/bash
#
# I2P Website Tools - All-in-One Menu
# Provides easy access to various website update utilities
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check and install dependencies
check_dependencies() {
    local missing=()

    # Check for Hugo
    if ! command -v hugo &>/dev/null; then
        missing+=("hugo")
    fi

    # Check for surge (npm package)
    if ! command -v surge &>/dev/null; then
        missing+=("surge")
    fi

    if [ ${#missing[@]} -eq 0 ]; then
        return 0
    fi

    echo ""
    echo -e "${YELLOW}Missing dependencies detected: ${missing[*]}${NC}"
    echo ""

    for dep in "${missing[@]}"; do
        case "$dep" in
            hugo)
                echo -e "${CYAN}Hugo is required for site building and preview.${NC}"
                echo -e "Would you like to install Hugo?"
                read -p "(y/n): " install_hugo
                if [[ "$install_hugo" =~ ^[Yy] ]]; then
                    install_hugo
                fi
                ;;
            surge)
                echo -e "${CYAN}Surge is required for preview hosting.${NC}"
                echo -e "Would you like to install Surge?"
                read -p "(y/n): " install_surge
                if [[ "$install_surge" =~ ^[Yy] ]]; then
                    install_surge
                fi
                ;;
        esac
    done

    echo ""
}

install_hugo() {
    echo -e "${BLUE}Installing Hugo...${NC}"

    if [ "$(uname)" = "Darwin" ]; then
        # macOS
        if command -v brew &>/dev/null; then
            brew install hugo
        else
            echo -e "${RED}Homebrew not found. Please install Hugo manually:${NC}"
            echo -e "  https://gohugo.io/installation/macos/"
            return 1
        fi
    elif [ "$(uname)" = "Linux" ]; then
        # Linux
        if command -v apt-get &>/dev/null; then
            sudo apt-get update && sudo apt-get install -y hugo
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y hugo
        elif command -v pacman &>/dev/null; then
            sudo pacman -S hugo
        elif command -v snap &>/dev/null; then
            sudo snap install hugo
        else
            echo -e "${RED}Could not detect package manager. Please install Hugo manually:${NC}"
            echo -e "  https://gohugo.io/installation/linux/"
            return 1
        fi
    else
        echo -e "${RED}Unsupported OS. Please install Hugo manually:${NC}"
        echo -e "  https://gohugo.io/installation/"
        return 1
    fi

    if command -v hugo &>/dev/null; then
        echo -e "${GREEN}Hugo installed successfully!${NC}"
    else
        echo -e "${RED}Hugo installation may have failed. Please verify.${NC}"
    fi
}

install_surge() {
    echo -e "${BLUE}Installing Surge...${NC}"

    # Check for npm
    if ! command -v npm &>/dev/null; then
        echo -e "${RED}npm not found. Please install Node.js first:${NC}"
        echo -e "  https://nodejs.org/"
        return 1
    fi

    npm install -g surge

    if command -v surge &>/dev/null; then
        echo -e "${GREEN}Surge installed successfully!${NC}"
        echo -e "${YELLOW}Note: You may need to run 'surge login' to authenticate.${NC}"
    else
        echo -e "${RED}Surge installation may have failed. Please verify.${NC}"
    fi
}

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
    echo -e "  ${CYAN}4)${NC} Add Blog Post"
    echo -e "  ${CYAN}5)${NC} Add Proposal"
    echo -e "  ${CYAN}6)${NC} Exit"
    echo ""
}

main() {
    # Check dependencies on startup
    check_dependencies

    while true; do
        show_header
        show_menu

        read -p "Select option: " choice

        case $choice in
            1)
                echo ""
                echo -e "${BLUE}Launching Banner Update Tool...${NC}"
                echo ""
                if [ -x "$TOOLS_DIR/update_banner.sh" ]; then
                    "$TOOLS_DIR/update_banner.sh"
                else
                    echo -e "${RED}Error: update_banner.sh not found or not executable${NC}"
                    echo "Expected location: $TOOLS_DIR/update_banner.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            2)
                echo ""
                echo -e "${BLUE}Launching Research Paper Tool...${NC}"
                echo ""
                if [ -x "$TOOLS_DIR/add_paper.sh" ]; then
                    "$TOOLS_DIR/add_paper.sh"
                else
                    echo -e "${RED}Error: add_paper.sh not found or not executable${NC}"
                    echo "Expected location: $TOOLS_DIR/add_paper.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            3)
                echo ""
                echo -e "${BLUE}Launching Media/Press Tool...${NC}"
                echo ""
                if [ -x "$TOOLS_DIR/add_media.sh" ]; then
                    "$TOOLS_DIR/add_media.sh"
                else
                    echo -e "${RED}Error: add_media.sh not found or not executable${NC}"
                    echo "Expected location: $TOOLS_DIR/add_media.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            4)
                echo ""
                echo -e "${BLUE}Launching Blog Post Tool...${NC}"
                echo ""
                if [ -x "$TOOLS_DIR/add_blog.sh" ]; then
                    "$TOOLS_DIR/add_blog.sh"
                else
                    echo -e "${RED}Error: add_blog.sh not found or not executable${NC}"
                    echo "Expected location: $TOOLS_DIR/add_blog.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            5)
                echo ""
                echo -e "${BLUE}Launching Proposal Tool...${NC}"
                echo ""
                if [ -x "$TOOLS_DIR/add_proposal.sh" ]; then
                    "$TOOLS_DIR/add_proposal.sh"
                else
                    echo -e "${RED}Error: add_proposal.sh not found or not executable${NC}"
                    echo "Expected location: $TOOLS_DIR/add_proposal.sh"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            6)
                echo ""
                echo -e "${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo ""
                echo -e "${RED}Invalid option. Please select 1-6.${NC}"
                sleep 1
                ;;
        esac
    done
}

main
