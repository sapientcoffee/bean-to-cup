# ☕ Brew: Decision Traceability & Auto-Sync (01_GLOSSARY.md)

This glossary establishes the Ubiquitous Language for the **Decision Traceability & Auto-Sync** feature. It ensures absolute semantic alignment across the swarm coordinator, the subagents, and human developers when managing, parsing, and syncing local project states with remote tracking services.

---

## 1. Domain Terms

**Plan Parser (Plan Compiler)**:
The parsing engine that reads the local markdown `05_PLAN.md` file of an active feature and compiles it into a structured, machine-readable JSON array of tasks (extracting step names, labels, target files, verification commands, and descriptions).
*Avoid*: markdown reader, checklist grabber, line reader

**Issue Synchronization Engine (`brew:sync`)**:
The CLI command and underlying logic responsible for comparing the parsed local task list against existing remote GitHub issues, creating missing task issues with descriptive bodies, and linking them to the parent Epic issue.
*Avoid*: issue publisher, github pusher, remote updater

**Idempotency Check**:
The verification step that queries the remote GitHub issue tracker (using `gh issue list`) before creating any task issue to prevent duplicate entries for the same step.
*Avoid*: existence scan, duplicate filter

**Topological Sort Solver**:
The algorithm that processes each task's `*Depends On:*` metadata string to produce a deadlock-free, validated DAG (Directed Acyclic Graph) of execution groups, separating parallelizable runs from sequential bottlenecks.
*Avoid*: scheduler, ordering loop

**Stitched PR Template Compiler**:
The generator that constructs a comprehensive `PR_BODY.md` description by dynamically stitching together the high-level PRD goals, the completed local task checklist, repository-relative walkthrough assets, and the collapsed `07_VERIFICATION.md` logs.
*Avoid*: pr writer, description template
