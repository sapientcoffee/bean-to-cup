# ☕ Walkthrough & Testing Evidence: Bean-to-Cup Plugin

This walkthrough provides empirical evidence of the thorough testing and native integration of the **Bean-to-Cup** Autonomous Barista Swarm plugin inside the Antigravity CLI (`agy`).

---

## 🔍 Empirical Test Results

To verify the integration, we simulated interactive CLI sessions using `tmux` capture panes to inspect the exact state and behavior of the CLI.

### 1. Active Subagents Thread Monitor (`/agents`)
The `/agents` interactive menu is designed as an **Active Subagent Session Manager** to monitor, toggle, or kill running background subagent tasks.
*   **Startup State**: At launch, because no background subagents are spawned, the menu displays only the main default session:
    ```text
    > ▾ Available Agents
         ● /default  Default agent
    ```

### 2. Live Agent Persona Swapping (`@engineer`)
Typing `@<agent_name>` in the interactive prompt swaps the agent's persona inline inside the main context. The following capture shows the `@engineer` subagent parsing the workspace rules and agents structure in real-time:

```text
────────────────────────────────────────────────────────────
> @engineer Hello! Please analyze the project and list files.

● ListDir(/home/robedwards/workspace/bean-to-cup/rules) (ctrl+o to expand)

▸ Thought for 2s, 366 tokens
  Exploring Rule Files

● ListDir(/home/robedwards/workspace/bean-to-cup/agents) (ctrl+o to expand)
```

### 3. Parallel Implementation & Subagent Swarm Execution
The system design and code implementation engines have been upgraded to support high-performance parallelism and isolated subagent execution:
*   **Dependency-Aware Planning**: During the planning stage (Stage 5 / `05_PLAN.md`), the `@architect` analyzes task relationships and partitions slices into concurrent execution groups (e.g., pure domain aggregates or independent endpoints).
*   **Isolated Subagents**: Each slice/task is assigned a dedicated, separate `@engineer` subagent. This guarantees clean context separation and avoids logical contamination or conflicting changes.
*   **Concurrent Execution**: Slices with no mutual dependencies are executed concurrently in parallel, while serial bottlenecks wait sequentially.

---

## 🏗️ Swarm Architecture & Files

The plugin registers **13 specialized personas** in the workspace:

