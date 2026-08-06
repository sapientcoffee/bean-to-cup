---
name: grill
description: Stage 1 - A relentless Socratic interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
---

# Skill: Grill (Stage 1)

## Objective
Your goal is to conduct a Socratic alignment and requirements gathering session. You must analyze the requirements of the feature or change, identify ambiguities, challenge terms, and stress-test the design before any technical specification is drafted.

## 00_IDEATION.md Context Check & Plan Directory Reuse
1. **Search for Ideation Output & Existing Plan Directory**: First, check if an existing plan directory under `plans/<feature-slug>/` or an ideation draft file (`00_IDEATION.md`) exists.
   - Look under `plans/<feature-slug>/<timestamp>/`. **REUSE that exact plan directory** for all subsequent stage outputs. Do NOT create a new timestamp folder when `ideator` or a prior stage was already run!
   - Also check the fallback path `.plans/00_IDEATION.md`.
2. **Use Context if Exists**: If `00_IDEATION.md` exists in the plan directory, read it immediately. Use the identified friction points, target personas, customer user journeys (CUJs), ADK orchestration topologies, and mock JSON schema inside it to prime and guide the grilling session.
3. **Fallback**: If no existing plan directory or `00_IDEATION.md` file is found, proceed with the grilling session using the user's initial prompt and create a new timestamped plan directory `plans/<feature-slug>/<timestamp>/`.

## Instructions
1. Engage in Socratic requirements gathering by running a relentless interactive interview (`/grilling` session) with the user.
2. Align with the `/domain-modeling` skill guidelines:
   - Challenge terms against the ubiquitous language.
   - Challenge design assumptions and align requirements with Google Cloud Well-Architected Framework pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency), deployment strategies, and SRE/observability best practices.
   - Sharpen fuzzy or overloaded terms.
   - Discuss concrete scenarios and probe edge cases one-by-one.
   - Write or update the global glossary (`docs/glossary.md`) directly on-the-fly as terms are resolved (do NOT write a local `01_GLOSSARY.md` file).
   - Record architectural decisions as ADRs inside `docs/adr/` if they meet the ADR criteria.
   - **Unified Visual Dashboard (`visual-dashboard.html`) - Stage 1 (Glossary & ADR Tabs)**: Ensure the dashboard exists by executing `python3 scripts/manage_dashboard.py ensure --plan-dir "plans/{feature-slug}/{timestamp}" --moniker "{feature-slug}"` (or invoke the `visual-dashboard` skill). Directly sync terms and ADRs by executing `python3 scripts/manage_dashboard.py sync-glossary --plan-dir "plans/{feature-slug}/{timestamp}" --moniker "{feature-slug}" --stage "Stage 1"`.
   - **Zero Intermediate Snippet Files**: Do NOT write any temporary HTML files. `sync-glossary` parses `docs/glossary.md` and `docs/adr/` directly and mirrors to system artifacts.