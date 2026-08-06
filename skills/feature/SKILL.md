---
name: feature
description: Stage 2 - Initialize a new feature development workflow (Discovery & Validation)
---

# Skill: Feature Discovery & Validation (Stage 2)

## Objective
Your goal is to act as the **Orchestration Engine** to initiate a new feature development workflow. You must capture the user's intent, clarify any ambiguities through Socratic alignment (`grill`), and establish the foundational `02_PRD.md` and unified master `visual-dashboard.html` artifacts with enterprise-grade rigor across clear execution gates.

## Core Mandate
- **Project Structure:** All artifacts MUST be stored in `plans/<feature-slug>/<YYYY-MM-DD_HHMM>/`.
- **Naming:** Use the feature name as the slug for the directory.
- **Verification & Interactivity:** You MUST use the `ask_question` tool (or direct interactive text questions) for ALL clarification questions.
- **Strict Execution Barrier:** You MUST NOT generate `02_PRD.md` in the initial turn. You MUST conduct the Socratic grilling phase first, present targeted clarifying questions, and **STOP execution** to await user answers.
- **Protocol:** Do NOT move to Stage 3 (Extraction/Research) until the user has explicitly approved the PRD.
- **Enterprise Standards:** You must explicitly address Non-Functional Requirements (NFRs) and Security Posture from the start.

## Instructions

### Step 1: Initialize & Resolve Context Directory
1. **Analyze Request & Passed Files:** Check if the user passed an explicit file path (e.g., `plans/<feature-slug>/<timestamp>/00_IDEATION.md`). If so, extract and REUSE that exact directory.
2. **Slugify Feature Name:** Determine the URL-friendly feature slug (e.g., "coffee-mood-app").
3. **Reuse Existing Plan Directory First:**
   - Check if an existing plan directory already exists under `plans/<feature-slug>/`.
   - If one or more timestamped directories exist (e.g., `plans/<feature-slug>/2026-08-05_1527/`), **REUSE the most recent existing plan directory**. Do NOT create a new timestamp directory when `ideator` or a prior stage was already run!
   - Preserve all existing files (`00_IDEATION.md`, `visual-dashboard.html`) in that directory and add new stage outputs (`02_PRD.md`, `03_EXTRACTION.md`, etc.) to it.
4. **Create New Directory (Fallback Only):** ONLY if no existing plan directory for `<feature-slug>` exists under `plans/`, run `date +%Y-%m-%d_%H%M` and create `plans/<feature-slug>/<timestamp>`.

### Step 2: Phase 1 — Socratic Alignment (`grill`)
1. **Execute Grill Skill (Stage 1 Socratic Alignment):** Call and execute the `grill` skill logic to conduct an interactive Socratic alignment session:
    - Read any pre-generated `00_IDEATION.md` to prime and guide the session.
    - Identify ambiguous requirements, edge cases, customer user journeys (CUJs), and Google Cloud Well-Architected pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency).
    - Formulate **3 to 5 targeted Socratic questions** focusing on unspecified boundaries, NFRs, and domain terminology.
    - Use the `ask_question` tool (or direct interactive output) to present these questions clearly to the user.
    - Document initial domain terms in `docs/glossary.md` and decisions in `docs/adr/`.
    - Generate or update the master `visual-dashboard.html` in `plans/<feature-slug>/<timestamp>/visual-dashboard.html` via `python3 scripts/manage_dashboard.py ensure --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"`.
    - Mirror the dashboard to system artifacts via `python3 scripts/manage_dashboard.py mirror --plan-dir "plans/<feature-slug>/<timestamp>"`.
2. 🛑 **HARD STOP (EXECUTION BARRIER)**: Stop calling tools and end your turn immediately after asking the grilling questions. **DO NOT** draft `02_PRD.md` or proceed to Stage 2 until the user responds to your questions!

### Step 3: Phase 2 — PRD Generation & Gating (After User Response)
1. **Incorporate Feedback:** Once the user provides answers to the Socratic grilling questions, update `docs/glossary.md` and `docs/adr/` accordingly.
2. **Draft Artifact:** Create `plans/<feature-slug>/<timestamp>/02_PRD.md` using the standard AI-Native PRD template:

   ```markdown
   # 02 PRD: <Feature Name>

   ## Objective
   [High-level summary of the feature's goal]

   ## User Stories
   - **As a [Role]**, I want [Goal], so that [Value].

   ## Phased Execution
   - [Phase 1: ...]
   - [Phase 2: ...]

   ## Non-Goals
   - [Hard boundary 1]
   - [Hard boundary 2]

   ## Evals & Metrics
   - [Metric 1: e.g. Performance < 200ms]
   - [Metric 2: e.g. Test coverage > 80%]

   ## Non-Functional Requirements (NFRs) - Google Cloud Well-Architected Framework
   - **Reliability:** [e.g. self-healing, backup plans, and rate-limiting limits]
   - **Security:** [e.g. IAM least-privilege scope, data encryption in transit and at rest]
   - **Cost Optimization:** [e.g. resource right-sizing rules, cleanup triggers, and retention policies]
   - **Performance Efficiency:** [e.g. database indexing requirements, caching rules, and autoscaling thresholds]
   - **Operational Excellence (Deployment & DevOps):** [e.g. CI/CD flow, Terraform Infrastructure-as-Code, progressive rollout style like canary/blue-green/rolling]
   - **Compliance:** [e.g. SOC2, GDPR]
   - **Accessibility:** [e.g. WCAG 2.1 AA]
   - **Data Residency:** [e.g. EU-West-1 only]

   ## Security Posture
   - [Security Assumption 1]
   - [Threat Vector Mitigation 1 (e.g. Cloud Secret Manager integration)]

   ## SRE Integration & Observability (SLIs/SLOs)
   - **Structured Logging:** [e.g. Google Cloud Logging standard JSON output format]
   - **Instrumentation & Metrics:** [e.g. Cloud Monitoring customs/standard metrics, Cloud Trace integration]
   - **SLI 1:** [e.g. Latency of GET /api/v1/resource < 200ms for 95% of requests]
   - **SLI 2:** [e.g. Availability of POST /api/v1/resource > 99.9%]
   - **Error Budget Policy:** [e.g. Actions taken if error budget is depleted]
   - **Runbooks & SOPs:** [e.g. References to standard recovery playbooks for known failure modes]
   ```

3. **Compile Visual PRD & Synchronize Dashboard (`visual-dashboard.html`)**:
   Run `python3 scripts/manage_dashboard.py auto-sync --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"` to parse `00_IDEATION.md`, `02_PRD.md`, `03_EXTRACTION.md`, `04_SPEC.md`, `05_PLAN.md`, update all tabs and Stage Tracker badges, and mirror all artifacts directly to the system artifacts directory.

### Step 4: Present and Gate
1. **Report Progress:** Inform the user that the directory, PRD, and visual dashboard companion have been created.
2. **Ask for Approval:** Ask the user to review the generated PRD artifacts:
   "Please review `plans/<feature-slug>/<timestamp>/02_PRD.md` and the visual companion `plans/<feature-slug>/<timestamp>/visual-dashboard.html`. Does this accurately reflect your vision? (Type 'approve' to move to Stage 3: Context Extraction)"