| Persona | Handle | Purpose | Definition File |
| :--- | :--- | :--- | :--- |
| **System Design** | `@architect` | Conceptual specs (`03_SPEC.md`) and task checklist planning (`04_PLAN.md`). | [system-design.md](file:///home/robedwards/workspace/bean-to-cup/agents/system-design.md) |
| **Code Implementation** | `@engineer` | Production code construction via Red-Green-Refactor TDD. | [code-implementation.md](file:///home/robedwards/workspace/bean-to-cup/agents/code-implementation.md) |
| **Quality Verification** | `@auditor` | Security, SLI/SLO compliance, and final QA verification report. | [quality-verification.md](file:///home/robedwards/workspace/bean-to-cup/agents/quality-verification.md) |
| **Context Discovery** | `@scout` | Context-free "Blind Research" of the codebase. | [context-discovery.md](file:///home/robedwards/workspace/bean-to-cup/agents/context-discovery.md) |

---

## 🚀 Native Command Registration (Subcommand Resolution)

In our initial design, the custom commands were organized into nested subdirectories (e.g., `commands/brew/init.toml`, `commands/ddd/plan.toml`), which is not supported natively by `agy` and resulted in ignored commands. 

To solve this natively in `agy`:
1.  **Flattened Directory Structure**: All command `.toml` files were relocated directly to the root `commands/` directory.
2.  **Namespace Mapping (Colon Notation)**: We renamed the files using a colon (`:`) notation (e.g., `commands/brew:init.toml`, `commands/loop:start.toml`, `commands/ddd:plan.toml`). Linux and the Antigravity parser natively support colons in filenames.
3.  **Clean Validation**: Running `agy plugin validate .` now successfully registers and compiles all **22 commands** and **14 skills** with 100% schema compliance:
    ```text
    ✔ skills      : 14 processed
    ✔ agents      : 13 processed
    ✔ commands    : 22 processed (converted to skills)
    ✔ hooks       : 1 processed
    ```

You can now type flat namespace commands directly (such as `/brew:init`, `/loop:start`, `/ddd:plan`, etc.), and `agy` will parse and map them to their corresponding agent prompts seamlessly.

### 4. Conversion of `feature.toml` to a Reusable Skill
The `/feature` command initialization logic has been refactored into a reusable skill (`skills/feature/SKILL.md`). This modularizes the Discovery & Validation protocol, allowing any agent inside the swarm to load and reference the Phase 1 PRD generation requirements contextually. The `commands/feature.toml` command has been simplified to a clean delegation wrapper that points to the new skill.

### 5. Unified Skill-Path Installation & Native Registration

We refactored the installation/uninstallation pipelines to utilize the standard simple skill folders for maximum compatibility and discoverability:
*   **Global Scope**: `~/.gemini/skills/`
*   **Workspace Scope**: `<project-root>/.agents/skills/`

#### Copy-by-Default (Standard Install)
Running `./install.sh --global --force` copies all plugin code files (excluding development folders like `.git` or `scratch`) into the destination folder, and then executes native registration with the `agy` CLI pointing to the copied files:

```text
Copying local plugin 'bean-to-cup' to /home/robedwards/.gemini/skills/bean-to-cup...
Registering plugin natively with Antigravity CLI...
  [ok]    bean-to-cup
          ✔ skills      : 8 processed
          ✔ agents      : 13 processed
          ✔ commands    : 19 processed (converted to skills)
          - mcpServers  : skipped (not found)
          ✔ hooks       : 1 processed
Plugin registered successfully in agy!
```

#### Local Development Symlinking
If you prefer a symlink for live edits during development, pass the `--link` (or `-l`) option:

```text
Linking local plugin 'bean-to-cup' to /home/robedwards/workspace/bean-to-cup/.agents/skills/bean-to-cup...
Registering plugin natively with Antigravity CLI...
  [ok]    bean-to-cup
          ✔ skills      : 8 processed
          ...
```

#### Native Uninstallation Clean-Up
Running `./uninstall.sh --global` completely cleans up the target directory and natively unregisters the plugin:

```text
Removing plugin directory or symlink at /home/robedwards/.gemini/skills/bean-to-cup...
Successfully removed plugin files from disk.
Unregistering plugin natively from Antigravity CLI...
Uninstalled plugin "bean-to-cup"
Plugin unregistered successfully in agy!
```




## 🚀 Phase 2 Migration: Legacy Commands to Skills (June 2026)

In June 2026, we completed the full migration of the remaining 10 legacy custom commands into native, self-contained Markdown Skills under Antigravity 2.0. This eliminates the double-indirection TOML wrappers and resolves registry loading overhead.

### 1. Verification of Clean Schema Compilation
Running `agy plugin validate .` now registers the entire workspace with exactly 0 active legacy commands and 20 native, self-contained skills:

```text
  [ok]    .
  ✔ skills      : 20 processed
  ✔ agents      : 8 processed
  - commands    : skipped (not found)
  - mcpServers  : skipped (not found)
  ✔ hooks       : 1 processed
```

### 2. Consolidated Skills List
All 9 remaining active commands have been successfully refactored into the following self-contained folders inside `skills/`:
*   `/feature` -> `skills/feature/SKILL.md` (Consolidated)
*   `/research` -> `skills/research/SKILL.md` (Consolidated)
*   `/brew:record` -> `skills/brew-record/SKILL.md` (Renamed & Consolidated recording parameters)
*   `/brew:archive` -> `skills/brew-archive/SKILL.md` (New native skill)
*   `/brew:sync` -> `skills/brew-sync/SKILL.md` (New native skill)
*   `/brew:worktree` -> `skills/brew-worktree/SKILL.md` (New native skill)
*   `/dev` -> `skills/dev/SKILL.md` (New native skill)
*   `/build:production` -> `skills/build-production/SKILL.md` (New native skill)
*   `/test:api` -> `skills/test-api/SKILL.md` (New native skill)

The obsolete bootstrapper `brew:init` has been successfully moved to `holding-pen/commands/brew:init.toml` to clean up the workspace. All changes are committed and validated.
