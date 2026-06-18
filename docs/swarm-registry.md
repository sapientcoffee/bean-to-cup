# ☕ Bean-to-Cup: Swarm & Command Registry

This document serves as the definitive reference manual and registry for all agents, skills, custom commands, and automated hooks within the **Bean-to-Cup** Autonomous Barista Swarm under the **Antigravity CLI (`agy`)**.

> [!NOTE]
> All custom commands, skills, and agents listed below comply with the `agy 2.0` schema. They are designed to operate strictly within the renumbered Stage 0 to Stage 9 SDLC protocol.

---

## ⌨️ 1. Custom Commands (19 Total)

All commands in this registry are registered natively in the flat `commands/` directory of the plugin. Nested folder structures are not used to guarantee proper discovery by the `agy` compiler.

| Command / Shortcut | Namespace | Target SDLC Stage | Core Objective & Behavior | Status |
| :--- | :--- | :--- | :--- | :--- |
| **[`/feature`](file:///home/robedwards/workspace/bean-to-cup/commands/feature.toml)** | global | **Stage 2** | Initiates the 9-stage feature development state machine, prompting requirements gathering. | **Active** |
| **[`/research`](file:///home/robedwards/workspace/bean-to-cup/commands/research.toml)** | global | **Stage 3** | Spawns parallel investigative agents to map codebase components and patterns. | **Active** |
| **[`/loop:start`](file:///home/robedwards/workspace/bean-to-cup/commands/loop:start.toml)** | loop | **Stage 7** | Starts the infinite, self-correcting development cycle (the Ralph loop) under TDD. | **Active** |
| **[`/loop:cancel`](file:///home/robedwards/workspace/bean-to-cup/commands/loop:cancel.toml)** | loop | **Stage 7** | Cancels any actively running self-correcting development loop. | **Active** |
| **[`/loop:help`](file:///home/robedwards/workspace/bean-to-cup/commands/loop:help.toml)** | loop | **Stage 7** | Displays diagnostic support and troubleshooting help for the loop commands. | **Active** |
| **[`/dev`](file:///home/robedwards/workspace/bean-to-cup/commands/dev.toml)** | global | **Utility** | General-purpose developer helper for non-complex, minor inline requests. | **Active** |
| **[`/startcycle`](file:///home/robedwards/workspace/bean-to-cup/commands/startcycle.toml)** | global | **Stage 1 & 7** | Resumes or bootstraps an existing active feature development cycle. | **Active** |
| **[`/brew:archive`](file:///home/robedwards/workspace/bean-to-cup/commands/brew:archive.toml)** | brew | **Maintenance** | Clears completed, spent feature grounds from the workspace to save context budget. | **Active** |
| **[`/brew:init`](file:///home/robedwards/workspace/bean-to-cup/commands/brew:init.toml)** | brew | **Bootstrapping** | *Legacy* command to bootstrap a local project with Head Barista templates. | ⚠️ **Deprecated**<br>*(Now handled automatically upon plugin registration in AGY 2.0)* |
| **[`/sql:analyze`](file:///home/robedwards/workspace/bean-to-cup/commands/sql:analyze.toml)** | sql | **Stage 3 / Spec** | Analyzes database schemas and legacy stored procedures for dependencies. | **Active** |
| **[`/ddd:logical`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:logical.toml)** | ddd | **DDD Stage 1** | Identifies logical subdomain boundaries and compiles the domain aggregate map. | **Active** |
| **[`/ddd:physical`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:physical.toml)** | ddd | **DDD Stage 2** | Defines physical design interfaces, database schemas, and contracts. | **Active** |
| **[`/ddd:plan`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:plan.toml)** | ddd | **DDD Stage 3** | Formulates a tactical, step-by-step DDD refactoring roadmap. | **Active** |
| **[`/ddd:implement`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:implement.toml)** | ddd | **DDD Stage 4** | Executes domain aggregate logic and handlers with unit tests. | **Active** |
| **[`/ddd:review`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:review.toml)** | ddd | **DDD Stage 5** | Performs architectural review and compliance testing against specs. | **Active** |
| **[`/ddd:fix`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:fix.toml)** | ddd | **DDD Stage 6** | Iteratively diagnoses and resolves compile or rule failures during refactoring. | **Active** |
| **[`/ddd:create-user-stories`](file:///home/robedwards/workspace/bean-to-cup/commands/ddd:create-user-stories.toml)** | ddd | **DDD Stage 7** | Synthesizes final refactored domain boundaries back into clear user stories. | **Active** |
| **[`/test:api`](file:///home/robedwards/workspace/bean-to-cup/commands/test:api.toml)** | test | **Stage 7** | Triggers suite-level automated endpoint testing and compliance checks. | **Active** |
| **[`/build:production`](file:///home/robedwards/workspace/bean-to-cup/commands/build:production.toml)** | build | **Stage 7 & 9** | Runs compilation, packaging, and builds production release artifacts. | **Active** |

---

## 🤖 2. Specialized Agents / Swarm (13 Total)

Specialized subagents are dispatched with specific, isolated prompts to execute targeted tasks. They are invoked using `@<alias>` in developer prompts.

| Agent Alias | Config File | Assigned Role | Target SDLC Stage | Core Focus & Area of Expertise | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`@architect`** | **[`system-design.md`](file:///home/robedwards/workspace/bean-to-cup/agents/system-design.md)** | Strategic Planner | **Stage 4 & 5** | Strategizes technical specification design (`04_SPEC.md`), physicalizes contracts, and constructs micro-step roadmaps (`05_PLAN.md`). | **Active** |
| **`@engineer`** | **[`code-implementation.md`](file:///home/robedwards/workspace/bean-to-cup/agents/code-implementation.md)** | Code Builder | **Stage 7** | Implements logical features and writes production-ready code strictly inside a failing-to-passing TDD loop. | **Active** |
| **`@auditor`** | **[`quality-verification.md`](file:///home/robedwards/workspace/bean-to-cup/agents/quality-verification.md)** | Quality Gatekeeper | **Stage 7** | Runs tests, verifies code against technical specifications, monitors regression, and compiles verification logs. | **Active** |
| **`@scout`** | **[`context-discovery.md`](file:///home/robedwards/workspace/bean-to-cup/agents/context-discovery.md)** | Investigative Researcher | **Stage 3** | Conducts codebase exploration, traces import graphs, and maps out actual state without recommending future code designs. | **Active** |
| **`@codebase-analyzer`** | **[`codebase-analysis.md`](file:///home/robedwards/workspace/bean-to-cup/agents/codebase-analysis.md)** | Technical Cartographer | **Stage 3** | Performs deep, surgical analysis of specific component implementations, patterns, and behaviors. | **Active** |
| **`@context-mapping`** | **[`context-mapping.md`](file:///home/robedwards/workspace/bean-to-cup/agents/context-mapping.md)** | Codebase Navigator | **Stage 3** | Maps entry points, component structures, and files relevant to a feature. | **Active** |
| **`@pattern-recognition`** | **[`pattern-recognition.md`](file:///home/robedwards/workspace/bean-to-cup/agents/pattern-recognition.md)** | Architecture Librarian | **Stage 3** | Locates existing code constructs, styles, and patterns to maintain consistency across modules. | **Active** |
| **`@security-auditor`** | **[`security-plan.md`](file:///home/robedwards/workspace/bean-to-cup/agents/security-plan.md)** | Security Sentry | **Stage 4** | Reviews security reports, audits static logic, and designs robust security remediation plans. | **Active** |
| **`@security-remediator`** | **[`security-reremediating.md`](file:///home/robedwards/workspace/bean-to-cup/agents/security-remediation.md)** | Security Developer | **Stage 7** | Specialized in implementing precise, isolated patches to resolve logic flaws and vulnerabilities. | **Active** |
| **`@vulnerability-scanner`** | **[`vulnerability-scan.md`](file:///home/robedwards/workspace/bean-to-cup/agents/vulnerability-scan.md)** | Risk Scanner | **Stage 7** | Performs static scanning, pattern matching, and configuration auditing to spot vulnerabilities. | **Active** |
| **`@code-review`** | **[`code-inspection.md`](file:///home/robedwards/workspace/bean-to-cup/agents/code-inspection.md)** | Architectural Critic | **Stage 7** | Evaluates code changes line-by-line for readability, structural smells, and complexity. | **Active** |
| **`@msbuild`** | **[`msbuild.md`](file:///home/robedwards/workspace/bean-to-cup/agents/msbuild.md)** | Compilation Engine | **Stage 7** | Executes MSBuild commands and compresses build feedback, returning concise error stacks. | **Active** |
| **`@pipeline-stages`** | **[`pipeline-stages.md`](file:///home/robedwards/workspace/bean-to-cup/agents/pipeline-stages.md)** | Release Engineer | **Stage 9** | Automatically handles branch validation, release hooks, and deployment stages. | **Active** |

---

## 🛠️ 3. Modular Skills (13 Total)

Skills are functional bundles of instructions, scripts, and examples found in the `skills/` directory that can be dynamically activated by agents to expand their capabilities.

| Skill Name | Primary SDLC Stage | Targeted Scope & Responsibility | Status |
| :--- | :--- | :--- | :--- |
| **[`ideator`](file:///home/robedwards/workspace/bean-to-cup/skills/ideator/SKILL.md)** | **Stage 0 (Optional)** | Brainstorms raw product ideas and feature requests, maps out persona friction points, and outputs `00_IDEATION.md`. | **Active** |
| **[`grill`](file:///home/robedwards/workspace/bean-to-cup/skills/grill/SKILL.md)** | **Stage 1** | Coordinates Socratic alignment interviews, managing glossary compilation and ADRs. | **Active** |
| **[`grilling`](file:///home/robedwards/workspace/bean-to-cup/skills/grilling/SKILL.md)** | **Stage 1** | Relentlessly questions the user on edge cases, scope boundaries, and personas to clarify the brief. | **Active** |
| **[`domain-modeling`](file:///home/robedwards/workspace/bean-to-cup/skills/domain-modeling/SKILL.md)** | **Stage 1, 4 & 5** | Compiles and updates the project-wide Ubiquitous Glossary in `docs/glossary.md` (and `01_GLOSSARY.md`) on-the-fly during requirements design. | **Active** |
| **[`feature`](file:///home/robedwards/workspace/bean-to-cup/skills/feature/SKILL.md)** | **Stage 2** | Prepares feature contexts and slugs, bootstraps versioned subdirectories, and launches Socratic alignment. | **Active** |
| **[`write-prd`](file:///home/robedwards/workspace/bean-to-cup/skills/write-prd/SKILL.md)** | **Stage 2** | Compiles requirements, KPIs, and in/out-of-scope boundaries into machine-parsable `02_PRD.md`. | **Active** |
| **[`research`](file:///home/robedwards/workspace/bean-to-cup/skills/research/SKILL.md)** | **Stage 3** | Coordinates context-isolated parallel codebase mapping and aggregates facts into `03_EXTRACTION.md`. | **Active** |
| **[`audit-code`](file:///home/robedwards/workspace/bean-to-cup/skills/audit-code/SKILL.md)** | **Stage 7** | Acts as QA to check spec alignment, find bugs, and commit changes inside the `app_build/` directory. | **Active** |
| **[`generate-code`](file:///home/robedwards/workspace/bean-to-cup/skills/generate-code/SKILL.md)** | **Stage 7** | Automatically scaffolds boilerplate, components, and controllers according to Spec contracts. | **Active** |
| **[`kanban`](file:///home/robedwards/workspace/bean-to-cup/skills/kanban/SKILL.md)** | **Stage 7** | Creates interactive progress boards (Markdown, Mermaid, & HTML) to visually track vertical slices. | **Active** |
| **[`chaos-mitigation`](file:///home/robedwards/workspace/bean-to-cup/skills/chaos-mitigation/SKILL.md)** | **Stage 7 & Day 2** | Investigates service logs and executes runbooks to resolve simulated outages in `press-service`. | **Active** |
| **[`deploy-app`](file:///home/robedwards/workspace/bean-to-cup/skills/deploy-app/SKILL.md)** | **Stage 7** | Automatically detects application framework stack, installs packages, and runs local servers. | **Active** |
| **[`github-workflow`](file:///home/robedwards/workspace/bean-to-cup/skills/github-workflow/SKILL.md)** | **Stage 9** | Manages git staging, milestoned commits, and automated PR generation with the GitHub CLI (`gh`). | **Active** |

---

## ⚡ 4. Automated Context Hooks (4 Total)

Hooks run automatically based on lifecycle triggers (Session Start or Post Tool Use) to inject context or enforce instant developer feedback.

| Hook Name | Lifecycle Trigger | Executable Script | Action & Responsibility | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`coffee-and-git`** | `SessionStart` | **[`coffee-and-git.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/coffee-and-git.sh)** | Greets the user with a fresh barista-style coffee brewing tip and displays recent git commit history. | **Active** |
| **`git-status`** | `SessionStart` | **[`git-status.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/git-status.sh)** | Queries the active git branch and uncommitted modifications to keep the agent's context grounded. | **Active** |
| **`recommend-devtools`** | `SessionStart` | **[`recommend-devtools.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/recommend-devtools.sh)** | Analyzes the project stack and recommends loading the Chrome DevTools extension if a UI is detected. | **Active** |
| **`lint-on-change`** | `PostToolUse` | **[`lint-on-change.sh`](file:///home/robedwards/workspace/bean-to-cup/hooks/lint-on-change.sh)** | Automatically triggers linter validation against modified code blocks, enforcing immediate back-pressure. | **Active** |
