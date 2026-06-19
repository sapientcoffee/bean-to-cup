---
trigger: always_on
---

# ☕ Bean-to-Cup Developer Experience (DX) Guidelines

Our goal is to build highly reliable, lightweight, and performant agent workflows for the Antigravity 2.0 CLI (`agy`).

## 1. Flat Namespace Commands
*   **Conventions:** All CLI commands placed in `commands/` must be flat `.toml` files matching the namespace standard (e.g., `commands/ddd:plan.toml`, `commands/brew:init.toml`).
*   **No Nesting:** Do not create nested command folders (e.g., `commands/ddd/plan.toml`), as they are ignored by the `agy` compiler.

## 2. Walkthrough Validation
*   **Testing Walkthroughs:** For any significant changes, always generate or update `walkthrough.md` to demonstrate proof of thorough manual testing, command validation, and successful registration.
*   **Terminal Walkthroughs (Asciinema):** For terminal-based or CLI-based validation, always consider and activate the **`asciinema`** skill. Generate a playback scenario JSON file (`walkthrough_scenario.json`) and run `brew:record` to capture high-fidelity executions and automatically compile them to animated `.gif` and `.cast` files.
*   **Asset Paths:** Ensure walkthrough screenshots and generated `.gif` files are stored inside the active plan directory and embedded in `08_WALKTHROUGH.md`, `walkthrough.md`, or pull requests using repository-root relative paths *WITHOUT* a leading slash (e.g., `plans/feature/timestamp/image.png` or `plans/feature/timestamp/walkthrough.gif`) to render correctly in GitHub PR descriptions.

## 3. GitHub Integration & CLI Tools
*   **Prefer `gh`:** When creating pull requests, managing repository secrets, or running CI/CD triggers, always prefer using the native GitHub CLI (`gh`) over standard git commands.

## 4. Resource Efficiency
*   **Zero Bloat:** Keep dependencies and script footprints tiny. Avoid heavy third-party npm or system dependencies in hook scripts or subagent definitions to keep setup times fast.

## 5. Artifact Mirroring (Dynamic UI Visibility)
*   **Dual-Write Requirement:** Whenever any stage-linked planning or documentation file is created or updated in the workspace (such as `01_GLOSSARY.md`, `02_PRD.md`, `03_EXTRACTION.md`, `04_SPEC.md`, `05_PLAN.md`, `07_VERIFICATION.md`, `08_WALKTHROUGH.md`, `walkthrough.md`, or `walkthrough.html`), you MUST also write it directly into the assistant's private system artifacts directory (`/home/robedwards/.gemini/antigravity-cli/brain/<conversation-id>/`) as a user-facing artifact (using descriptive, lowercase filenames like `02_prd.md` or `04_spec.md`).
*   **Purpose:** This mirrors workspace documentation inside the chat UI's persistent Artifacts viewer panel, making it incredibly easy to see and inspect what files have been created or modified without leaving the UI.
