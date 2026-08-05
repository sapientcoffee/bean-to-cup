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
    echo -e "  -g, --global      Install globally into ~/.gemini/ (Default)"
    echo -e "  -w, --workspace   Install into the current workspace (.agents/)"
    echo -e "  -l, --link        Create symlinks for local development instead of copying files"
    echo -e "  -f, --force       Overwrite any existing plugin installation without prompting"
    echo -e "  -h, --help        Show this help message"
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
    PLUGIN_BASE_DIR="$HOME/.gemini/config/plugins"
    SKILLS_BASE_DIR="$HOME/.gemini/skills"
else
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
    PLUGIN_BASE_DIR="$WORKSPACE_ROOT/.agents/plugins"
    SKILLS_BASE_DIR="$WORKSPACE_ROOT/.agents/skills"
fi

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

TMP_DIR=""
cleanup() {
    if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

SCRIPT_DIR=""
if [[ -f "./plugin.json" ]]; then
    SCRIPT_DIR="$PWD"
elif [[ -n "${BASH_SOURCE[0]:-}" && -f "$BASH_SOURCE" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
fi

if [[ -n "$GIT_URL" ]]; then
    SOURCE_MODE="git"
elif [[ -n "$SCRIPT_DIR" && -f "$SCRIPT_DIR/plugin.json" ]]; then
    SOURCE_MODE="local"
    SOURCE_DIR="$SCRIPT_DIR"
    PLUGIN_NAME=$(get_plugin_name "$SOURCE_DIR")
else
    GIT_URL="https://github.com/sapientcoffee/bean-to-cup.git"
    SOURCE_MODE="git"
fi

if [[ "$SOURCE_MODE" == "git" ]]; then
    echo -e "${BLUE}Cloning remote repository...${NC}"
    TMP_DIR=$(mktemp -d -t agy-plugin-XXXXXX)
    if ! git clone --quiet "$GIT_URL" "$TMP_DIR"; then
        echo -e "${RED}Error: Failed to clone repository from $GIT_URL${NC}"
        exit 1
    fi
    PLUGIN_NAME=$(get_plugin_name "$TMP_DIR")
    SOURCE_DIR="$TMP_DIR"
fi

# 1. Install Plugin Package to PLUGIN_BASE_DIR
mkdir -p "$PLUGIN_BASE_DIR"
FINAL_PLUGIN_TARGET="$PLUGIN_BASE_DIR/$PLUGIN_NAME"

if [[ -L "$FINAL_PLUGIN_TARGET" || -d "$FINAL_PLUGIN_TARGET" ]]; then
    rm -rf "$FINAL_PLUGIN_TARGET"
fi

if [[ "$LINK" == "true" ]]; then
    echo -e "${BLUE}Linking plugin '$PLUGIN_NAME' into $FINAL_PLUGIN_TARGET...${NC}"
    ln -sfn "$SOURCE_DIR" "$FINAL_PLUGIN_TARGET"
else
    echo -e "${BLUE}Syncing plugin '$PLUGIN_NAME' into $FINAL_PLUGIN_TARGET...${NC}"
    mkdir -p "$FINAL_PLUGIN_TARGET"
    if command -v rsync &>/dev/null; then
        rsync -a --exclude='.git' --exclude='.agents' --exclude='.plans' --exclude='.plan' --exclude='plans' --exclude='scratch' "$SOURCE_DIR/" "$FINAL_PLUGIN_TARGET/"
    else
        cp -R "$SOURCE_DIR"/. "$FINAL_PLUGIN_TARGET/"
        rm -rf "$FINAL_PLUGIN_TARGET/.git" "$FINAL_PLUGIN_TARGET/.agents" "$FINAL_PLUGIN_TARGET/.plans" "$FINAL_PLUGIN_TARGET/.plan" "$FINAL_PLUGIN_TARGET/plans" "$FINAL_PLUGIN_TARGET/scratch"
    fi
fi

# 2. Register Individual Skills in SKILLS_BASE_DIR
mkdir -p "$SKILLS_BASE_DIR"
if [[ -d "$SOURCE_DIR/skills" ]]; then
    for skill_dir in "$SOURCE_DIR/skills"/*; do
        if [[ -d "$skill_dir" ]]; then
            skill_name=$(basename "$skill_dir")
            skill_target="$SKILLS_BASE_DIR/$skill_name"
            if [[ "$LINK" == "true" ]]; then
                ln -sfn "$skill_dir" "$skill_target"
            else
                mkdir -p "$skill_target"
                if command -v rsync &>/dev/null; then
                    rsync -a "$skill_dir/" "$skill_target/"
                else
                    cp -R "$skill_dir"/. "$skill_target/"
                fi
            fi
            echo -e "${GREEN}  ✔ Registered skill: $skill_name${NC}"
        fi
    done
fi

# 3. Completion confirmation
echo -e "${GREEN}Plugin files and skills synchronized successfully!${NC}"

echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "${GREEN}${BOLD} 🎉 Installation Successful! 🎉                   ${NC}"
echo -e "${GREEN}${BOLD}===================================================${NC}"
echo -e "Plugin Name:  ${BOLD}$PLUGIN_NAME${NC}"
echo -e "Scope:        ${BOLD}$SCOPE${NC}"
echo -e "Plugin Path:  ${BOLD}$FINAL_PLUGIN_TARGET${NC}"
echo -e "Skills Path:  ${BOLD}$SKILLS_BASE_DIR${NC}"
echo ""
