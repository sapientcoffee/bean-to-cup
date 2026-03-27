# Implementation Plan: Evolve State Machine Workflow

## Objective
Update the Swarm execution protocol in `system.md` and the Mermaid diagram in `README.md` to reflect the new agentic workflow based on the "question -> research -> design -> structure -> plan -> worktree -> implement -> PR" approach.

## Key Files & Context
- `system.md`: Contains the core execution protocol and state machine for the Supervisor agent.
- `README.md`: Contains the Mermaid diagram and high-level documentation of the Swarm lifecycle.

## Implementation Steps

1. **Update `system.md`:**
   - Modify the "🧠 CORE RESPONSIBILITIES" section to list the new 8-phase pipeline.
   - Replace the existing "PHASE 1" through "PHASE 5" with the new detailed phases:
     - **PHASE 1: QUESTION** (Clarify goal)
     - **PHASE 2: RESEARCH** (Scout/Investigator maps codebase)
     - **PHASE 3: DESIGN** (Architect drafts high-level design)
     - **PHASE 4: STRUCTURE** (Architect defines file skeletons/directory structure)
     - **PHASE 5: PLAN** (Architect creates task plans & stops for human review)
     - **PHASE 6: WORKTREE** (Supervisor creates isolated git branch/worktree)
     - **PHASE 7: IMPLEMENTATION LOOP** (Engineer implements, Auditor verifies, Supervisor commits)
     - **PHASE 8: PULL REQUEST** (Supervisor pushes branch and creates PR)

2. **Update `README.md`:**
   - Update the Mermaid `graph TD` block in the "🔄 Protocol Lifecycle" section to visually represent the new 8-step flow: Start -> Question -> Research -> Design -> Structure -> Plan -> Worktree -> Implement/Verify Loop -> Git Commit -> PR.
   - Update the descriptive text around the diagram to align with the new phase names.

## Verification & Testing
- Read the updated `system.md` to ensure no original constraints (like "NO DIRECT CODING" and "STRICT GIT") were accidentally lost.
- Run a markdown preview/linter on `README.md` to ensure the new Mermaid syntax is valid.
- Verify that the workflow logically flows and correctly assigns the appropriate existing agents (`architect`, `engineer`, `auditor`, `scout`) to their respective steps.