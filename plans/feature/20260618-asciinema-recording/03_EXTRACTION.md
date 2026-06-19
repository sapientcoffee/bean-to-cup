# ☕ Brew: Asciinema Terminal Recording Skill (03_EXTRACTION.md)

This Extraction document lists the factual findings from researching the workspace structure, existing commands, and dependency mechanics to establish the foundation for implementing the `asciinema` recording skill.

---

## 1. File & Schema Structures

### 1.1 CLI Commands (`commands/*.toml`)
Existing commands are configured as TOML files under `commands/`. Each file contains:
*   `description`: String metadata.
*   `prompt`: String containing LLM instructions.
*   No nested directories are supported (flat namespace).

### 1.2 Skills (`skills/*/SKILL.md`)
Skills are configured as directories containing a `SKILL.md` file. Each `SKILL.md` has:
*   YAML Frontmatter (containing `name` and `description`).
*   Body: Detailed instructions for the executing agent.

---

## 2. PTY and Recording Orchestration in Linux/Python
*   **PTY Control**: Python has a built-in `pty` module (`import pty`) which allows spawning a sub-process inside a pseudo-terminal. This is essential for `asciinema` to correctly capture interactive keyboard sizing, terminal codes, and color formatting.
*   **Scenario Playback**: A scenario runner script can read a JSON/YAML file and:
    1.  Spawn a bash/sh shell inside a PTY under `asciinema rec`.
    2.  Animate keypresses by writing characters to the PTY input descriptor with custom delays.
    3.  Feed the commands automatically, handling output logging.
*   **Static Binary Download**: The `agg` (Asciinema GIF Generator) static binary is hosted on GitHub Releases (`https://github.com/asciinema/agg/releases`). We can programmatically check system architecture (`uname -m`) and fetch the appropriate static binary (e.g., `x86_64` or `aarch64`) into `.agents/bin/` if it is not present in the system PATH.

---

## 3. Storage Convention Compliance
*   We must respect the dual-write rules for plan/documentation artifacts.
*   Walkthrough visual artifacts must be saved under the current plan directory (e.g., `plans/feature/20260618-asciinema-recording/`) and relative paths used in documents.
