# ☕ Brew: Asciinema Terminal Recording Skill (05_PLAN.md)

This execution plan outlines the step-by-step implementation tasks (slices) for building the Asciinema Terminal Recording feature, marked as parallelizable (`[Parallel]`) or serial (`[Serial]`).

---

## 1. Implementation Slices

### 🟩 Slice 1: Workspace Scaffolding & Setup `[Serial]`
*   **Tasks**:
    - Ensure `scripts/` folder exists.
    - Ensure `docs/recordings/` exists.
    - Add `.agents/bin/` pattern to `.gitignore` to avoid checking downloaded third-party binaries into Git.
*   **Dependencies**: None

### 🟩 Slice 2: Orchestration, Playback Script, & TMUX Integration `[Serial]`
*   **Tasks**:
    - Implement CLI argument parsing for `--scenario`, `--output`, `--upload` in `scripts/record.py`.
    - Implement `agg` binary self-healing detection and downloading from GitHub Releases.
    - Implement the `scripts/playback.py` playback script (types prompt, comments, commands with realistic delays, executes commands via subprocess).
    - Implement `tmux` orchestration in `scripts/record.py` (spawns detached session, sets 100x30 screen size, runs asciinema and playback script, polls for completion).
    - Implement standard backup fallback if `tmux` is absent.
*   **Dependencies**: Slice 1

### 🟩 Slice 3: CLI Command Declaration (`commands/brew:record.toml`) `[Parallel]`
*   **Tasks**:
    - Write `commands/brew:record.toml` defining the CLI schema for the `agy` compiler.
*   **Dependencies**: Slice 2

### 🟩 Slice 4: Agent Skill Integration (`skills/asciinema/SKILL.md`) `[Parallel]`
*   **Tasks**:
    - Write the YAML-frontmatter and instructions in `skills/asciinema/SKILL.md`.
*   **Dependencies**: Slice 2

### 🟩 Slice 5: Verification & Walkthrough Hook `[Serial]`
*   **Tasks**:
    - Create a small test scenario file.
    - Run `agy plugin validate .` to verify compilation and namespace mapping.
    - Execute a scripted run under tmux to verify cast file creation and automated GIF rendering.
*   **Dependencies**: Slices 3, 4

---

## 2. Human Review Gate (🛑 STOP)

This plan requires human developer approval before proceeding to implementation.
Once approved, we will:
1. Initialize the files of Slices 1 and 2.
2. Implement Slices 3 and 4 in parallel.
3. Verify using Slice 5 and generate `08_WALKTHROUGH.md`.
