# Socratic Alignment & Ubiquitous Glossary

This document establishes the ubiquitous language and socratic alignment for introducing graceful self-updates into the Bean-to-Cup plugin installer.

## Core Glossary

### Graceful Self-Update
The process by which the installer (`install.sh`) detects a pre-existing installation and cleanly incorporates upstream changes without performing a destructive wipe of the destination folder.
*Avoid*: Complete reinstall, destructive wipe, clean slate overwrite.

### Git Pull Integration
The mechanism of executing `git pull` inside a previously cloned plugin installation directory to fetch and merge upstream updates, preserving local git-untracked files, custom plans, and logs.
*Avoid*: Cloning over, rm -rf followed by clone.

### In-Place Copy Update
For non-git, non-symlinked installations, copying/syncing updated files directly into the active target directory to overwrite matching core files while keeping other custom plans, scratch directories, or logs untouched.
*Avoid*: Deleting the entire plugin folder before copying.

### Symlink No-Op Validation
Checking if the active target is already a symbolic link pointing to the desired local source path. If so, validating it and logging a successful no-op update instead of recreating or destroying it.
