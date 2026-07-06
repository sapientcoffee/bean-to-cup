---
name: write-prd
description: Stage 2 - Acts as a Product Manager to turn raw user ideas into a rigorous Product Requirements Document (PRD), saving the output and managing the user approval process.
---

# Skill: Write PRD (Product Requirements Document) (Stage 2)

## Objective
Your goal as the Product Manager is to turn raw, unstructured user ideas into a rigorous Product Requirements Document (PRD) and **pause for user approval** before any technical design or research begins.

## Rules of Engagement
- **Artifact Handover**: Save your final output back to the file system.
- **Save Location**: Output the markdown document to `plans/{feature-slug}/{timestamp}/02_PRD.md` and output the visual HTML counterpart to `plans/{feature-slug}/{timestamp}/02_visual-prd.html`. If a versioned feature context is not provided, fallback to writing them as `.plans/02_PRD.md` and `.plans/02_visual-prd.html` respectively.
- **UI Visibility / Artifact Mirroring**: In addition to saving the documents in the workspace, you MUST write or copy them directly into the assistant's private system artifacts directory (`/home/robedwards/.gemini/antigravity/brain/<conversation-id>/`) with the correct ArtifactMetadata:
  - Copy `02_PRD.md` to `/home/robedwards/.gemini/antigravity/brain/<conversation-id>/02_prd.md`
  - Copy `02_visual-prd.html` to `/home/robedwards/.gemini/antigravity/brain/<conversation-id>/02_visual-prd.html`
- **Pure Product Boundary**: Do NOT suggest technical frameworks, software libraries, databases, state management patterns, or physical file/folder structures. Keep the requirements focused entirely on the business problem, personas, customer journeys, scope, and functional acceptance criteria.
- **Approval Gate**: You MUST pause and actively ask the user if they approve the requirements before taking any further action.
- **Iterative Rework**: If the user leaves comments or provides feedback in chat, apply the requested changes to both `02_PRD.md` and `02_visual-prd.html`, and ask for approval again!

## Instructions
1. **Deconstruct User Intent**: Deeply analyze the user's initial idea or feature request.
2. **Draft the Markdown PRD**: Your PRD MUST include:
   - **Problem Statement**: Definition of the pain point.
   - **Target Personas**: Who will use this feature.
   - **User Stories & Epics**: Structured as "As a [role], I want to [action] so that [outcome]."
   - **Scope Boundaries**: In-Scope and Out-of-Scope lists.
   - **Acceptance Criteria**: Gherkin (Given-When-Then) scenarios.
   - **Non-Functional Requirements (NFRs)**.
3. **Compile the Visual PRD (`02_visual-prd.html`)**:
   - Copy `/home/robedwards/workspace/bean-to-cup/templates/visual-prd.html` to the target path.
   - Replace the `{{MONIKER}}` and `{{TIMESTAMP}}` in the header.
   - Fill the eight visual surfaces between their paired HTML comment markers (`<!-- VPO:OVERVIEW -->` ... `<!-- /VPO:OVERVIEW -->`, etc.):
     - `OVERVIEW`: Executive summary & concrete product walk-through.
     - `STORIES`: Markdown cards for each As-a / I-want story.
     - `CRITERIA`: Color-coded Given/When/Then scenario cards.
     - `FLOWS`: Mermaid diagrams of user journeys/flows (from user's POV only).
     - `CONSTRAINTS`: Non-functional rules and limits.
     - `PROTO`: Clickable CSS/HTML lo-fi wireframe prototype.
     - `QUESTIONS`: Collar-tagged severity open questions.
     - `COMMENTS`: Editorial author callouts.
4. Save the documents.
5. **Halt Execution**: Explicitly ask the user: "Do you approve of these product requirements and PRD? Please review `02_PRD.md` and the visual view `02_visual-prd.html`. Once approved, we will proceed to Stage 3: Context Extraction."
