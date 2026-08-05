---
name: feature
description: Stage 2 - Initialize a new feature development workflow (Discovery & Validation)
---

# Skill: Feature Discovery & Validation (Stage 2)

## Objective
Your goal is to act as the **Orchestration Engine** to initiate a new feature development workflow. You must capture the user's intent, clarify any ambiguities, and establish the foundational `02_PRD.md` and unified master `visual-dashboard.html` artifacts with enterprise-grade rigor.

## Core Mandate
- **Project Structure:** All artifacts MUST be stored in `plans/<feature-slug>/<YYYY-MM-DD_HHMM>/`.
- **Naming:** Use the feature name as the slug for the directory.
- **Verification:** You MUST use the `ask_user` tool for ALL clarification questions.
- **Protocol:** Do NOT move to Stage 3 (Extraction/Research) until the user has explicitly approved the PRD.
- **Enterprise Standards:** You must explicitly address Non-Functional Requirements (NFRs) and Security Posture from the start.

## Instructions

### Step 1: Initialize Context
1. **Analyze Request:** Analyze the user's feature request and goals.
2. **Slugify Feature Name:** Determine a URL-friendly slug for the feature (e.g., "add-login-page").
3. **Get Timestamp:** Run `date +%Y-%m-%d_%H%M` via a terminal command execution.
4. **Create Directory:** Create the versioned plan directory: `plans/<feature-slug>/<timestamp>`.

### Step 2: Discovery & PRD
1. **Execute Grill Skill (Stage 1 Socratic Alignment):** Call and execute the `grill` skill to conduct a relentless, interactive Socratic requirements gathering and alignment session. Do NOT rely on simple/passive discovery questions. Under the `grill` skill, you must:
    - Search for any pre-generated `00_IDEATION.md` to prime and guide the session.
    - Run an interactive `/grilling` session, actively challenging user terms against the ubiquitous language, sharpening fuzzy requirements, and probing edge cases.
    - **Google Cloud Alignment:** Actively stress-test design assumptions against Google Cloud Well-Architected pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency), deployment strategies (Cloud Run, GKE, progressive delivery), and robust observability/SRE concepts.
    - Document terms inside the global glossary (`docs/glossary.md`) on-the-fly (never write a local `01_GLOSSARY.md`).
    - Record architectural decisions as ADRs inside `docs/adr/`.
    - Generate or update the unified master `visual-dashboard.html` in `plans/<feature-slug>/<timestamp>/visual-dashboard.html` via `python3 scripts/manage_dashboard.py ensure --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"`, rendering terms in `<!-- VG:GLOSSARY -->` and ADRs in `<!-- VG:ADR -->`.
    - Mirror the dashboard to system artifacts via `python3 scripts/manage_dashboard.py mirror --plan-dir "plans/<feature-slug>/<timestamp>"`.
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

3. **Compile Visual PRD inside the Unified Dashboard (`visual-dashboard.html`)**:
   Follow the `write-prd` skill to update and fill the PRD sections (Overview, Stories, Criteria, Flows, Constraints, etc.) inside the unified master `visual-dashboard.html` in the versioned plans directory using `python3 scripts/manage_dashboard.py update`, and mirror both files directly to the system artifacts directory:
   - Copy `02_PRD.md` to system artifacts directory as `02_prd.md`
   - Mirror `visual-dashboard.html` via `python3 scripts/manage_dashboard.py mirror --plan-dir "plans/<feature-slug>/<timestamp>"`

### Step 3: Present and Gate
1. **Report Progress:** Inform the user that the directory, PRD, and visual dashboard companion have been created.
2. **Ask for Approval:** Ask the user to review the generated PRD artifacts:
   "Please review `plans/<feature-slug>/<timestamp>/02_PRD.md` and the visual companion `plans/<feature-slug>/<timestamp>/visual-dashboard.html`. Does this accurately reflect your vision? (Type 'approve' to move to Stage 3: Context Extraction)"
