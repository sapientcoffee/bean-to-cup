# ADR 0000: Use Architecture Decision Records (ADRs)

*   Status: Accepted
*   Date: 2026-04-24
*   Deciders: Gemini CLI, User

## Context and Problem Statement
As the project grows, architectural decisions are often made implicitly or lost in commit messages. We need a way to capture the "why" behind significant design choices to inform future development and prevent regressions in architectural intent.

## Decision Drivers
*   Long-term maintainability.
*   Onboarding new agents and developers.
*   Consistency in design patterns.

## Considered Options
1.  No formal record (status quo).
2.  Architecture Decision Records (ADRs) in `docs/adr/`.
3.  Design documents in `plans/` only.

## Decision Outcome
Chosen option: **ADRs in `docs/adr/`**, because it provides a centralized, version-controlled repository of historical decisions that persists beyond individual feature implementation cycles.

### Positive Consequences
*   Clear historical context for future design phases.
*   Reduced ambiguity when choosing between patterns.
*   Better alignment between different agents in the swarm.

### Negative Consequences
*   Slightly more overhead when making significant changes.

## Links
*   `rules/adr.md`
*   `rules/adr_template.md`
