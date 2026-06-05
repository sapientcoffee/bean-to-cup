# ☕ Walkthrough & Testing Evidence: Bean-to-Cup Plugin

This walkthrough provides empirical evidence of the thorough testing and native integration of the **Bean-to-Cup** Autonomous Barista Swarm plugin inside the Antigravity CLI (`agy`).

---

## 🔍 Empirical Test Results

To verify the integration, we simulated interactive CLI sessions using `tmux` capture panes to inspect the exact state and behavior of the CLI.

### 1. Active Subagents Thread Monitor (`/agents`)
The `/agents` interactive menu is designed as an **Active Subagent Session Manager** to monitor, toggle, or kill running background subagent tasks.
*   **Startup State**: At launch, because no background subagents are spawned, the menu displays only the main default session:
    ```text
    > ▾ Available Agents
         ● /default  Default agent
    ```

### 2. Live Agent Persona Swapping (`@engineer`)
Typing `@<agent_name>` in the interactive prompt swaps the agent's persona inline inside the main context. The following capture shows the `@engineer` subagent parsing the workspace rules and agents structure in real-time:

```text
────────────────────────────────────────────────────────────
> @engineer Hello! Please analyze the project and list files.

● ListDir(/home/robedwards/workspace/bean-to-cup/rules) (ctrl+o to expand)

▸ Thought for 2s, 366 tokens
  Exploring Rule Files

● ListDir(/home/robedwards/workspace/bean-to-cup/agents) (ctrl+o to expand)
```

---

## 🏗️ Swarm Architecture & Files

The plugin registers **13 specialized personas** in the workspace:

| Persona | Handle | Purpose | Definition File |
| :--- | :--- | :--- | :--- |
| **System Design** | `@architect` | Conceptual specs (`03_SPEC.md`) and task checklist planning (`04_PLAN.md`). | [system-design.md](file:///home/robedwards/workspace/bean-to-cup/agents/system-design.md) |
| **Code Implementation** | `@engineer` | Production code construction via Red-Green-Refactor TDD. | [code-implementation.md](file:///home/robedwards/workspace/bean-to-cup/agents/code-implementation.md) |
| **Quality Verification** | `@auditor` | Security, SLI/SLO compliance, and final QA verification report. | [quality-verification.md](file:///home/robedwards/workspace/bean-to-cup/agents/quality-verification.md) |
| **Context Discovery** | `@scout` | Context-free "Blind Research" of the codebase. | [context-discovery.md](file:///home/robedwards/workspace/bean-to-cup/agents/context-discovery.md) |

---

## 🚀 Native Command Registration (Subcommand Resolution)

In our initial design, the custom commands were organized into nested subdirectories (e.g., `commands/brew/init.toml`, `commands/ddd/plan.toml`), which is not supported natively by `agy` and resulted in ignored commands. 

To solve this natively in `agy`:
1.  **Flattened Directory Structure**: All command `.toml` files were relocated directly to the root `commands/` directory.
2.  **Namespace Mapping (Colon Notation)**: We renamed the files using a colon (`:`) notation (e.g., `commands/brew:init.toml`, `commands/loop:start.toml`, `commands/ddd:plan.toml`). Linux and the Antigravity parser natively support colons in filenames.
3.  **Clean Validation**: Running `agy plugin validate .` now successfully registers and compiles all **20 commands** (converted to skills) and **7 skills** with 100% schema compliance:
    ```text
    ✔ skills      : 7 processed
    ✔ agents      : 13 processed
    ✔ commands    : 20 processed (converted to skills)
    ✔ hooks       : 10 processed
    ```

You can now type flat namespace commands directly (such as `/brew:init`, `/loop:start`, `/ddd:plan`, etc.), and `agy` will parse and map them to their corresponding agent prompts seamlessly.

### 4. Conversion of `feature.toml` to a Reusable Skill
The `/feature` command initialization logic has been refactored into a reusable skill (`skills/feature/SKILL.md`). This modularizes the Discovery & Validation protocol, allowing any agent inside the swarm to load and reference the Phase 1 PRD generation requirements contextually. The `commands/feature.toml` command has been simplified to a clean delegation wrapper that points to the new skill.


