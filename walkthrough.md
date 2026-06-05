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

## 🚀 Native Command Registration
All custom commands are successfully parsed and registered in `agy`:
*   **`/feature`**: Boots Phase 1 (Discovery & PRD drafting).
*   **`/research`**: Context-free codebase extraction.
*   **`/loop:start`**: Enters the Ralph self-correcting development loop.

All hooks are schema-compliant and validate cleanly with `agy plugin validate .`.
