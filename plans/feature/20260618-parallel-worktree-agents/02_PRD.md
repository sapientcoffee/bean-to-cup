# ☕ Brew: Parallel Worktree Implementation (02_PRD.md)

## 1. Product Overview & User Persona
As a developer or automation orchestrator using the **Bean-to-Cup** CLI plugin repository, I want a robust, isolated, and self-healing multi-agent implementation environment using Git Worktrees and Isolate Branches. This ensures that parallel subagents can build, compile, test, and rollback their respective implementation slices concurrently without file collisions, shared state corruption, or destructive cross-agent modifications.

---

## 2. Requirements & Features

### 2.1 Workspace Isolation via Git Worktrees
*   **Local Worktree Mounts:** Provision and mount Git Worktrees inside a dedicated subfolder within the workspace: `.worktrees/task-<id>/`.
*   **Git Avoidance:** Programmatically append `.worktrees/` to the workspace `.gitignore` file to ensure nested files are never tracked or scanned by the parent repository.
*   **Bootstrapping:** The lifecycle manager must run a lightweight dependency restore (`dotnet restore` or `npm install --prefer-offline`) inside the worktree immediately after mounting to ensure the subagent starts with a fully compilable project.

### 2.2 Branch Lifecycle Management
*   **Deterministic Naming:** Isolate branches must be named `task/slice-<id>-<short-slug>`.
*   **Local Merging & Pruning:** Upon a successful subagent execution (all verification tests pass):
    1. Commit changes within the worktree.
    2. Merge the isolate branch back into the main development branch.
    3. Prune and delete the worktree (`git worktree remove --force <path>`).
    4. Delete the isolate branch.
*   **Rollback & Fail-Safe:** If a subagent fails or exceeds its retry limits, its worktree is pruned and its branch is preserved or marked as failed for manual inspection, leaving the main workspace entirely clean and unaffected.

### 2.3 Concurrency & Merge Conflict Mitigation
*   **Serialize Shared Files:** Slices that modify shared infrastructure (e.g., migrations, main route registrations) must be marked as `[Serial]` in the execution plan and run sequentially.
*   **Parallel Execution Slices:** Slices implementing purely isolated, independent domain aggregate logic (separate classes and tests) must run in parallel.
*   **Serial Merge Queue:** Concurrent merges must enter a lock-protected queue to avoid race conditions. If a trivial merge conflict arises (e.g., package listings in `.csproj`), the orchestrator should trigger a targeted resolution handler.

### 2.4 Recovery & Orphaned Worktree Cleanup
*   **Proactive Reconciliation:** On startup or plugin registration, scan `.worktrees/` for any directories whose parent process is no longer active. Automatically run `git worktree prune` and delete these dangling directories.
*   **Manual Override:** Provide a manual synchronizing command (e.g., via `/brew:sync` or `/loop:cancel`) to sweep, force-prune, and clean up any active worktree sessions.

---

## 3. Non-Goals
*   Managing remote GitHub repositories or triggering remote branch pushes (handled strictly in Stage 9 of the SDLC).
*   Supporting non-Git workspace environments.
*   Providing user interface configurations for git operations (strictly CLI and API-driven execution).

---

## 4. Acceptance Criteria
1.  Multiple subagents can run implementation loops concurrently with absolute file isolation.
2.  All worktrees are created within `.worktrees/` and are fully ignored by the parent Git repository.
3.  Successful subagent tasks are committed, merged, and their worktrees are cleanly pruned.
4.  Aborted or failed tasks preserve their branch state for inspection but cleanly remove their physical worktree.
5.  Orphaned worktrees left behind by interrupted sessions are automatically reconciled and swept on next startup.
