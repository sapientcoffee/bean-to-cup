# Technical Extraction: Analyzing Existing Installation Logic

This document details facts and logic extracted from the existing codebase regarding the installer (`install.sh`).

## Existing Codebase Analysis

### File: `install.sh`
*   **Target Directory Resolution:**
    *   Global Scope: `$HOME/.gemini/skills`
    *   Workspace Scope: `$WORKSPACE_ROOT/.agents/skills`
    *   Final target path: `FINAL_TARGET="$TARGET_DIR/$PLUGIN_NAME"` (line 172).

*   **Existing Pre-existing Check (lines 174-189):**
    ```bash
    # 3. Handle pre-existing installations
    if [[ -e "$FINAL_TARGET" || -L "$FINAL_TARGET" ]]; then
        if [[ "$FORCE" == "true" ]]; then
            echo -e "${YELLOW}Force option active. Overwriting existing installation at $FINAL_TARGET...${NC}"
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
    ```

*   **Installation Actions (lines 191-215):**
    *   If `SOURCE_MODE == git`:
        *   `mv "$TMP_DIR" "$FINAL_TARGET"` (moves cloned folder to final path).
    *   If `SOURCE_MODE == local`:
        *   If `LINK == true`: `ln -sfn "$SOURCE_DIR" "$FINAL_TARGET"`
        *   Else: Runs `rsync` or `cp -R` into `$FINAL_TARGET/`.

## Key Insights
1.  Currently, the check unconditionally runs `rm -rf "$FINAL_TARGET"` if overwriting.
2.  If the installer is re-run, even for a local development symlink, it prints a warning and prompts to overwrite (which deletes the symlink) before recreating it.
3.  If `SOURCE_MODE == git` (remote clone), we can check if `$FINAL_TARGET/.git` exists. If so, we can simply execute `git pull` inside `$FINAL_TARGET` and skip step 4 (the moving/copying process).
4.  If `SOURCE_MODE == local` and `LINK == true`, we can verify if the symlink already exists and points to the correct location. If it does, we can report a successful no-op update!
