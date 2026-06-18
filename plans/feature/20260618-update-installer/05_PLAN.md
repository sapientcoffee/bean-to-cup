# Execution Plan: Graceful Installer Self-Update

We will implement the refactored installation flow to enable robust in-place updates.

## Implementation Plan

### Step 1: Update `install.sh` Step 3 & 4
- [ ] Incorporate `UPDATED_IN_PLACE` tracking variable.
- [ ] Implement symlink path verification block.
- [ ] Implement git repository detection and `git -C "$FINAL_TARGET" pull --quiet` fallback block.
- [ ] Implement in-place folder copy sync (by skipping directory deletion unless `--force` is given).
- [ ] Wrap Section 4 (copying/moving) inside `if [[ "$UPDATED_IN_PLACE" == "false" ]]` block.

### Step 2: Verification and Manual Testing Walkthrough
- [ ] Run `./install.sh --link` first to create a link.
- [ ] Re-run `./install.sh --link` to verify the "already symlinked" no-op output.
- [ ] Create a mock git repository in a temp target, and run the script with a remote URL to test the `git pull` update logic.
- [ ] Verify that manual copy installs are updated in-place without removing untracked custom files (like mock plans or notes).

---

## Technical Contract & Safe-Checking
The script modifies only `/home/robedwards/workspace/bean-to-cup/install.sh`.
Since this is a bash installer script, we don't have functional Javascript/TypeScript tests to execute. Manual test-script validation and walkthrough captures will serve as verification proof.
