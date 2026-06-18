# Ubiquitous Glossary

This is the central Domain-Driven Design (DDD) glossary for the **Bean-to-Cup** project. It establishes a rigorous Ubiquitous Language to prevent context drift and ensure complete linguistic alignment among human developers, orchestration engines, and specialized autonomous subagents.

---

## Core Domain Terms

**Brew**:
A discrete software feature, refactoring unit, or bug fix being actively developed under the Stage 0-9 protocol. 
_Avoid_: Task, issue, ticket, feature branch

**Autonomous Brewing Swarm**:
The collection of specialized, role-focused agentic engines (e.g., Orchestration Engine, Code Implementation Engine, Code Inspection Engine) working collaboratively to deliver a Brew.
_Avoid_: Agent pool, script set, AI assistants

**State Machine (Stage 0 to Stage 9 Protocol)**:
The strict, document-driven lifecycle that a Brew must traverse from raw ideation (Stage 0) through to PR delivery (Stage 9).
_Avoid_: Workflow, process, pipe, pipeline

**Document-as-Context**:
The architectural pattern where structured Markdown documents in a versioned plan directory act as the physical API and single source of truth between agent runs and human checkpoints.
_Avoid_: Chat history, prompt instructions, oral state

**Socratic Grilling (Socratic Alignment)**:
The initial phase and process of stress-testing a feature's requirements, boundaries, and domain vocabulary via an interactive interview prior to technical planning.
_Avoid_: Chatting, requirements gathering, brainstorming

**Orchestration Engine**:
The central controller of the swarm that maintains the protocol state, enforces execution boundaries, manages Git state (including stashing/rollback), and dispatches specialized subagents.
_Avoid_: Parent agent, main script, coordinator

**Context Firewall (Blind Research)**:
The practice of keeping requirement discovery and technical codebase extraction contextually separated to prevent LLM confirmation bias and context-window bloat during the research phase.
_Avoid_: Direct grep, full search, context pollution

**Physicalized Contract**:
Concrete interface definitions (e.g., TypeScript types, Proto schemas, database migrations, empty classes) that must be physically created and committed before functional logic is written.
_Avoid_: Implementation, draft, mock logic

**Test-Driven Implementation (TDD Loop)**:
The iterative development loop where a failing test is written to verify contract behavior (Red), minimal code is written to pass the test (Green), and the codebase is refactored (Refactor) under silent-on-success back-pressure.
_Avoid_: Coding first, manual testing, implementation run

**Walkthrough**:
The phase and automated process of launching local servers and using the browser agent or generalist tools to compile technical or visual evidence of a feature's completeness.
_Avoid_: Demo, showcase, manual validation
