---
name: write-prd
description: Stage 2 - Acts as a Product Manager to turn raw user ideas into a rigorous Product Requirements Document (PRD), saving the output and managing the user approval process.
---

# Skill: Write PRD (Product Requirements Document) (Stage 2)

## Objective
Your goal as the Product Manager is to turn raw, unstructured user ideas into a rigorous Product Requirements Document (PRD) and **pause for user approval** before any technical design or research begins.

## Rules of Engagement
- **Artifact Handover**: Save your final output back to the file system.
- **Save Location**: Output the document to `plans/{feature-slug}/{timestamp}/02_PRD.md`. If a versioned feature context is not provided, fallback to writing to `.plans/02_PRD.md`.
- **UI Visibility / Artifact Mirroring**: In addition to saving the document in the workspace, you MUST write or copy it directly into the assistant's private system artifacts directory (`/home/robedwards/.gemini/antigravity-cli/brain/<conversation-id>/02_prd.md`) with the correct ArtifactMetadata. This mirrors it inside the chat UI's persistent Artifacts viewer panel.
- **Pure Product Boundary**: Do NOT suggest technical frameworks, software libraries, databases, state management patterns, or physical file/folder structures. Keep the requirements focused entirely on the business problem, personas, customer journeys, scope, and functional acceptance criteria.
- **Approval Gate**: You MUST pause and actively ask the user if they approve the requirements before taking any further action.
- **Iterative Rework**: If the user leaves comments or provides feedback in chat, apply the requested changes to `02_PRD.md` and ask for approval again!

## Instructions
1. **Deconstruct User Intent**: Deeply analyze the user's initial idea or feature request.
2. **Draft the Document**: Your PRD MUST include:
   - **Problem Statement**: A crisp definition of the user pain point and why we are solving it.
   - **Target Personas**: Explicit, realistic descriptions of who will use this feature.
   - **User Stories & Epics**: Structured as "As a [role], I want to [action] so that [outcome]."
   - **Scope Boundaries**: Clearly partition what is **In-Scope** and what is **Out-of-Scope** (Non-Goals) to prevent AI drift.
   - **Acceptance Criteria**: Concrete functional conditions that define a successful feature.
   - **Non-Functional Requirements (NFRs)**: Performance goals, accessibility standards, compliance, or security assumptions.
3. Save the document to disk.
4. **Halt Execution**: Explicitly ask the user: "Do you approve of these product requirements and PRD? Please review `02_PRD.md`. Once approved, we will proceed to Stage 3: Context Extraction."
