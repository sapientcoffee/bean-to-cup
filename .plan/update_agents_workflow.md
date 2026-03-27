# Implementation Plan: Update Agents for 8-Phase Workflow

## Objective
Update the swarm agents (`scout`, `architect`, `engineer`, `auditor`) to reflect the new 8-phase workflow: **Question -> Research -> Design -> Structure -> Plan -> Worktree -> Implement -> PR**.

## New Agent: `scout.md`
- **Role:** The Investigator / Researcher.
- **Responsibilities:**
  - Support Phase 1 (Question) with codebase queries to clarify objectives.
  - Execute Phase 2 (Research) by gathering pure facts, mapping architecture, and tracing dependencies.
  - Output: `plans/research/RESEARCH_REPORT.md` (Ground truth, no tasks).
- **Constraints:** Purely read-only. No planning, no tasks.

## Updated Agent: `architect.md`
- **Role:** The Strategic Planner.
- **Responsibilities:**
  - Phase 3: Create a short alignment doc (`01_DESIGN.md`).
  - Phase 4: Define vertical phases and create file skeletons/interfaces (`02_STRUCTURE.md`).
  - Phase 5: Create a detailed implementation plan (`03_IMPLEMENTATION_PLAN.md`).
- **Guidance:** Use "vertical phases" for early tests. Keep designs short and logical for SWEs.

## Updated Agent: `engineer.md`
- **Role:** The Expert Builder.
- **Responsibilities:**
  - Phase 7: Implement tasks from `03_IMPLEMENTATION_PLAN.md` using TDD (Red-Green-Refactor).
  - Update the plan file to track progress.
- **Guidance:** Strict adherence to the plan and design.

## Updated Agent: `auditor.md`
- **Role:** The Quality Gatekeeper.
- **Responsibilities:**
  - Phase 7: Verify implementation against `01_DESIGN.md`, `02_STRUCTURE.md`, and `03_IMPLEMENTATION_PLAN.md`.
  - Provide evidence-based verification.
- **Guidance:** Focus on correctness, tests, and alignment with the architecture.

## Implementation Steps

1.  **Create `agents/scout.md`**: Define the investigator persona and its focus on pure facts and ground truth.
2.  **Update `agents/architect.md`**: Redesign the prompt to produce the three distinct deliverables (Design, Structure, Plan) and emphasize vertical slices.
3.  **Update `agents/engineer.md`**: Refine the implementation loop to be tighter and more focused on the new plan structure.
4.  **Update `agents/auditor.md`**: Align verification with the multi-artifact outputs of the architect (Design, Structure, Plan).

## Verification & Testing
- Read all agent files to ensure they align with the 8-phase protocol in `system.md`.
- Verify that tool usage and constraints are consistent across the swarm.
- Ensure all agent names and roles make sense to a Senior Software Engineer.
