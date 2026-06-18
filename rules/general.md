---
trigger: always_on
---

# ☕ Bean-to-Cup: General Developer Rules

Welcome to the **Bean-to-Cup** CLI plugin repository! This is an autonomous barista swarm designed to automate the software development lifecycle under the **Antigravity CLI (`agy`)**. 

To maintain the highest standards of code and architectural discipline, always adhere to the following rules:

## 1. The Perfect Brew (Stage 0 to Stage 9 SDLC Protocol)
*   **Strict State Machine:** We treat software tasks as "Brews." You must follow the Stage 0-9 document-driven protocol:
    0.  **Discovery/Ideation (Optional - `00_IDEATION.md`):** Formulate raw ideas, persona friction, and data schemas.
    1.  **Socratic Alignment (`01_GLOSSARY.md`):** Engage in Socratic requirements gathering and build the Ubiquitous Glossary.
    2.  **PRD (`02_PRD.md`):** Establish requirements, non-goals, target personas, metrics, and acceptance criteria.
    3.  **Extraction (`03_EXTRACTION.md`):** Conduct blind, factual codebase research using specialized sub-agents.
    4.  **Specification (`04_SPEC.md`):** Design the architecture aligned with local `design.md`, including threat model and telemetry.
    5.  **Execution Planning (`05_PLAN.md`):** Establish physical contracts and cut vertical slices into checklist items.
    6.  **Human Review Gate (🛑 STOP):** Present design discussion & contracts to the user for explicit approval.
    7.  **TDD Implementation (`07_VERIFICATION.md`):** Execute code incrementally using TDD via `/tdd` (silent on success).
    8.  **Walkthrough (`08_WALKTHROUGH.md`):** Capture visual or technical proof via browser agent walkthrough.
    9.  **PR Delivery:** Push branches and open PRs using `gh` CLI, maintaining codebase hygiene with `/improve-codebase-architecture`.

## 2. Plugin Validation & Schema Compliance
*   **Continuous Validation:** All commands (`commands/*.toml`), skills (`skills/*/SKILL.md`), and hook files (`hooks.json`) must comply with the `agy 2.0` schema.
*   **Schema Checks:** Run `agy plugin validate .` to verify compilation, namespace mappings, and command declarations before finalizing any work.

## 3. Core Discipline (No Spec, No Code)
*   **Zero Improvisation:** Never write code directly without a corresponding and approved specification and implementation plan.
*   **Licensing:** All new source files must contain the standard Google Apache 2.0 license header. Use the `google-license-manager` skill to automate this.
