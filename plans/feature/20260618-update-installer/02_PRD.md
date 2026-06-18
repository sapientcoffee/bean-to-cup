# Product Requirements Document (PRD): Graceful Installer Self-Update

## 1. Objective
Refactor the plugin installation script (`install.sh`) to detect pre-existing installations and gracefully update or merge changes into them, rather than unconditionally forcing a destructive complete wipe (`rm -rf`) of the destination folder. This preserves local untracked files, custom plans, scratch scripts, and logs.

## 2. Target Personas & Friction
*   **Developer:** Runs local symlinks or direct git clones. Re-running `install.sh` to register or verify changes currently prompts them to completely delete and reinstall, resulting in losing progress in custom plan directories or untracked local scripts.
*   **Swarm Agent:** Re-runs installation scripts to verify or hook up plugins but may inadvertently wipe out its own plan documents (`.plans/` or `plans/`) or scratch script logs.

## 3. Requirements & Use Cases
*   **UC1: Existing Symlink (No-Op or Relink):**
    *   If a symlink exists and points to the correct source, do nothing or log that it is already active.
    *   If it points to a different source, safely recreate the link without touching other directories.
*   **UC2: Existing Git Repository (Git Pull):**
    *   If the target has a `.git` subdirectory, run a `git pull` directly inside the target directory.
    *   If successful, register the plugin and finish.
    *   If git pull fails (e.g., merge conflicts), warn the user and fall back to asking whether to overwrite completely or exit.
*   **UC3: Existing Copied Directory (In-Place Copy/Sync):**
    *   If copying files from local folders into a pre-existing directory, do not delete the destination folder first.
    *   Use `rsync` (if available) or copy files directly over, overriding matching files but keeping custom added files/directories (like `scratch/` or `.plans/`) completely intact.

## 4. Non-Goals
*   Solving complex git merge conflicts automatically (it will fall back to prompting for a clean reinstall if `git pull` fails).
*   Supporting downgrades automatically (standard pulling handles forward merges).
