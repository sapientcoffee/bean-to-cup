# ☕ Bean-to-Cup: The Autonomous Barista Swarm

**Bean-to-Cup** is a comprehensive Gemini CLI extension designed to automate the entire Software Development Lifecycle (SDLC). It transforms the AI from a simple code generator into a structured **Autonomous Brewing Team** that follows a rigorous, multi-phase protocol to deliver high-quality, verified software.

---

## 📖 Core Philosophy: "The Perfect Brew"

Just as a master barista follows a precise recipe—from selecting the beans to the final pour—this extension treats software features as "Brews." It enforces a strict **State Machine** to ensure:
1.  **Strategic Discovery**: No code is written until the intent is perfectly clear.
2.  **Unbiased Research**: The current system is mapped factually before changes are planned.
3.  **TDD Implementation**: Every change is driven by tests and verified by an independent auditor.
4.  **Evidence-Based Delivery**: A final walkthrough provides visual and technical proof of success.

---

## 🏗️ Architectural Overview

### 1. The Head Barista (Main Context)
The heart of the extension is the `bean-to-cup.md` file (merged into the model's context). It acts as the **Supervisor** and **Guardian of the Protocol**. It does not write code; it orchestrates the swarm.

**The Stage 0 to Stage 9 SDLC Protocol:**
*   **Stage 0: Discovery / Ideation (Optional)**: Brainstorming and drafting ideas (`00_IDEATION.md`).
*   **Stage 1: Socratic Alignment (The Grill)**: Gathering requirements, compiling glossary, and ADRs (`01_GLOSSARY.md`).
*   **Stage 2: Product Requirements**: Structuring PRD with personas and NFRs (`02_PRD.md`).
*   **Stage 3: Context Extraction**: Context-firewall factual research via sub-agents (`03_EXTRACTION.md`).
*   **Stage 4: Technical Specification**: High-level design, SRE telemetry, Threat Model (`04_SPEC.md`).
*   **Stage 5: Execution Planning**: Slices, checklist plan, and physical contracts (`05_PLAN.md`).
*   **Stage 6: Human Review Gate**: Mandatory STOP for user approval of contracts/specs before code execution.
*   **Stage 7: Test-Driven Implementation**: Incremental CDD TDD iteration loop (`07_VERIFICATION.md`).
*   **Stage 8: Automated Walkthrough**: Browser-agent walkthrough and visual evidence (`08_WALKTHROUGH.md`).
*   **Stage 9: PR Delivery & Maintenance**: Push branches and create PRs via `gh` CLI.

---

## 🤖 The Brewing Swarm (Agents)

Invoke specialized sub-agents using `@<name>`:

| Agent | Role | Expertise |
| :--- | :--- | :--- |
| **`@architect`** | The Planner | Design patterns, roadmap management, and TDD task splitting. |
| **`@engineer`** | The Builder | Production-ready code, TDD (Red-Green-Refactor), and ES Modules. |
| **`@auditor`** | The Gatekeeper | Security auditing, SOLID compliance, and test verification. |
| **`@scout`** | The Investigator | Factual codebase mapping and dependency tracing. |
| **`@codebase-analyzer`** | The Cartographer | Deep surgical analysis of implementation details (Factual only). |
| **`@security-auditor`** | The Sentry | Hunting for OWASP vulnerabilities and logic flaws. |
| **`@code-review`** | The Critic | Identifying performance traps and architectural drift. |

---

## ⌨️ Custom Commands

| Command | Namespace | Purpose |
| :--- | :--- | :--- |
| **`/feature`** | Core | Initiates the 9-phase brewing protocol for a new feature. |
| **`/brew:init`** | Brew | *(Deprecated)* Bootstraps a local project with the Head Barista protocol (now handled automatically in AGY 2.0). |
| **`/brew:archive`** | Brew | Clears away 'spent grounds' (completed tasks) to keep context clean. |
| **`/research`** | Core | Spawns parallel agents for deep, factual codebase extraction. |
| **`/loop:start`** | Loop | Starts an infinite, self-correcting development loop (Ralph). |
| **`/ddd:*`** | DDD | A specialized 7-step pipeline for refactoring SQL to modern .NET/DDD. |
| **`/dev`** | Ops | Starts backend and frontend local servers in the background. |
| **`/build:prod`** | Ops | Runs linting and production builds. |

---

## 🛠️ Reusable Skills

Skills are specialized instructions pulled into the agent's context as needed:
*   **`audit-code`**: Phase 7: QA assessment against technical specs.
*   **`write-specs`**: Phase 1: Transforming vague ideas into rigorous technical specifications.
*   **`generate-code`**: Phase 7: Full-stack scaffolding and implementation.
*   **`deploy-app`**: Phase 7: Stack detection and automated local hosting.
*   **`github-workflow`**: Phase 9: Standardized branch management and PR creation using `gh`.
*   **`chaos-mitigation`**: Phase 7: Observability-driven troubleshooting for degraded states.
*   **`kanban`**: Phase 7: Interactive progress tracking (HTML & Mermaid visualizer) for vertical slices.

---

## 🪝 Automated Hooks

These scripts run automatically based on CLI events:
*   **`lint-on-change`**: Runs `npm run lint` or `turbo lint` whenever a file is modified.
*   **`coffee-and-git`**: Injects a fresh coffee tip and the last 3 git commits at the start of every session.
*   **`git-status`**: Keeps the current branch and modified file count visible in the context.
*   **`stop-loop`**: The logic gate for the Ralph implementation loop mechanism.

---

## 📁 Directory Structure

```text
bean-to-cup/
├── agents/             # Sub-agent definitions (.md with YAML frontmatter)
├── commands/           # Custom command definitions (.toml)
├── hooks/              # Shell scripts and hook configurations (hooks.json)
├── policies/           # Tool-usage and security restrictions (.toml)
├── rules/              # Project mandates and developer guidelines (.md)
├── skills/             # Reusable agent capabilities (SKILL.md)
├── workflows/          # Automated execution sequences (.md)
├── bean-to-cup.md      # The "Head Barista" Supervisor protocol
├── gemini-extension.json # Extension manifest and metadata
└── README.md           # User-facing quickstart and reference
```

---

## 🚀 Getting Started

1.  **Link the Extension**:
    ```bash
    gemini extensions link /path/to/bean-to-cup
    ```
2.  **Initialize your Workspace (Deprecated)**:
    > [!NOTE]
    > Under Antigravity 2.0, bootstrapping is handled automatically upon registration. If you are on the legacy Gemini CLI, you can still optionally run:
    ```bash
    /brew:init
    ```
3.  **Start a Feature Brew**:
    ```bash
    /feature "Add a search bar to the coffee bean catalog"
    ```

---
*Created with ❤️ by the Bean-to-Cup team.*
