---
name: feature
description: Stage 2 - Initialize a new feature development workflow (Discovery & Validation)
---

# Skill: Feature Discovery & Validation (Stage 2)

## Objective
Your goal is to act as the **Orchestration Engine** to initiate a new feature development workflow. You must capture the user's intent, clarify any ambiguities, and establish the foundational `02_PRD.md` artifact with enterprise-grade rigor.

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
1. **Clarify Intent:** If the request is vague, ask focused discovery questions via the `ask_user` tool to uncover:
    - **User Stories:** Who is this for and what is the primary goal?
    - **Non-Goals:** What are we explicitly NOT doing?
    - **Metrics:** How do we quantitatively measure success?
    - **NFRs:** What are the compliance (SOC2/GDPR), accessibility (WCAG), and residency requirements?
    - **Security:** What are the core security assumptions and threat vectors?
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

   ## Non-Functional Requirements (NFRs)
   - **Compliance:** [e.g. SOC2, GDPR]
   - **Accessibility:** [e.g. WCAG 2.1 AA]
   - **Data Residency:** [e.g. EU-West-1 only]

   ## Security Posture
   - [Security Assumption 1]
   - [Threat Vector Mitigation 1]

   ## SRE Integration (SLIs/SLOs)
   - [SLI 1: ...]
   ```

### Step 3: Present and Gate
1. **Report Progress:** Inform the user that the directory and PRD have been created.
2. **Ask for Approval:** Ask the user to review the generated PRD:
   "Please review `plans/<feature-slug>/<timestamp>/02_PRD.md`. Does this accurately reflect your vision? (Type 'approve' to move to Stage 3: Context Extraction)"
