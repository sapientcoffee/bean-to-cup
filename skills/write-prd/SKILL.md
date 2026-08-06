---
name: write-prd
description: Stage 2 - Acts as a Product Manager to turn raw user ideas into a rigorous Product Requirements Document (PRD), saving the output and managing the user approval process.
---

# Skill: Write PRD (Product Requirements Document) (Stage 2)

## Objective
Your goal as the Product Manager is to turn raw, unstructured user ideas into a rigorous Product Requirements Document (PRD) and **pause for user approval** before any technical design or research begins.

## Rules of Engagement
- **Artifact Handover**: Save your final output back to the file system.
- **Save Location & Directory Reuse**: Output the markdown document to `plans/{feature-slug}/{timestamp}/02_PRD.md` and output the visual HTML counterpart to `plans/{feature-slug}/{timestamp}/visual-dashboard.html`. **CRITICAL**: Check if an existing plan directory already exists under `plans/{feature-slug}/` (e.g., created by `ideator` or a prior skill). If one exists, **REUSE that exact directory**. Do NOT create a new timestamp folder when `ideator` was run first. Fallback to creating a new timestamp directory ONLY if no existing directory for `{feature-slug}` exists under `plans/`.
- **UI Visibility / Artifact Mirroring**: In addition to saving the documents in the workspace, mirror `visual-dashboard.html` to system artifacts via `python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py mirror --plan-dir "plans/{feature-slug}/{timestamp}"`, and copy `02_PRD.md` to system artifacts as `02_prd.md`.
- **Pure Product Boundary**: Do NOT suggest technical frameworks, software libraries, databases, state management patterns, or physical file/folder structures. Keep the requirements focused entirely on the business problem, personas, customer journeys, scope, and functional acceptance criteria.
- **Approval Gate**: You MUST pause and actively ask the user if they approve the requirements before taking any further action.
- **Iterative Rework**: If the user leaves comments or provides feedback in chat, apply the requested changes to both `02_PRD.md` and `visual-dashboard.html`, and ask for approval again!

## Instructions
1. **Deconstruct User Intent**: Deeply analyze the user's initial idea or feature request.
2. **Draft the Markdown PRD**: Your PRD MUST include:
   - **Problem Statement**: Definition of the pain point.
   - **Target Personas**: Who will use this feature.
   - **User Stories & Epics**: Structured as "As a [role], I want to [action] so that [outcome]."
   - **Scope Boundaries**: In-Scope and Out-of-Scope lists.
   - **Acceptance Criteria**: Gherkin (Given-When-Then) scenarios.
   - **Non-Functional Requirements (NFRs) / Google Cloud Well-Architected Framework Pillars**: Reliability (self-healing, backups), Security (least-privilege IAM, VPC Service Controls, Cloud Secret Manager), Cost Optimization (right-sizing, cleanups), Performance Efficiency (indexes, cache, autoscaling thresholds).
   - **Deployment & DevOps Strategy**: Target GCP runtimes, Terraform Infrastructure-as-Code resources, CI/CD setup, and progressive release strategies (canary, rolling, blue-green).
   - **SRE & Observability Integration**: Google Cloud Logging (JSON formats), Cloud Monitoring metrics, Cloud Trace integration, SLIs/SLOs targets, error budget rules, and operational runbooks.
3. **Adversarial Red-Team Review Gate**:
   - Dispatch the subagent `@red-team-reviewer` to audit `02_PRD.md` for unhandled negative paths, missing rate-limiting bounds, ambiguous Gherkin steps, and security blind spots.
   - Refine `02_PRD.md` based on any Critical/High flaws identified during the adversarial audit.
4. **Generate Executable Evals (`evals/test_kpis.py`)**:
   - Parse all measurable KPIs and non-functional requirements in `02_PRD.md` and generate programmatic benchmark test scripts in `evals/test_kpis.py` (e.g. testing latency thresholds, error rate bounds, and payload limits).
5. **Compile the Visual PRD inside the Unified Dashboard (`visual-dashboard.html`)**:
   - Ensure `visual-dashboard.html` exists by executing `python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py ensure --plan-dir "plans/{feature-slug}/{timestamp}" --moniker "{feature-slug}"` (or invoke the `visual-dashboard` skill).
   - Automatically compile all PRD sections into full-fidelity HTML cards and render raw markdown by running:
     `python3 ~/.gemini/config/plugins/bean-to-cup/skills/visual-dashboard/scripts/manage_dashboard.py sync-prd --plan-dir "plans/{feature-slug}/{timestamp}" --moniker "{feature-slug}"`
   - **Zero Intermediate Snippet Files**: Do NOT write any temporary HTML files. `sync-prd` parses `02_PRD.md` directly and updates `visual-dashboard.html` in-place.
6. Save all documents (`02_PRD.md`, `evals/test_kpis.py`, `visual-dashboard.html`).
7. **Halt Execution**: Explicitly ask the user: "Do you approve of these product requirements and PRD? Please review `02_PRD.md`, the executable KPIs in `evals/test_kpis.py`, and the visual dashboard `visual-dashboard.html`. Once approved, we will proceed to Stage 3: Context Extraction."


