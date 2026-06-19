---
date: 2026-06-18T22:12:00-07:00
researcher: Antigravity
git_commit: 18d4bba7f937141157db18017c6c72371163170a
branch: main
repository: bean-to-cup
topic: "Implementing robust AI workspace isolation via git worktrees and branches during the TDD implementation phase"
tags: [research, codebase, git-worktree, parallel-agents, implementation-engine]
status: complete
last_updated: 2026-06-18
last_updated_by: Antigravity
---

# 03 Extraction Report: Parallel Worktree Implementation

**Date**: 2026-06-18 22:12:00-07:00
**Researcher**: Antigravity
**Git Commit**: 18d4bba7f937141157db18017c6c72371163170a
**Branch**: main
**Repository**: bean-to-cup

## Research Question
"at implementation stage ensure that git worktrees and branches are used to ptovide a robust AI implmentation mechism to support parrlelel work/agents"

## Summary
Currently, the **Bean-to-Cup** swarm defines an `Implementation Engine` in [commands/ddd:implement.toml](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:implement.toml) that dictates "Isolated & Parallel Subagent Implementation". However, the implementation engine runs all parallel subagents in the *same physical workspace directory* and uses a destructive `git restore .` for rolling back individual failures. 

This research maps out the current state of implementation commands, git branch management scripts, and identifies the exact entry points needed to build a robust Git Worktree and branch-based isolation layer.

## Detailed Findings

### 1. The Implementation Command Structure
- **Current File:** [commands/ddd:implement.toml](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:implement.toml)
- **Behavior:** It defines the `ddd:implement` command with directives for spawning isolated subagents for each task/slice and running independent tasks concurrently in parallel.
- **Vulnerability / Clashing Risk:** Under `RETRY/ROLLBACK POLICY` (lines 37-41), if tests fail, a subagent is instructed to execute `git restore .` to revert the workspace. If multiple subagents run concurrently in the same directory, one subagent's rollback will completely destroy another subagent's uncommitted work.

### 2. Standard Branching and GitHub Workflows
- **Current File:** [skills/github-workflow/SKILL.md](file:///home/robedwards/workspace/bean-to-cup/skills/github-workflow/SKILL.md)
- **Behavior:** This file establishes standard local and remote branch workflows. It mentions running `git status`, verifying the current branch, and using `git checkout -b <branch>` for creating feature branches.
- **Integration Potential:** We can leverage these conventions to define how the Worktree Lifecycle Manager names branches (`task/slice-<id>-<slug>`) and creates/deletes them.

### 3. Startup and Sync Hooks
- **Current Files:**
  - [commands/startcycle.toml](file:///home/robedwards/workspace/bean-to-cup/commands/startcycle.toml) - Executes sequential pipeline steps (`write-specs` -> `generate-code` -> `audit-code` -> `deploy-app`).
  - [docs/swarm-registry.md](file:///home/robedwards/workspace/bean-to-cup/docs/swarm-registry.md) - Registers all commands, scripts, skills, and hooks (including automated session hooks like `git-status.sh` and `coffee-and-git.sh`).
- **Integration Potential:** The startup or reconciliation hook can be registered as a session startup hook or bound to command sequences to clean up orphaned `.worktrees/` directories.

## Code References
- [commands/ddd:implement.toml#L26-L30](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:implement.toml#L26-L30) - Directive requiring isolated, parallel subagent spawns.
- [commands/ddd:implement.toml#L37-L41](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:implement.toml#L37-L41) - Destructive `git restore .` rollback policy causing collisions.
- [skills/github-workflow/SKILL.md#L19-L22](file:///home/robedwards/workspace/bean-to-cup/skills/github-workflow/SKILL.md#L19-L22) - Standard branch checkout pattern `git checkout -b`.

## Architecture Documentation
Currently, the system is designed with a **Head Barista / Orchestrator** pattern that drives the 9-stage SDLC. In Stage 7, parallel subagents (e.g., `@engineer` or `@auditor`) are dispatched. There is no concept of multiple concurrent working trees or local directories in the current setup; everything executes directly inside the root workspace `/home/robedwards/workspace/bean-to-cup/` or `app_build/`.

## Historical Context (ADRs & Thoughts)
Review of existing documentation confirms that no Architecture Decision Record (ADR) or planning document currently exists for Git Worktree orchestration. This feature represents a brand new architectural layer in the Bean-to-Cup platform.

## Open Questions
- What physical utility should implement the **Worktree Lifecycle Manager**? A dedicated Bash script, or a specialized subagent command? (We will resolve this in Stage 4: Specification).
