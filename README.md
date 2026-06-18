> [!WARNING]
> **Demo/Illustrative Purpose Only**: This project is intended for inspiration and demonstration of AI-assisted development techniques. It should **not** be deployed to production environments without thorough testing, security audits, and validation. Use as a starting point for your own implementations.

# ☕ Bean-to-Cup: The Autonomous Barista Swarm

**Bean-to-Cup** is a comprehensive Gemini CLI extension designed to automate the entire Software Development Lifecycle (SDLC). It transforms the AI from a simple code generator into a structured **Autonomous Brewing Team** (Blueprint Forge) that follows a rigorous, multi-phase protocol to deliver high-quality, verified software.

![The Brewing Swarm](docs/images/brewing-swarm.png)

This is a collection of AI-assisted development techniques, steps, and methods I have been experimenting with and building up over the last year. It is always evolving, and the space is evolving very quickly.

---

## 📖 Core Philosophy: "The Perfect Brew"

Just as a master barista follows a precise recipe—from selecting the beans to the final pour—this extension treats software features as "Brews." It enforces a strict **State Machine** based on the "Document-as-Context" architecture, where Markdown files act as the API for your AI agents.

![The Control Funnel](docs/images/control-funnel.png)

This extension is a formal implementation of the **QRSPI method** (Questions, Research, Structure, Plan, Implement). This workflow combines the **RPI technique** (pioneered by **Dex Horthy** at HumanLayer) and the **Socratic Spec / AI-assisted product design** philosophies (pioneered by **Matt Pocock** at [AI Hero](https://www.aihero.dev/)). Together, these evolved into a state-of-the-art agentic pipeline protocol that ensures the human remains the "director" while the AI handles the "execution." It is designed to prevent "outsourcing thinking" by creating high-fidelity checkpoints where you and the AI must align.

### The AI-Native SDLC Stack
This extension implements emerging standards for AI-assisted development:

![The Artifact Filter](docs/images/artifact-filter.png)

| SDLC Stage | Standard / Convention | Artifact File | extension Role |
| :--- | :--- | :--- | :--- |
| **Stage 0 (Optional)** | Product Discovery | `00_IDEATION.md` | Formulate raw ideas, persona friction, and data schemas. |
| **Stage 1** | Socratic Alignment | `01_GLOSSARY.md` | Engage in Socratic interview & Ubiquitous Glossary. |
| **Stage 2** | Product Requirements | `02_PRD.md` | Machine-parsable requirements, NFRs, & non-goals. |
| **Stage 3** | Context Extraction | `03_EXTRACTION.md` | Factual codebase mapping (Blind Research). |
| **Stage 4** | Technical Specification | `04_SPEC.md` | Tech spec, Threat Model, SRE telemetry. |
| **Stage 5** | Execution Planning | `05_PLAN.md` | Slices, TDD checklist, & physical contracts. |
| **Stage 6** | Human Review Gate | *None (Halt)* | STOP. Verify contracts & specs before implementation. |
| **Stage 7** | Test-Driven Implementation | `07_VERIFICATION.md` | Incrementally execute code under TDD loop. |
| **Stage 8** | Automated Walkthrough | `08_WALKTHROUGH.md` | Visual & technical browser-based proof. |
| **Stage 9** | PR Delivery & Maintenance | *PR Description* | Push branch, submit PR with walkthrough report. |

---

### 🛡️ Spec-Driven Development (SDD)

Transitioning to SDD requires a shift in how you work with agents. If specifications are too long or vague, the agent will "drift" or experience context loss. This extension enforces these SDD tenets:

#### A. Prioritize Human Reviewability
The "fundamental test" of a spec is whether a human can review it effectively. If a specification change is too long to review in 5 minutes, the feature is too large. We keep specifications concise and focused on intentionality.

#### B. Solve the "Lost in the Middle" Problem
LLMs often struggle with information buried in the middle of long documents. We keep `04_SPEC.md` and `05_PLAN.md` files modular and use **Plan Mode** guardrails to iterate in a read-only state before generating any code.

#### C. Use "Boundary Specs" (What NOT to build)
Agents are prone to "over-implementing." Our artifacts explicitly list **Constraints** and **Non-Goals** (e.g., "Do not upgrade existing dependencies" or "Do not add authentication logic") to prevent scope drift.

#### D. Agentic Validation (Evals)
Don't just write tests; write Evals. In your `04_SPEC.md`, we define what "Success" looks like for the AI using measurable criteria (SLIs/SLOs), such as "The generated API must have a response time < 100ms."

---

## 🏗️ Architectural Overview

### The 9-Phase Protocol (The State Machine)
The extension follows a rigorous 9-phase protocol to move from initial idea to a verified Pull Request.

```mermaid
flowchart TD
    %% Define Google Colors for Sketchnote Style
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#333;
    classDef phase fill:#ffffff,stroke:#4285F4,stroke-width:2px,color:#333;
    classDef human fill:#ffffff,stroke:#EA4335,stroke-width:2px,color:#333,stroke-dasharray: 5 5;
    classDef agent fill:#ffffff,stroke:#34A853,stroke-width:2px,color:#333;
    classDef artifact fill:#ffffff,stroke:#FBBC05,stroke-width:2px,color:#333;
    classDef orchestrator fill:#ffffff,stroke:#4285F4,stroke-width:3px,color:#333;

    subgraph "Stage 0: Product Discovery (Optional)"
        P0[ideator: Stage 0 Discovery]:::agent
        A0[\00_IDEATION.md\]:::artifact
        P0 --> A0
    end

    Start_Raw((Start: Raw Idea)) --> P0
    A0 --> P1
    Start((Start: /feature)) --> P1

    subgraph "Stage 1: Socratic Alignment"
        P1[Orchestration Engine: Chat & Clarify]:::orchestrator
        H1{Human Approval}:::human
        A1_Glossary[\01_GLOSSARY.md\]:::artifact
        P1 --> H1
        H1 -- Approve --> A1_Glossary
    end

    subgraph "Stage 2: Product Requirements"
        A1_Glossary --> P2[Orchestration Engine: PRD Generation]:::orchestrator
        A1[\02_PRD.md\]:::artifact
        P2 --> A1
    end

    subgraph "Stage 3: Context Extraction"
        A1 --> P3[/Dispatch Specialized Engines\]:::agent
        P3_1(Context Mapping)
        P3_2(Codebase Analysis)
        P3_3(Pattern Finder)
        P3 --> P3_1 & P3_2 & P3_3
        P3_1 & P3_2 & P3_3 --> A2[\03_EXTRACTION.md\]:::artifact
    end

    subgraph "Stage 4: Technical Specification"
        A1 & A2 --> P4[/Dispatch @architect\]:::agent
        A3[\04_SPEC.md\]:::artifact
        P4 --> A3
    end

    subgraph "Stage 5: Execution Planning"
        A3 --> P5[/Dispatch @architect\]:::agent
        A4[\05_PLAN.md\]:::artifact
        P5 --> A4
    end

    subgraph "Stage 6: Human Review Gate"
        A4 --> H2{Human Approval}:::human
    end

    subgraph "Stage 7: Test-Driven Implementation"
        H2 -- Approve --> L_Start((Start Loop))
        L_Start --> P7_1[/Dispatch @engineer\]:::agent
        P7_1 --> P7_2[/Dispatch @auditor\]:::agent
        
        P7_2 -- "Fail (Code)" --> P7_1
        P7_2 -- "Fail (Plan)" --> P5
        P7_2 -- "Pass" --> P7_3[Orchestration Engine: Update Plan]:::orchestrator
        
        H3{Human Approval: Commit?}:::human
        P7_3 --> H3
        H3 -- Approve --> P7_4[(Git Commit)]
        
        P7_4 -- "More Tasks" --> L_Start
        P7_4 -- "All Done" --> A5[\07_VERIFICATION.md\]:::artifact
    end

    subgraph "Stage 8: Automated Walkthrough"
        A5 --> P8[/Dispatch @browser_agent\]:::agent
        A6[\08_WALKTHROUGH.md\]:::artifact
        P8 --> A6
    end

    subgraph "Stage 9: PR Delivery & Maintenance"
        A6 --> P9[Orchestration Engine: Push & PR]:::orchestrator
        End((Pull Request Created))
        P9 --> End
    end
```

### 1. The Head Barista (Supervisor) [CORE]
The heart of the extension is the `bean-to-cup.md` file. It acts as the **Head Barista** and **Guardian of the Protocol**. It ensures that "Intent" (PRD) is separated from "Extraction" (Research) to prevent bias.

**Key Mandates:**
*   **PRD over Specs:** Every feature starts with a machine-parsable `02_PRD.md` including **Non-Goals** and **SLIs/SLOs**.
*   **UI/UX Alignment:** The Architect (@architect) explicitly searches for an existing `design.md` in your root to ensure UI/UX consistency.
*   **SRE-Ready:** Requirements include initial telemetry and monitoring constraints for Day 2 operations.

---

## 🤖 The Brewing Swarm (Agents)

The Bean-to-Cup plugin manages an autonomous network of **13 specialized sub-agents**. You can invoke them in your chat prompts using `@<name>`. For a detailed description of each agent's config file and target SDLC stage, see the [Swarm & Command Registry](docs/swarm-registry.md#-2-specialized-agents--swarm-13-total).

| Agent | Role | Expertise & Focus | Status |
| :--- | :--- | :--- | :--- |
| **`@architect`** | The Planner | Strategic design patterns, `04_SPEC.md` specs, and `05_PLAN.md` roadmaps. | **CORE** |
| **`@engineer`** | The Builder | TDD implementation, Red-Green-Refactor, and production logic. | **CORE** |
| **`@auditor`** | The Gatekeeper | Spec validation, regression checking, and QA cupping. | **CORE** |
| **`@scout`** | The Investigator | Context-isolated codebase queries and raw context extraction. | **CORE** |
| **`@browser_agent`** | The Browser | Automated browser walkthroughs and visual UI/UX verification. | **CORE** |
| **`@codebase-analyzer`** | The Cartographer | Deep structural mapping and component tracing. | **CORE** |
| **`@context-mapping`** | The Navigator | Entrypoint mapping and rapid workspace discovery. | **CORE** |
| **`@pattern-recognition`** | The Librarian | Locating and mirroring existing architectural code patterns. | **CORE** |
| **`@security-auditor`** | The Planner Sentry | Secure architecture specifications and threat remediation plans. | **CORE** |
| **`@security-remediator`** | The Builder Sentry | Implementing isolated patches and correcting security vulnerabilities. | **CORE** |
| **`@vulnerability-scanner`** | The Scanner Sentry | Running static analysis scans to detect exposed secrets or flaws. | **CORE** |
| **`@code-review`** | The Critic | Line-by-line quality reviews and static code smells analysis. | **CORE** |
| **`@msbuild`** | The Compiler | MSBuild/compiler feedback compressor for rapid .NET builds. | **CORE** |
| **`@pipeline-stages`** | The CI/CD | automated release validation and delivery pipeline stages. | **CORE** |

---

## ⌨️ Custom Commands

The plugin implements **19 Custom Commands** mapped as flat namespace TOML declarations. For a comprehensive overview of every specialized command and its stage alignment, see the [Swarm & Command Registry](docs/swarm-registry.md#-1-custom-commands-19-total).

### Core Lifecycle
*   **`/feature <goal>`** [CORE]: Initiates the 9-phase protocol starting with an AI-Ready PRD.
*   **`/research <query>`** [CORE]: Spawns parallel agents for deep, factual technical extraction.
*   **`/loop:start`** [CORE]: Starts an infinite, self-correcting development loop (Ralph).

### Workspace Management
*   **`/brew:init`** [CORE] *(Deprecated)*: Legacy command to bootstrap your project. This setup is now handled automatically.
*   **`/brew:archive`** [CORE]: Clears away 'spent grounds' (completed tasks) to keep context clean.
*   **`/dev <task>`** [CORE]: General-purpose development helper for quick tasks.
*   **`/startcycle`** [CORE]: Logic for starting or resuming development cycles.

### Specialized Pipelines
*   **`/sql:analyze`** [CORE]: Deep analysis of legacy stored procedures and schema.
*   **`/ddd:*`** [CORE]: A 7-step pipeline (`logical`, `physical`, `plan`, `implement`, `review`, `fix`, `create-user-stories`) for SQL-to-DDD refactoring.
*   **`/test:api`** [CORE]: Specialized API testing and validation pipeline.
*   **`/build:production`** [CORE]: Production-ready build and packaging automation.

---

## 🛠️ Reusable Skills & Hooks

Each modular skill in the `skills/` directory complies with the open **Agent Skills specification**, enabling deep reuse. For the complete skill-to-stage mappings and execution scripts, see the [Swarm & Command Registry](docs/swarm-registry.md#-3-modular-skills-13-total).

### Skills
*   **`ideator`** [CORE]: **Stage 0 (Optional)**: Generates a product discovery and technical architecture draft from any raw hackathon prompt, writing the results to `.plans/CONTEXT_DRAFT.md`.
*   **`grill` / `grilling`** [CORE]: **Stage 1**: Relentless interactive interview and requirements stress-testing.
*   **`domain-modeling`** [CORE]: **Stage 1, 4 & 5**: Builds, refines, and maintains the ubiquitous glossary and domain models.
*   **`write-prd`** [CORE]: **Stage 2**: Standardizes requirements, non-goals, and KPIs into a machine-parsable `02_PRD.md`.
*   **`research`** [CORE]: **Stage 3**: Guides context-isolated codebase extraction into factual `03_EXTRACTION.md`.
*   **`audit-code`** [CORE]: **Stage 7**: Runs architectural compliance checks, QA gates, and executes minor commits.
*   **`generate-code`** [CORE]: **Stage 7**: Generates boilerplate and components according to Spec contracts.
*   **`kanban`** [CORE]: **Stage 7**: Progress tracking (HTML & Mermaid visualizer) for vertical sprint slices.
*   **`chaos-mitigation`** [CORE]: **Stage 7**: Handles SRE log inspection and runs automated mitigation playbooks.
*   **`deploy-app`** [CORE]: **Stage 7**: Resolves dependencies, compiles packages, and serves local webservers.
*   **`github-workflow`** [CORE]: **Stage 9**: Automates branch pushes and PR compilation with the GitHub CLI (`gh`).

### Automated Hooks
*   **`lint-on-change`** [CORE]: Automatically runs your linter whenever a file is modified.
*   **`coffee-and-git`** [CORE]: Provides a coffee tip and git history at session start.
*   **`git-status`** [CORE]: Keeps your current branch and workspace state visible.

---

## 🚀 Installation & Quickstart

This repository is **multi-compatible**: it functions seamlessly as a modern **Antigravity Plugin**, a standard **Agent Skills Package** via the `skills` CLI, and a legacy **Gemini CLI Extension**. 

You can use whichever harness or tool matches your workflow; they will coexist peacefully using their respective manifest files (`plugin.json` and `gemini-extension.json`) and standard layouts.

---

### Option A: Running as an Antigravity Plugin (Modern)

Antigravity natively scans your active workspace or user home directory to discover plugins and registers all included subagents, skills, and rules automatically.

We provide an automated, dependency-free Bash installer script (`install.sh`) at the root of the repository to set up the plugin.

#### 1. One-Line Installation (No local clone required)
If you are on a new machine and don't have the repository cloned locally, you can stream the installer directly via `curl` to clone and register the plugin in one step:

*   **Global-Level Installation** (Active across all of your projects):
    ```bash
    curl -sSL https://raw.githubusercontent.com/sapientcoffee/bean-to-cup/main/install.sh | bash
    ```
*   **Workspace-Level Installation** (Active only in the current workspace directory):
    ```bash
    curl -sSL https://raw.githubusercontent.com/sapientcoffee/bean-to-cup/main/install.sh | bash -s -- --workspace
    ```

#### 2. Local Clone Installation (Symlinked for Active Development)
If you are actively developing the plugin, or already have a local clone of this repository, run the installer script from the root of your clone. This creates a **symlink** to your development directory:

*   **Global Symlink** (Registers your local clone for all projects):
    ```bash
    ./install.sh
    ```
*   **Workspace-Level Symlink** (Registers your local clone inside the current project):
    ```bash
    ./install.sh --workspace
    ```

#### 3. How to Update the Plugin (`git pull`)
Updates are clean and simple depending on how the plugin was installed:

*   **If installed via Local Symlink (Development)**:
    Just run `git pull` inside your local clone. Since the plugin directory is symlinked, Antigravity picks up changes instantly.
*   **If installed via One-Line Curl (Direct Clones)**:
    The installer clones the real Git repository directly into the target location. You can fetch updates by navigating into that directory and pulling:
    ```bash
    cd ~/.gemini/skills/bean-to-cup
    git pull
    ```

#### 4. Verify Discovery
Start your Antigravity session. The platform automatically scans `plugin.json` and loads the custom skills and subagents:
*   View your active agents by listing them in your developer panel (or using the `/agents` helper).
*   Any skills inside the `skills/` directory (like `audit-code` or `github-workflow`) are instantly accessible to your active agent.

---

### Option B: Running as a Gemini CLI Extension (Legacy)

#### 1. Install the Extension
You can install or link the extension directly using the Gemini CLI.

**Via GitHub (Recommended):**
```bash
gemini extensions install https://github.com/sapientcoffee/bean-to-cup.git
```

**Via Local Path (For Development):**
```bash
# Clone the repository
git clone https://github.com/sapientcoffee/bean-to-cup.git

# Link the extension
gemini extensions link ./bean-to-cup
```

#### 2. Initialize your Workspace (Deprecated)
> [!NOTE]
> This step is deprecated under Antigravity 2.0. Workspace bootstrapping is now managed automatically upon plugin registration.
>
> If running on legacy Gemini CLI, you can still optionally run:
> ```bash
> /brew:init
> ```

#### 3. Start your first Brew
Begin the 9-phase protocol for a new feature:
```bash
/feature "Add a search bar to the coffee bean catalog"
```

---

### Option C: Installing Individual Skills via the Open Skills CLI (Universal)

Each capability inside our `skills/` directory complies with the open **Agent Skills specification** designed by Vercel Labs. This means you can install, manage, and use these skills across **over 40 supported local coding agents** (including Claude Code, Cursor, Windsurf, Roo Code, and more) using the universal `skills` CLI.

#### 1. List Available Skills in this Repository
You can query this repository directly using the `skills` CLI to see all discovered modular capabilities:
```bash
npx skills add sapientcoffee/bean-to-cup --list
```

#### 2. Install a Specific Skill
To add an individual skill (such as our high-performance code auditor) to your current project:
```bash
npx skills add sapientcoffee/bean-to-cup --skill audit-code
```

#### 3. Install All Skills Globally
To make the entire suite of `bean-to-cup` skills available globally across all of your local AI coding agents:
```bash
npx skills add sapientcoffee/bean-to-cup -g
```

---

**Credits**: [@dandobrin](https://github.com/dandobrin), [@jjdelorme](https://github.com/jjdelorme), [@cedricyao](https://github.com/cedricyao), [Dex Horthy](https://x.com/dexhorthy), [Matt Pocock](https://www.aihero.dev/).

*Created with ❤️ for demo/example purposes only.*
