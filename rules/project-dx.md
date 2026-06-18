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
*   **Absolute vs. Relative Paths:** Ensure screenshot paths are relative to the repository root without a leading slash (e.g., `plans/feature/timestamp/image.png`) to render correctly in GitHub PRs.

## 3. GitHub Integration & CLI Tools
*   **Prefer `gh`:** When creating pull requests, managing repository secrets, or running CI/CD triggers, always prefer using the native GitHub CLI (`gh`) over standard git commands.

## 4. Resource Efficiency
*   **Zero Bloat:** Keep dependencies and script footprints tiny. Avoid heavy third-party npm or system dependencies in hook scripts or subagent definitions to keep setup times fast.
