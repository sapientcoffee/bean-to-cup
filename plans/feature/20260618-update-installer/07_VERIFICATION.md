# Test-Driven Verification

Since this is a bash script, standard functional unit testing frameworks are not applicable. Instead, we perform incremental verification using strict manual validation scripts and directory state assertions.

## Verification Checklist & Test Cases

### TC1: Initial Clean Installation (Workspace Scope)
- **Action:** Run `./install.sh --workspace --force` to guarantee a clean slate.
- **Result:** Successfully created a copied directory at `.agents/skills/bean-to-cup`.
- **Status:** PASS

### TC2: Symlink Creation & Validation (No-Op Path)
- **Action:**
  1. Run `./install.sh --link` to create a global symlink pointing to the current local repository.
  2. Run `./install.sh --link` again.
- **Expected Output:** `Plugin 'bean-to-cup' is already symlinked correctly to /home/robedwards/workspace/bean-to-cup.` (or similar).
- **Result:** Log output matched perfectly:
  ```
  Plugin 'bean-to-cup' is already symlinked correctly to /home/robedwards/workspace/bean-to-cup.
  ```
- **Status:** PASS

### TC3: Directory In-Place Update (Preserving Untracked User Files)
- **Action:**
  1. Install using `./install.sh --workspace`.
  2. Create a custom untracked text file: `.agents/skills/bean-to-cup/my_custom_config.txt`.
  3. Re-run `./install.sh --workspace` without `--force`.
- **Expected Output:**
  ```
  Existing directory found at /home/robedwards/workspace/bean-to-cup/.agents/skills/bean-to-cup.
  Performing in-place file sync...
  ```
  The script completes successfully and does **NOT** prompt to overwrite or delete the folder.
  Verify that `.agents/skills/bean-to-cup/my_custom_config.txt` is preserved.
- **Result:**
  * Log outputs matched perfectly.
  * `my_custom_config.txt` was verified to be intact and unaffected.
- **Status:** PASS

### TC4: Symlink/Recursive Loop Prevention and Skill Compilation
- **Action:**
  1. Add `.agents` and `plans` exclusions to copy blocks in `install.sh`.
  2. Wipe out previous corrupted folders under `~/.gemini/skills/` and `~/.gemini/config/plugins/`.
  3. Execute `./install.sh` to perform a clean copy install.
- **Expected Output:**
  * No file name too long errors or recursive copying loops.
  * Successfully registers 13 skills, 13 agents, 19 commands, and 1 hook with `exit 0`.
  * Verify that all 13 compiled skills (including `ideator`) are successfully created inside `~/.gemini/config/plugins/bean-to-cup/skills/`.
- **Result:**
  * Compiled successfully with no warnings/errors.
  * All 13 skills compiled cleanly, and `ideator` is verified to be fully loaded and functioning.
- **Status:** PASS
