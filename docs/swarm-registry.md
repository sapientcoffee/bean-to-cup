# ☕ Bean-to-Cup: Swarm & Command Registry

This document serves as the definitive reference manual and registry for all agents, skills, custom commands, and automated hooks within the **Bean-to-Cup** Autonomous Barista Swarm under the **Antigravity CLI (`agy`)**.

> [!NOTE]
> All commands, skills, and agents listed below comply with the `agy 2.0` schema. They operate strictly within the renumbered Stage 0 to Stage 9 SDLC protocol.

---

## ⌨️ 1. Custom Commands

Commands are registered as flat `.toml` files matching the namespace standard in `commands/`. Nested command subdirectories are avoided to ensure seamless discovery by the `agy` compiler.

| Command | SDLC Stage | Description & Behavior | Status |
| :--- | :--- | :--- | :--- |
| **`/feature`** | **Stage 2** | Initiates feature development (Stages 1-2), prompting Socratic alignment and PRD generation. | **Active** |
| **`/research`** | **Stage 3** | Spawns parallel investigative agents to map codebase components and patterns (`03_EXTRACTION.md`). | **Active** |
| **`/rewrite`** | **Stage 1 & 2** | Orchestrates legacy application rewrite workflows by analyzing modernization assessments. | **Active** |
| **`/assess`** | **Stage 1 & 2** | Executes context-aware application modernization assessment via CodMod CLI & GCP checks. | **Active** |
| **`/record`** | **Stage 8** | Records terminal interactions using asciinema and compiles them to animated `.gif` walkthroughs. | **Active** |
| **`/sync`** | **Stage 5** | Parses the vertical execution plan (`05_PLAN.md`) and synchronizes tasks to GitHub issues. | **Active** |
| **`/worktree`** | **Stage 7 & 9** | Manages Git Worktrees and isolates feature branches during development. | **Active** |
| **`/push`** | **Stage 9** | Delivers code changes to GitHub following conventional commits, linting, and rich PR descriptions. | **Active** |
| **`/dev`** | **Stage 7 / Utility** | General-purpose developer environment runner (backend & frontend). | **Active** |
| **`/archive`** | **Maintenance** | Clears completed, spent feature grounds (`plans/`) to `plans/archive/` and updates `.geminiignore`. | **Active** |
| **`/test:api`** | **Stage 7** | Triggers suite-level automated endpoint testing and compliance checks. | **Active** |
| **`/build:production`** | **Stage 7 & 9** | Runs compilation, packaging, and builds production release artifacts. | **Active** |

---

## 🤖 2. Active Specialized Subagents (9 Active Swarm)

Specialized subagents reside in `agents/` and are dispatched with targeted system prompts. They are invoked using `@<alias>` in developer prompts or by parent skills.

