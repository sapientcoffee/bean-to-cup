# Execution Plan: Graceful Installer Self-Update

We will implement the refactored installation flow to enable robust in-place updates.

## Implementation Plan

### Step 1: Update `install.sh` Step 3 & 4
- [x] Incorporate `UPDATED_IN_PLACE` tracking variable.
- [x] Implement symlink path verification block.
- [x] Implement git repository detection and `git -C "$FINAL_TARGET" pull --quiet` fallback block.
- [x] Implement in-place folder copy sync (by skipping directory deletion unless `--force` is given).
- [x] Wrap Section 4 (copying/moving) inside `if [[ "$UPDATED_IN_PLACE" == "false" ]]` block.

### Step 2: Verification and Manual Testing Walkthrough
- [x] Run `./install.sh --link` first to create a link.
- [x] Re-run `./install.sh --link` to verify the "already symlinked" no-op output.
- [x] Create a mock git repository in a temp target, and run the script with a remote URL to test the `git pull` update logic.
- [x] Verify that manual copy installs are updated in-place without removing untracked custom files (like mock plans or notes).

### Step 3: Symlink/Recursive Loop Prevention and Skill Compilation Fix
- [x] Modify `install.sh` to add `--exclude='.agents'` and `--exclude='plans'` (and `plans/` / `.agents/`) to both `rsync` and the `cp` fallback copy blocks to prevent recursive loops.
- [x] Wipe corrupted installations from `~/.gemini/skills/bean-to-cup` and `~/.gemini/config/plugins/bean-to-cup`.
- [x] Execute `./install.sh` to compile cleanly and confirm that `ideator` and all 13 skills are fully compiled and registered.

---

## Technical Contract & Safe-Checking
The script modifies only `/home/robedwards/workspace/bean-to-cup/install.sh`.
Since this is a bash installer script, we don't have functional Javascript/TypeScript tests to execute. Manual test-script validation and walkthrough captures will serve as verification proof.
