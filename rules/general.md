---
trigger: always_on
---

# ☕ Bean-to-Cup: General Developer Rules

Welcome to the **Bean-to-Cup** CLI plugin repository! This is an autonomous barista swarm designed to automate the software development lifecycle under the **Antigravity CLI (`agy`)**. 

To maintain the highest standards of code and architectural discipline, always adhere to the following rules:

## 1. The Perfect Brew (Stage 0 to Stage 9 SDLC Protocol)
*   **Entry-Agnostic Dashboard Lifecycle ("Create-if-Missing, Preserve & Update"):** A task may enter the SDLC pipeline at any stage (e.g. Stage 0 `ideator`, Stage 1 `grill`, Stage 2 `write-prd`, Stage 4 `system-design`, etc.). Every skill MUST use the central `visual-dashboard` skill / `python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py` protocol:
    - **If `visual-dashboard.html` does not exist**: Instantiate it from `templates/visual-dashboard.html` (`python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py ensure --plan-dir "..." --moniker "..."`) and populate `{{TIMESTAMP}}` & `{{MONIKER}}`.
    - **If `visual-dashboard.html` exists**: Retain all previously generated stage tabs (e.g. Discovery, Glossary, PRD, Spec) and update only the section corresponding to the active stage (`python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py update ...`).
    - **Dual-Write Guarantee**: Always mirror `visual-dashboard.html` to system artifacts (`python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py mirror ...`) so changes render live in the UI artifact viewer.
    0.  **Discovery/Ideation (Optional - `00_IDEATION.md` & `visual-dashboard.html`):** Formulate raw ideas, persona friction, and data schemas, publishing to the Discovery tab of the unified dashboard.
    1.  **Socratic Alignment (`docs/glossary.md` & `visual-dashboard.html`):** Engage in Socratic requirements gathering, build the global Ubiquitous Glossary, and publish to the Glossary tab inside the unified dashboard.
    2.  **PRD (`02_PRD.md` & `visual-dashboard.html`):** Establish requirements, non-goals, target personas, metrics, and acceptance criteria in both markdown and the Product PRD tab inside the unified dashboard.
    3.  **Extraction (`03_EXTRACTION.md`):** Conduct blind, factual codebase research using specialized sub-agents.
    4.  **Specification (`04_SPEC.md` & `visual-dashboard.html`):** Design the architecture aligned with local `design.md`, including threat model, telemetry, and the Design Spec tab inside the unified dashboard.
    5.  **Execution Planning (`05_PLAN.md` & `visual-dashboard.html`):** Establish physical contracts, cut vertical slices, perform dependency analysis, and synchronize task states in the Interactive Kanban Board on the Brew Overview tab of the unified dashboard.
    6.  **Human Review Gate (🛑 STOP):** Present design discussion, contracts, and unified visual dashboard to the user for explicit approval.
    7.  **TDD Implementation (`07_VERIFICATION.md` & `visual-dashboard.html`):** Spawn specialized subagents to execute implementation slices. Developers or agents interactively manage tasks inside the Interactive Kanban Board on the Brew Overview tab of the unified dashboard.
    8.  **Walkthrough (`08_WALKTHROUGH.md` & `visual-dashboard.html`):** Capture visual or technical proof via browser agent walkthrough or terminal playback recording (`record`), and generate the Recap tab of the unified dashboard detailing all changes.
    9.  **PR Delivery:** Push branches and open PRs using `gh` CLI, maintaining codebase hygiene with `/improve-codebase-architecture`.


## 2. Plugin Validation & Schema Compliance
*   **Continuous Validation:** All commands (`commands/*.toml`), skills (`skills/*/SKILL.md`), and hook files (`hooks.json`) must comply with the `agy 2.0` schema.
*   **Schema Checks:** Run `agy plugin validate .` to verify compilation, namespace mappings, and command declarations before finalizing any work.

## 3. Core Discipline (No Spec, No Code)
*   **Zero Improvisation:** Never write code directly without a corresponding and approved specification and implementation plan.
*   **Dual-Existence & Stage Handoff Protocol:** The markdown files (`02_PRD.md`, `04_SPEC.md`, `05_PLAN.md`, `07_VERIFICATION.md`, and `08_WALKTHROUGH.md`) coexist perfectly with `visual-dashboard.html` as the definitive, machine-parseable source of truth representing each stage. They are used directly by the test harness and model parsers as high-fidelity stage handoffs, ensuring full backward compatibility and automated parser interoperability.
*   **Licensing:** All new source files must contain the standard Google Apache 2.0 license header. Use the `google-license-manager` skill to automate this.
