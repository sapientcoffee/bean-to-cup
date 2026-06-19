# ☕ Brew: Decision Traceability & Auto-Sync (02_PRD.md)

## 1. Product Overview & User Persona
As an orchestrator or autonomous coordinator in the **Bean-to-Cup** swarm, I want a robust local-to-remote issue synchronization engine (`brew:sync`) so that I can automatically parse execution plans, provision idempotent sub-task issues, establish complete parent-child issue traceability on GitHub, and comment on the main Epic to notify human maintainers for approval (Phase 6 Human Gate).

---

## 2. Requirements & Features

### 2.1 Native Plan Parsing
*   **Regex-Based Scanner:** Must read `05_PLAN.md` line-by-line using standard regex to extract:
    *   Step labels (e.g., `Step 1.A`) and task names.
    *   Step status (`[ ]` or `[x]`).
    *   Metadata headers under each step section (`*Target File:*`, `*Verification:*`, `*Depends On:*`).
    *   Descriptions/custom instructions inside the step's block.
*   **DAG Construction:** Construct a Directed Acyclic Graph (DAG) based on the `*Depends On:*` field to represent implementation dependencies.

### 2.2 Idempotent GitHub Provisioning (`brew:sync`)
*   **Duplicate Prevention:** Query `gh issue list` to match existing titles before creating any new task issues.
*   **Structured Issue Bodies:** Provision issues using a consistent markdown template:
    *   Include a reference back to the parent Epic Issue number.
    *   Detail the target file path and verification criteria.
    *   List any prerequisite tasks (`*Depends On:*`).
    *   Set the standard label `ready-for-dev`.
*   **Epic Linkage:** Automatically extract the main Epic Issue ID to prefix titles and bodies appropriately.

### 2.3 Phase 6 Human Gate Handshake
*   **Approval Prompting:** Once tasks are parsed and synced, post a comment on the Epic issue via `gh issue comment <Epic_ID>` prompting the maintainer to review the local plan and add the `approved` label or click "Proceed" to continue execution.

---

## 3. Non-Goals
*   A full-blown web dashboard for managing issues (we rely on GitHub UI and the local interactive Kanban board).
*   Automatic merging of code or PR creation (handled by other phases of the protocol).

---

## 4. Acceptance Criteria
1.  Running `agy brew:sync` successfully parses `05_PLAN.md` and generates a logical model of tasks and dependencies.
2.  If any task issue already exists on GitHub, `agy brew:sync` skips creating it (idempotency).
3.  Each newly created task contains complete metadata (Target File, Verification, and Depends On) in its body, labeled as `ready-for-dev`.
4.  The script posts a beautifully formatted coordination comment on the parent Epic, initiating the Phase 6 human gate.
