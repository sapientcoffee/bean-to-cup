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
echo -e "${BLUE}${BOLD}===================================================${NC}"
echo -e "${BLUE}${BOLD}      ☕ Bean-to-Cup Plugin Installer ☕          ${NC}"
echo -e "${BLUE}${BOLD}===================================================${NC}"

# Help message
show_help() {
    echo -e "Usage: $0 [GIT_URL] [OPTIONS]"
    echo ""
    echo -e "Options:"
    echo -e "  -g, --global      Install globally into ~/.gemini/skills/ (Default)"
    echo -e "  -w, --workspace   Install into the current workspace (.agents/skills/)"
    echo -e "  -l, --link        Create a symlink for local development instead of copying files"
    echo -e "  -f, --force       Overwrite any existing plugin installation without prompting"
    echo -e "  -h, --help        Show this help message"
    echo ""
    echo -e "Examples:"
    echo -e "  Install the local directory globally (copies files):"
    echo -e "    $0"
    echo ""
    echo -e "  Link the local directory globally for development (symlinks):"
    echo -e "    $0 --link"
    echo ""
    echo -e "  Install from a remote git repository globally:"
    echo -e "    $0 https://github.com/sapientcoffee/bean-to-cup.git"
    echo ""
    echo -e "  Install from a remote git repository into the current workspace:"
    echo -e "    $0 https://github.com/sapientcoffee/bean-to-cup.git --workspace"
}

# Defaults
GIT_URL=""
SCOPE="global"
FORCE=false
LINK=false

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
        -l|--link)
            LINK=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        *)
            if [[ -z "$GIT_URL" ]]; then
                GIT_URL="$1"
            else
                echo -e "${RED}Error: Unknown argument '$1'${NC}"
                show_help
                exit 1
            fi
            shift
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
        echo -e "${RED}Error: Missing plugin.json in source directory.$NC" >&2
        exit 1
    fi
    local name
    name=$(grep -m 1 '"name":' "$dir/plugin.json" | sed -E 's/.*"name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
    if [[ -z "$name" ]]; then
        echo -e "${RED}Error: Could not parse plugin name from plugin.json.$NC" >&2
        exit 1
    fi
    echo "$name"
}

