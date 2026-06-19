# ☕ Brew: Parallel Worktree Implementation (01_GLOSSARY.md)

This glossary establishes the Ubiquitous Language for the **Parallel Worktree Implementation** feature. It ensures absolute alignment when discussing parallelized agent executions, workspace isolation, and state synchronization across multiple concurrent tasks.

---

## 1. Domain Terms

**Git Worktree**:
A linked checkout of a git repository. It allows multiple branches to be checked out simultaneously in different physical directories while sharing the same underlying `.git` database.
*Avoid*: virtual clone, repo copy, duplicate repository

**Isolate Branch**:
A dedicated, short-lived Git branch (e.g., `task/slice-4-auth`) created specifically for an individual implementation slice.
*Avoid*: dev branch, subagent branch, branch copy

**Worktree Path / Mount Point**:
A subdirectory within the workspace (e.g., `.worktrees/task-<id>`) where a specific Git Worktree is checked out. It must be explicitly gitignored in the main repository to prevent recursion.
*Avoid*: temp folder, build path, worktree dir

**Worktree Lifecycle Manager**:
The automated manager responsible for creating the isolate branch, checking out the Git Worktree, passing control to the implementation subagent, and pruning/cleaning up the worktree upon task completion or rollback.
*Avoid*: branch manager, git cleaner

**Isolated Swarm Execution**:
The parallel execution of multiple subagents, each assigned to a separate Worktree Path, allowing simultaneous compilation, testing (TDD), and filesystems edits without collision.
*Avoid*: multithreaded agents, concurrent run