| Agent Alias | Config File | Assigned Role | Target SDLC Stage | Inputs Required | Primary Outputs | Data Pulled In | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`@architect`** | **[`system-design.md`](file:///home/robedwards/workspace/bean-to-cup/agents/system-design.md)** | Strategic Planner | **Stage 4 & 5** | `02_PRD.md`, `03_EXTRACTION.md`, `design.md` | `04_SPEC.md`, `05_PLAN.md`, `visual-dashboard.html` (Spec & Overview Tabs) | Design guidelines, telemetry specs, physical API contracts | **Active** |
| **`@red-team-reviewer`** | **[`red-team-reviewer.md`](file:///home/robedwards/workspace/bean-to-cup/agents/red-team-reviewer.md)** | Adversarial Critic | **Stage 2, 4, 5** | `02_PRD.md`, `04_SPEC.md`, `05_PLAN.md` proposals | `0X_RED_TEAM_AUDIT.md`, edge case critique | Security checklists, unhandled failure scenarios | **Active** |
| **`@engineer`** | **[`code-implementation.md`](file:///home/robedwards/workspace/bean-to-cup/agents/code-implementation.md)** | Code Builder | **Stage 7** | `04_SPEC.md`, `05_PLAN.md` slice | Source code, unit tests, passing test suites | Existing codebase patterns, lint rules, package manifests | **Active** |
| **`@auditor`** | **[`quality-verification.md`](file:///home/robedwards/workspace/bean-to-cup/agents/quality-verification.md)** | Quality Gatekeeper | **Stage 7** | `04_SPEC.md`, `05_PLAN.md`, implementation diffs | `07_VERIFICATION.md`, audit logs, regression reports | Test execution outputs, build logs, API contract definitions | **Active** |
| **`@scout`** | **[`context-discovery.md`](file:///home/robedwards/workspace/bean-to-cup/agents/context-discovery.md)** | Investigative Researcher | **Stage 3** | User query or research scope | Factual file listings, symbol definitions, import graphs | Codebase file system, AST maps, module declarations | **Active** |
| **`@codebase-analyzer`** | **[`codebase-analysis.md`](file:///home/robedwards/workspace/bean-to-cup/agents/codebase-analysis.md)** | Technical Cartographer | **Stage 3** | Target component path or function name | Component analysis with exact `file:line` references | Raw source code lines, function signatures, data flow paths | **Active** |
| **`@context-mapping`** | **[`context-mapping.md`](file:///home/robedwards/workspace/bean-to-cup/agents/context-mapping.md)** | Codebase Navigator | **Stage 3** | High-level feature concept | Entry point inventory, file boundary map | Project folder hierarchy, routing tables, configuration files | **Active** |
| **`@pattern-recognition`** | **[`pattern-recognition.md`](file:///home/robedwards/workspace/bean-to-cup/agents/pattern-recognition.md)** | Architecture Librarian | **Stage 3** | Architectural pattern request | Pattern reference examples, conventions guide | Codebase utilities, middleware chains, factory/repository instances | **Active** |
| **`@code-review`** | **[`code-inspection.md`](file:///home/robedwards/workspace/bean-to-cup/agents/code-inspection.md)** | Architectural Critic | **Stage 7** | Git diff / modified files | Code inspection report, smell analysis, polish recommendations | Staged diffs, coding standards, complexity metrics | **Active** |


### 📦 Archived / Holding-Pen Agents (5 Total)
The following subagents are safely moved to `holding-pen/agents/` to maintain workspace cleanliness and focus:
*   `@security-auditor` (`holding-pen/agents/security-plan.md`) - Sentry security audit.
*   `@security-remediator` (`holding-pen/agents/security-remediation.md`) - Vulnerability patching.
*   `@vulnerability-scanner` (`holding-pen/agents/vulnerability-scan.md`) - Static dependency scanner.
*   `@msbuild` (`holding-pen/agents/msbuild.md`) - MSBuild compilation engine.
*   `@pipeline-stages` (`holding-pen/agents/pipeline-stages.md`) - Legacy CI/CD release engineer.

---

## 🛠️ 3. Modular Skills (25 Total)

Skills are modular instruction bundles in `skills/` activated dynamically by agents or slash commands.

| Skill Name | Target Stage | Description & Responsibility | Primary Inputs | Primary Outputs | Data Pulled In | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[`ideator`](file:///home/robedwards/workspace/bean-to-cup/skills/ideator/SKILL.md)** | **Stage 0** | Product discovery & idea drafting. | Raw user prompt / idea | `00_IDEATION.md`, `visual-dashboard.html` (Discovery Tab) | Personas, friction points, mock schemas | **Active** |
| **[`grill`](file:///home/robedwards/workspace/bean-to-cup/skills/grill/SKILL.md)** | **Stage 1** | Socratic alignment interview, updating glossary, ADRs, and dashboard. | `00_IDEATION.md` or user prompt | `docs/glossary.md`, `docs/adr/`, `visual-dashboard.html` (Glossary & ADR Tabs) | Codebase facts, Well-Architected Framework guidelines | **Active** |
| **[`grilling`](file:///home/robedwards/workspace/bean-to-cup/skills/grilling/SKILL.md)** | **Stage 1** | **[DEPRECATED]** Legacy interview prompt. Replaced by `grill`. | User prompt | Interactive interview | Codebase queries | **Deprecated** |
| **[`domain-modeling`](file:///home/robedwards/workspace/bean-to-cup/skills/domain-modeling/SKILL.md)** | **Stage 1, 4, 5** | Maintains global ubiquitous glossary (`docs/glossary.md`) and ADRs (`docs/adr/`). | Domain concepts, decisions | `docs/glossary.md`, `docs/adr/`, `visual-dashboard.html` | Domain terminology, architectural trade-offs | **Active** |
| **[`feature`](file:///home/robedwards/workspace/bean-to-cup/skills/feature/SKILL.md)** | **Stage 2** | Bootstraps feature directory and initializes Socratic discovery. | Feature prompt | `plans/<slug>/<timestamp>/` folder | Active workspace status, existing plans | **Active** |
| **[`write-prd`](file:///home/robedwards/workspace/bean-to-cup/skills/write-prd/SKILL.md)** | **Stage 2** | Formulates product PRD with non-goals, KPIs, and user stories. | `docs/glossary.md`, Socratic interview | `02_PRD.md`, `visual-dashboard.html` (PRD Tab) | Persona friction, business constraints | **Active** |
| **[`rewrite`](file:///home/robedwards/workspace/bean-to-cup/skills/rewrite/SKILL.md)** | **Stage 1 & 2** | Orchestrates legacy application modernization workflows. | Modernization assessment report | Modernization roadmap across Stages 0-5 | Legacy schemas, migration metrics | **Active** |
| **[`research`](file:///home/robedwards/workspace/bean-to-cup/skills/research/SKILL.md)** | **Stage 3** | Coordinates parallel codebase extraction (Blind Research). | `02_PRD.md` or research query | `03_EXTRACTION.md`, `visual-dashboard.html` (Extraction Tab) | File paths, ASTs, import graphs, grep results | **Active** |
| **[`assess`](file:///home/robedwards/workspace/bean-to-cup/skills/assess/SKILL.md)** | **Stage 1 & 2** | Application modernization assessment via CodMod CLI & GCP check. | Workspace path, GCP credentials | Assessment report, cost estimation | Codebase AST, dependency trees, cloud config | **Active** |
| **[`audit-code`](file:///home/robedwards/workspace/bean-to-cup/skills/audit-code/SKILL.md)** | **Stage 7** | QA Engineer assessing code alignment with spec, fixing bugs in `app_build/`. | `04_SPEC.md`, `05_PLAN.md`, `app_build/` | Verified code, bug fix commits, test logs | Spec contracts, test outputs, build logs | **Active** |
| **[`generate-code`](file:///home/robedwards/workspace/bean-to-cup/skills/generate-code/SKILL.md)** | **Stage 7** | Full-stack code generation from tech spec. | `04_SPEC.md`, `05_PLAN.md` | Source code, unit tests | Spec interfaces, existing codebase patterns | **Active** |
| **[`kanban`](file:///home/robedwards/workspace/bean-to-cup/skills/kanban/SKILL.md)** | **Stage 5 & 7** | Interactive Kanban board and Mermaid progress flow generator. | `05_PLAN.md` task states | `visual-dashboard.html` (Overview Tab Kanban), `05_PLAN.md` | Task status markers (`[ ]`, `[/]`, `[x]`) | **Active** |
| **[`chaos-mitigation`](file:///home/robedwards/workspace/bean-to-cup/skills/chaos-mitigation/SKILL.md)** | **Stage 7 & Day 2** | Chaos event detection & mitigation in `press-service`. | Service logs, health endpoints | Incident resolution, runbook logs | `press-service` stdout/stderr, metric telemetry | **Active** |
| **[`deploy-app`](file:///home/robedwards/workspace/bean-to-cup/skills/deploy-app/SKILL.md)** | **Stage 7** | Stack detection & local dev server hosting. | Source directory | Running local server process, access URL | Dependency manifests (`package.json`, etc.) | **Active** |
| **[`dev`](file:///home/robedwards/workspace/bean-to-cup/skills/dev/SKILL.md)** | **Stage 7 / Utility** | Starts local backend & frontend development servers. | Dev configs | Background server process | Port availability, dev scripts | **Active** |
| **[`build-production`](file:///home/robedwards/workspace/bean-to-cup/skills/build-production/SKILL.md)** | **Stage 7 & 9** | Builds application for production release. | Workspace source, build scripts | Release binary / bundle | Build tools, package manifests | **Active** |
| **[`record`](file:///home/robedwards/workspace/bean-to-cup/skills/record/SKILL.md)** | **Stage 8** | Terminal asciinema interaction recorder. | Scenario script or interactive session | `.cast`, `.gif`, embedded in `08_WALKTHROUGH.md` | Terminal stdout/stderr streams | **Active** |
| **[`test-api`](file:///home/robedwards/workspace/bean-to-cup/skills/test-api/SKILL.md)** | **Stage 7** | Executes local backend API validation scripts. | Dev server URL, endpoint definitions | API test report | HTTP status codes, JSON response bodies | **Active** |
| **[`visual-dashboard`](file:///home/robedwards/workspace/bean-to-cup/skills/visual-dashboard/SKILL.md)** | **Universal (0-8)** | Manages, updates, and mirrors `visual-dashboard.html` across all stages. | Plan directory path, stage moniker | `visual-dashboard.html` in workspace & system artifacts | Stage markdown files (`00_IDEATION.md` through `08_WALKTHROUGH.md`) | **Active** |
| **[`worktree`](file:///home/robedwards/workspace/bean-to-cup/skills/worktree/SKILL.md)** | **Stage 7 & 9** | Manages Git Worktrees for isolated subagent execution. | Branch name, base branch | Git worktree folder (`.worktrees/<branch>`) | Git commit history, branch list | **Active** |
| **[`sync`](file:///home/robedwards/workspace/bean-to-cup/skills/sync/SKILL.md)** | **Stage 5** | Synchronizes vertical execution plan tasks to GitHub issues. | `05_PLAN.md` | GitHub Issues created/updated | `05_PLAN.md` checklist, `gh` CLI issue list | **Active** |
| **[`github-workflow`](file:///home/robedwards/workspace/bean-to-cup/skills/github-workflow/SKILL.md)** | **Stage 9** | Git branch, commit, and PR management via `gh` CLI. | Staged files, PR description | Active Pull Request on GitHub | `gh` authentication status, git branch state | **Active** |
| **[`git-delivery`](file:///home/robedwards/workspace/bean-to-cup/skills/git-delivery/SKILL.md)** | **Stage 9** | Emoji-powered delivery pipeline with atomic commits and rich PRs. | Staged changes, `08_WALKTHROUGH.md` | Atomic commits, Pull Request | Git diffs, commit history, walkthrough proof | **Active** |
| **[`archive`](file:///home/robedwards/workspace/bean-to-cup/skills/archive/SKILL.md)** | **Maintenance** | Archives completed plans to `plans/archive/` and updates `.geminiignore`. | `plans/` directory | `plans/archive/`, `.geminiignore` | Directory completion status | **Active** |
| **[`motivate`](file:///home/robedwards/workspace/bean-to-cup/skills/motivate/SKILL.md)** | **Utility** | Provides encouraging coffee-themed messages and puns. | User request | Friendly chat response | Coffee trivia & puns | **Active** |

---

## 🔗 4. Skill Nesting & Subagent Composition Topology

This composition map explicitly documents how parent skills nest child skills and dispatch specialized subagents across the SDLC pipeline:

```
1. /feature (Command)
   └── feature (Skill)
       ├── Nests: ideator (Skill) [Optional Stage 0 Discovery]
       ├── Nests: grill (Skill) [Stage 1 Socratic Alignment]
       │   ├── Nests: domain-modeling (Skill) [Updates docs/glossary.md & docs/adr/]
       │   └── Nests: visual-dashboard (Skill) [Syncs Glossary Tab]
       └── Nests: write-prd (Skill) [Stage 2 PRD Generation]
           └── Nests: visual-dashboard (Skill) [Syncs PRD Tab]

2. /research (Command)
   └── research (Skill)
       ├── Dispatches Subagent: @scout (context-discovery.md)
       ├── Dispatches Subagent: @context-mapping (context-mapping.md)
       ├── Dispatches Subagent: @codebase-analyzer (codebase-analysis.md)
       ├── Dispatches Subagent: @pattern-recognition (pattern-recognition.md)
       └── Nests: visual-dashboard (Skill) [Syncs Extraction Tab]

3. Stages 4 & 5 (Specification & Execution Planning)
   └── Head Barista Orchestrator
       ├── Dispatches Subagent: @architect (system-design.md)
       ├── Nests: kanban (Skill) [Generates Interactive Kanban]
       └── Nests: visual-dashboard (Skill) [Syncs Spec & Overview Tabs]

4. Stage 7 (TDD Implementation Loop)
   └── Head Barista Orchestrator
       ├── Dispatches Subagent: @engineer (code-implementation.md)
       ├── Dispatches Subagent: @auditor (quality-verification.md)
       ├── Dispatches Subagent: @code-review (code-inspection.md)
       ├── Nests: generate-code (Skill)
       ├── Nests: audit-code (Skill)
       ├── Nests: kanban (Skill)
       ├── Nests: deploy-app (Skill)
       ├── Nests: visual-dashboard (Skill) [Syncs Overview Tab]
       └── Triggers Hook: lint-on-change.sh

5. /rewrite (Command)
   └── rewrite (Skill)
       ├── Nests: assess (Skill) [CodMod CLI & GCP Checks]
       ├── Nests: grill (Skill)
       ├── Nests: write-prd (Skill)
       └── Nests: research (Skill)

6. /record (Command)
   └── record (Skill)
       └── Nests: visual-dashboard (Skill) [Syncs Recap Tab]

7. /push (Command)
   └── github-workflow / git-delivery (Skills) [Creates GitHub PR via gh CLI]
```

---

## ⚡ 5. Automated Context Hooks (4 Total)

| Hook Name | Lifecycle Trigger | Executable Script | Action & Responsibility | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`coffee-and-git`** | `SessionStart` | **[`coffee-and-git.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/coffee-and-git.sh)** | Greets user with barista coffee brewing tip and displays recent git commit history. | **Active** |
| **`git-status`** | `SessionStart` | **[`git-status.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/git-status.sh)** | Injects current git branch and working directory status into context. | **Active** |
| **`recommend-devtools`** | `SessionStart` | **[`recommend-devtools.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/recommend-devtools.sh)** | Recommends Chrome DevTools extension if web UI assets are detected. | **Active** |
| **`lint-on-change`** | `PostToolUse` | **[`lint-on-change.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/lint-on-change.sh)** | Triggers linter validation immediately after code file edits. | **Active** |
