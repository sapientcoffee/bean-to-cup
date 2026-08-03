---
trigger: always_on
---

# ☕ Bean-to-Cup: General Developer Rules

Welcome to the **Bean-to-Cup** CLI plugin repository! This is an autonomous barista swarm designed to automate the software development lifecycle under the **Antigravity CLI (`agy`)**. 

To maintain the highest standards of code and architectural discipline, always adhere to the following rules:

## 1. The Perfect Brew (Stage 0 to Stage 9 SDLC Protocol)
*   **Strict State Machine:** We treat software tasks as "Brews." You must follow the Stage 0-9 document-driven protocol, writing or updating active tabs in the single unified master **`visual-dashboard.html`** across each phase:
    0.  **Discovery/Ideation (Optional - `00_IDEATION.md`):** Formulate raw ideas, persona friction, and data schemas.
    1.  **Socratic Alignment (`docs/glossary.md` & `visual-dashboard.html`):** Engage in Socratic requirements gathering, build the global Ubiquitous Glossary, and publish to the Glossary tab inside the unified dashboard.
    2.  **PRD (`02_PRD.md` & `visual-dashboard.html`):** Establish requirements, non-goals, target personas, metrics, and acceptance criteria in both markdown and the Product PRD tab inside the unified dashboard.
    3.  **Extraction (`03_EXTRACTION.md`):** Conduct blind, factual codebase research using specialized sub-agents.
    4.  **Specification (`04_SPEC.md` & `visual-dashboard.html`):** Design the architecture aligned with local `design.md`, including threat model, telemetry, and the Design Spec tab inside the unified dashboard.
    5.  **Execution Planning (`05_PLAN.md`):** Establish physical contracts, cut vertical slices, and perform dependency analysis. Set up task states inside the Kanban Board tab of the unified dashboard.
    6.  **Human Review Gate (🛑 STOP):** Present design discussion, contracts, and unified visual dashboard to the user for explicit approval.
    7.  **TDD Implementation (`07_VERIFICATION.md` & `visual-dashboard.html`):** Spawn specialized subagents to execute implementation slices. Developers or agents interactively manage tasks inside the Kanban Board tab of the unified dashboard.
    8.  **Walkthrough (`08_WALKTHROUGH.md` & `visual-dashboard.html`):** Capture visual or technical proof via browser agent walkthrough or terminal playback recording (`record`), and generate the Recap tab of the unified dashboard detailing all changes.
    9.  **PR Delivery:** Push branches and open PRs using `gh` CLI, maintaining codebase hygiene with `/improve-codebase-architecture`.


## 2. Plugin Validation & Schema Compliance
*   **Continuous Validation:** All commands (`commands/*.toml`), skills (`skills/*/SKILL.md`), and hook files (`hooks.json`) must comply with the `agy 2.0` schema.
*   **Schema Checks:** Run `agy plugin validate .` to verify compilation, namespace mappings, and command declarations before finalizing any work.

## 3. Core Discipline (No Spec, No Code)
*   **Zero Improvisation:** Never write code directly without a corresponding and approved specification and implementation plan.
*   **Licensing:** All new source files must contain the standard Google Apache 2.0 license header. Use the `google-license-manager` skill to automate this.
