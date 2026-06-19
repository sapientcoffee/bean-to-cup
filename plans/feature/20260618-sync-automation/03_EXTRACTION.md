# ☕ Brew: Decision Traceability & Auto-Sync (03_EXTRACTION.md)

This document contains our blind, factual research on the codebase architecture, existing CLI command structures, and GitHub CLI integrations required to implement the Plan Parser and Sync Engine.

---

## 1. Workspace Findings & CLI Structure

### 1.1 Flat Namespaces for Commands
Our research confirms that CLI command definitions are placed in `commands/` as flat namespace TOML files. For example:
- `commands/brew:record.toml`
- `commands/brew:init.toml`
- `commands/ddd:plan.toml`

Nesting folders (such as `commands/brew/record.toml`) is ignored by the compiler. Therefore, our sync command definition must be placed strictly at `commands/brew:sync.toml`.

### 1.2 Python CLI Script Styling
Existing helper scripts in `scripts/` (e.g., `playback.py` and `record.py`) use:
- Only Python 3 standard libraries to ensure lightweight, non-bloated, and secure execution.
- Subprocess operations to interact with shell processes and PTYs.
- Explicit Apache 2.0 Google license headers at the top of each file.

---

## 2. GitHub CLI Integration Details

We will use Python's `subprocess` module to call the native GitHub CLI (`gh`), which leverages the existing user authentication in the local terminal.

### 2.1 Retrieve Existing Issues (Idempotency)
To get currently open issues and prevent duplicates:
```bash
gh issue list --state open --json number,title,labels
```
We can parse this JSON response directly in Python to check if a task's title already exists.

### 2.2 Create Sub-Tasks
To create individual sub-tasks under the Parent Epic:
```bash
gh issue create --title "[Task] Step X.Y: <Task Name>" --body "<Body_Text>" --label "ready-for-dev"
```

### 2.3 Notify Human Gate
To post a verification comment to the Parent Epic issue:
```bash
gh issue comment <Epic_ID> --body "<Comment_Text>"
```

---

## 3. Existing 05_PLAN.md Formatting

Our research on [SKILL.md of Kanban](file:///home/robedwards/workspace/bean-to-cup/skills/kanban/SKILL.md) shows that the existing plan files use:
1. Checklist formatting: `^\s*[\-\*]\s+\[([ xX])\]\s+((Step\s+([\w\.]+))[:\-]\s*(.*))$/i`
2. Subheadings for details: `#### Step X.Y <Title>`
3. Metadata lines:
   - `*Target File:* <file>`
   - `*Verification:* <verify>`
   - `*Depends On:* <deps>` (New requirement from our grilling session)
