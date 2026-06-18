#!/usr/bin/env bash

# Robust error handling
set -euo pipefail

# Text formatting helper constants
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print banner
echo -e "${RED}${BOLD}===================================================${NC}"
echo -e "${RED}${BOLD}      ☕ Bean-to-Cup Plugin Uninstaller ☕        ${NC}"
echo -e "${RED}${BOLD}===================================================${NC}"

# Help message
show_help() {
    echo -e "Usage: $0 [OPTIONS]"
    echo ""
    echo -e "Options:"
    echo -e "  -g, --global      Uninstall from global plugins (~/.gemini/skills/) (Default)"
    echo -e "  -w, --workspace   Uninstall from the current workspace (.agents/skills/)"
    echo -e "  -h, --help        Show this help message"
    echo ""
    echo -e "Examples:"
    echo -e "  Uninstall globally:"
    echo -e "    $0"
    echo ""
    echo -e "  Uninstall from the current workspace:"
    echo -e "    $0 --workspace"
}

# Defaults
SCOPE="global"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -g|--global)
            SCOPE="global"
            shift
            ;;
        -w|--workspace)
            SCOPE="workspace"
            shift
            ;;
        *)
            echo -e "${RED}Error: Unknown argument '$1'${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Resolve paths
if [[ "$SCOPE" == "global" ]]; then
    TARGET_DIR="$HOME/.gemini/skills"
else
    # Find active workspace root (first directory up that has .git, or current directory)
    CURRENT_DIR="$PWD"
    WORKSPACE_ROOT=""
    while [[ "$CURRENT_DIR" != "/" ]]; do
        if [[ -d "$CURRENT_DIR/.git" ]]; then
            WORKSPACE_ROOT="$CURRENT_DIR"
            break
        fi
        CURRENT_DIR="$(dirname "$CURRENT_DIR")"
    done
    if [[ -z "$WORKSPACE_ROOT" ]]; then
        WORKSPACE_ROOT="$PWD"
    fi
    TARGET_DIR="$WORKSPACE_ROOT/.agents/skills"
fi

# Function to extract plugin name from plugin.json
get_plugin_name() {
    local dir="$1"
    if [[ ! -f "$dir/plugin.json" ]]; then
        # Default fallback if plugin.json is missing in current working directory
        echo "bean-to-cup"
        return
    fi
    local name
    name=$(grep -m 1 '"name":' "$dir/plugin.json" | sed -E 's/.*"name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
    if [[ -z "$name" ]]; then
        echo "bean-to-cup"
        return
    fi
    echo "$name"
}

# 1. Determine Script Directory & Plugin Name
SCRIPT_DIR=""
if [[ -f "./plugin.json" ]]; then
    SCRIPT_DIR="$PWD"
elif [[ -n "${BASH_SOURCE[0]:-}" && -f "$BASH_SOURCE" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
fi

if [[ -n "$SCRIPT_DIR" ]]; then
    PLUGIN_NAME=$(get_plugin_name "$SCRIPT_DIR")
else
    PLUGIN_NAME="bean-to-cup"
fi

FINAL_TARGET="$TARGET_DIR/$PLUGIN_NAME"

# 2. Check and Uninstall the Plugin
if [[ -e "$FINAL_TARGET" || -L "$FINAL_TARGET" ]]; then
    echo -e "${BLUE}Removing plugin directory or symlink at $FINAL_TARGET...${NC}"
    rm -rf "$FINAL_TARGET"
    echo -e "${GREEN}Successfully removed plugin files from disk.${NC}"
else
    echo -e "${YELLOW}Warning: Plugin '$PLUGIN_NAME' is not installed at $FINAL_TARGET.${NC}"
fi

# 3. Native agy CLI unregistration
if command -v agy &>/dev/null; then
    echo -e "${BLUE}Unregistering plugin natively from Antigravity CLI...${NC}"
    set +e
    # Try uninstalling by name
    agy plugin uninstall "$PLUGIN_NAME"
    REG_STATUS=$?
    set -e
    if [[ $REG_STATUS -eq 0 ]]; then
        echo -e "${GREEN}Plugin unregistered successfully in agy!${NC}"
    else
        # Fallback to absolute path just in case
        set +e
        agy plugin uninstall "$FINAL_TARGET"
        REG_STATUS_PATH=$?
        set -e
        if [[ $REG_STATUS_PATH -eq 0 ]]; then
            echo -e "${GREEN}Plugin unregistered successfully in agy!${NC}"
        else
            echo -e "${YELLOW}Warning: Native unregistration via 'agy plugin uninstall' returned an error (code $REG_STATUS).${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Warning: 'agy' CLI binary not found on PATH. Manual unregistration not possible.${NC}"
fi

# 4. Show beautiful completion message
echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "${GREEN}${BOLD} 🎉 Uninstall Completed Successfully! 🎉           ${NC}"
echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "Plugin Name:  ${BOLD}$PLUGIN_NAME${NC}"
echo -e "Scope:        ${BOLD}$SCOPE${NC}"
echo -e "Location:     ${BOLD}$FINAL_TARGET${NC}"
echo ""
echo -e "Antigravity CLI has been cleaned up. Next session will reload without this plugin."
