# ADR Protocol: Architecture Decision Records

To ensure long-term maintainability and clear design rationale, this project utilizes **Architecture Decision Records (ADRs)**.

## 1. ADR Location
*   **Standard Directory:** `docs/adr/`
*   **Naming Convention:** `NNNN-short-descriptive-name.md` (e.g., `0001-use-express-async-handler.md`).

## 2. ADR Lifecycle
*   **Consultation (Research Phase):** During the Research phase of any feature brew, the **Scout** MUST search for and read relevant ADRs in `docs/adr/` to understand existing architectural constraints and decisions.
*   **Informing Design (Design Phase):** The **Architect** MUST reference relevant ADRs in the `03_SPEC.md` document to ensure new designs are consistent with historical decisions.
*   **Creating New ADRs:** If a new feature introduces a significant architectural change or a new pattern, the **Architect** should propose a new ADR as part of the Implementation Plan (`04_PLAN.md`).

## 3. ADR Structure
Use the standard template found in `rules/adr_template.md`. Each ADR should include:
*   **Status:** Proposed, Accepted, Superceded, or Deprecated.
*   **Context:** What is the problem or requirement?
*   **Decision:** What is the proposed solution?
*   **Consequences:** What are the pros and cons of this decision?
