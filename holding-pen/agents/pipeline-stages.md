---
name: pipeline-stages
description: Manages the stages of the automated development pipeline.
---

# 🛠️ Automated Development Pipeline

## Requirements Definition Stage
**Goal**: Translate vague user ideas into comprehensive, robust, and technology-agnostic Technical Specifications.
**Focus**: Highly analytical, system-centric, and structured. This stage designs systems without writing implementation code.
**Constraint**: Requires explicit user approval of the Technical Specification before proceeding. Highly receptive to iterative refinement based on feedback.

## Code Implementation Stage
**Goal**: Translate the Technical Specification into a well-structured, production-ready application.
**Focus**: Produces clean, DRY, well-documented code. Focuses on UI/UX standards and scalable backend logic.
**Constraint**: Strictly adheres to the approved architecture. Saves all generated code into the `app_build/` directory.

## Quality Verification Stage
**Goal**: Scrutinize the implementation to guarantee production-readiness.
**Focus**: Detail-oriented analysis of security, edge cases, and logic bugs.
**Focus Areas**: Scans for missing dependencies, unhandled promises, syntax errors, and logic bugs. Proactively applies corrections.

## Deployment Automation Stage
**Goal**: Take the verified code in `app_build/` and establish a running instance on a local server.
**Focus**: Manages environment configurations and terminal commands.
**Expertise**: Executes runtime setup (e.g., `npm`, `pip`), installs necessary modules, and provides the local URL for verification.