# Setup clean-up handler for temp directory if needed
TMP_DIR=""
cleanup() {
    if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

# 1. Determine Source & Plugin Name
SCRIPT_DIR=""
if [[ -f "./plugin.json" ]]; then
    SCRIPT_DIR="$PWD"
elif [[ -n "${BASH_SOURCE[0]:-}" && -f "$BASH_SOURCE" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
fi

if [[ -n "$GIT_URL" ]]; then
    # Remote Git installation specified
    SOURCE_MODE="git"
elif [[ -n "$SCRIPT_DIR" && -f "$SCRIPT_DIR/plugin.json" ]]; then
    # Local installation from current/script directory
    SOURCE_MODE="local"
    SOURCE_DIR="$SCRIPT_DIR"
    PLUGIN_NAME=$(get_plugin_name "$SOURCE_DIR")
else
    # Run via curl / pipe, or run in a folder without plugin.json
    # Default to cloning the main bean-to-cup repository!
    GIT_URL="https://github.com/sapientcoffee/bean-to-cup.git"
    SOURCE_MODE="git"
    echo -e "${YELLOW}No local plugin.json found. Defaulting to remote installation from:${NC}"
    echo -e "  ${BOLD}$GIT_URL${NC}"
    echo ""
fi

if [[ "$SOURCE_MODE" == "git" ]]; then
    # Remote Git installation
    echo -e "${BLUE}Cloning remote repository...${NC}"
    TMP_DIR=$(mktemp -d -t agy-plugin-XXXXXX)
    
    if ! git clone --quiet "$GIT_URL" "$TMP_DIR"; then
        echo -e "${RED}Error: Failed to clone repository from $GIT_URL${NC}"
        exit 1
    fi
    
    PLUGIN_NAME=$(get_plugin_name "$TMP_DIR")
fi

# 2. Prepare Target Directory
mkdir -p "$TARGET_DIR"
FINAL_TARGET="$TARGET_DIR/$PLUGIN_NAME"

UPDATED_IN_PLACE=false

# 3. Handle pre-existing installations
if [[ -e "$FINAL_TARGET" || -L "$FINAL_TARGET" ]]; then
    if [[ -L "$FINAL_TARGET" ]]; then
        # Handle symlink
        local_link_target=$(readlink "$FINAL_TARGET" || true)
        if [[ "$LINK" == "true" && "$local_link_target" == "$SOURCE_DIR" ]]; then
            echo -e "${GREEN}Plugin '$PLUGIN_NAME' is already symlinked correctly to $SOURCE_DIR.${NC}"
            UPDATED_IN_PLACE=true
        else
            echo -e "${YELLOW}Symlink exists but points elsewhere or configuration changed. Re-linking...${NC}"
            ln -sfn "$SOURCE_DIR" "$FINAL_TARGET"
            UPDATED_IN_PLACE=true
        fi
    elif [[ -d "$FINAL_TARGET/.git" ]]; then
        # Handle git repository pull
        if [[ "$FORCE" == "true" ]]; then
            echo -e "${YELLOW}Force option active. Overwriting existing repository...${NC}"
            rm -rf "$FINAL_TARGET"
        else
            echo -e "${BLUE}Existing Git repository found at $FINAL_TARGET.${NC}"
            echo -e "${BLUE}Attempting to update via git pull...${NC}"
            set +e
            git -C "$FINAL_TARGET" pull --quiet
            PULL_STATUS=$?
            set -e
            if [[ $PULL_STATUS -eq 0 ]]; then
                echo -e "${GREEN}Plugin successfully updated in-place via git pull!${NC}"
                UPDATED_IN_PLACE=true
            else
                echo -e "${YELLOW}Warning: git pull failed (possibly due to local conflicts).${NC}"
                read -p "Do you want to force overwrite the existing folder? [y/N] " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo -e "${YELLOW}Overwriting existing installation...${NC}"
                    rm -rf "$FINAL_TARGET"
                else
                    echo -e "${RED}Update cancelled due to unresolved merge conflicts.${NC}"
                    exit 1
                fi
            fi
        fi
    elif [[ "$SOURCE_MODE" == "local" && "$LINK" == "false" ]]; then
        # Handle in-place copy update
        if [[ "$FORCE" == "true" ]]; then
            echo -e "${YELLOW}Force option active. Overwriting existing installation...${NC}"
            rm -rf "$FINAL_TARGET"
        else
            echo -e "${BLUE}Existing directory found at $FINAL_TARGET.${NC}"
            echo -e "${BLUE}Performing in-place file sync...${NC}"
            # We skip deleting the folder, letting copying logic run in-place
            UPDATED_IN_PLACE=false
        fi
    else
        # Fallback for plain remote folder without git repo or other mismatch
        if [[ "$FORCE" == "true" ]]; then
            rm -rf "$FINAL_TARGET"
        else
            echo -e "${YELLOW}Warning: Installation already exists at $FINAL_TARGET${NC}"
            read -p "Do you want to overwrite it? [y/N] " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${RED}Installation cancelled.${NC}"
                exit 0
            fi
            rm -rf "$FINAL_TARGET"
        fi
    fi
fi

# 4. Install the Plugin (Only if not already updated in-place)
if [[ "$UPDATED_IN_PLACE" == "false" ]]; then
    if [[ "$SOURCE_MODE" == "git" ]]; then
        echo -e "${BLUE}Installing plugin '$PLUGIN_NAME' to $FINAL_TARGET...${NC}"
        # Move the temporary clone to the final destination
        mv "$TMP_DIR" "$FINAL_TARGET"
        # Nullify TMP_DIR so cleanup doesn't try to rm it
        TMP_DIR=""
    else
        if [[ "$LINK" == "true" ]]; then
            echo -e "${BLUE}Linking local plugin '$PLUGIN_NAME' to $FINAL_TARGET...${NC}"
            # Create symlink pointing to the local directory
            ln -sfn "$SOURCE_DIR" "$FINAL_TARGET"
        else
            echo -e "${BLUE}Copying local plugin '$PLUGIN_NAME' to $FINAL_TARGET...${NC}"
            mkdir -p "$FINAL_TARGET"
            # Copy files robustly, excluding git/temporary folders if present
            if command -v rsync &>/dev/null; then
                rsync -a --exclude='.git' --exclude='.plans' --exclude='.plan' --exclude='scratch' "$SOURCE_DIR/" "$FINAL_TARGET/"
            else
                cp -R "$SOURCE_DIR"/. "$FINAL_TARGET/"
                # Clean up git/scratch folders if they got copied
                rm -rf "$FINAL_TARGET/.git" "$FINAL_TARGET/.plans" "$FINAL_TARGET/.plan" "$FINAL_TARGET/scratch"
            fi
        fi
    fi
fi


# 5. Native agy CLI registration
if command -v agy &>/dev/null; then
    echo -e "${BLUE}Registering plugin natively with Antigravity CLI...${NC}"
    set +e
    agy plugin install "$FINAL_TARGET"
    REG_STATUS=$?
    set -e
    if [[ $REG_STATUS -eq 0 ]]; then
        echo -e "${GREEN}Plugin registered successfully in agy!${NC}"
    else
        echo -e "${YELLOW}Warning: Native registration via 'agy plugin install' returned an error (code $REG_STATUS), but files are successfully placed.${NC}"
    fi
else
    echo -e "${YELLOW}Warning: 'agy' CLI binary not found on PATH. Please ensure it is installed.${NC}"
fi

# 6. Show beautiful completion message
echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "${GREEN}${BOLD} 🎉 Installation Successful! 🎉                   ${NC}"
echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "Plugin Name:  ${BOLD}$PLUGIN_NAME${NC}"
echo -e "Scope:        ${BOLD}$SCOPE${NC}"
echo -e "Location:     ${BOLD}$FINAL_TARGET${NC}"
if [[ "$SOURCE_MODE" == "local" ]]; then
    if [[ "$LINK" == "true" ]]; then
        echo -e "Type:         ${BLUE}Symlinked Local Directory (Development)${NC}"
    else
        echo -e "Type:         ${BLUE}Copied Local Directory${NC}"
    fi
else
    echo -e "Type:         ${BLUE}Cloned Remote Git Repository${NC}"
fi
echo ""
echo -e "Antigravity CLI will automatically detect and load this plugin on your next session."
