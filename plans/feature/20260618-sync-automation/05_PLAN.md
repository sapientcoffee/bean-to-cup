# Execution Plan: Decision Traceability & Auto-Sync (05_PLAN.md)

We will implement the automated plan parser and synchronization command (`brew:sync`) using standard python libraries and the GitHub CLI (`gh`).

---

## Implementation Plan

### Step 1.A: Create CLI Command Declaration
- [x] Step 1.A: Create commands/brew:sync.toml
  *Target File:* commands/brew:sync.toml
  *Verification:* Run `agy plugin validate .` to verify compilation, namespace mappings, and command declarations.

### Step 2.A: Implement Markdown Parser
- [x] Step 2.A: Implement scripts/sync.py Markdown Parser
  *Target File:* scripts/sync.py
  *Verification:* Run `python3 scripts/sync.py --plan plans/feature/20260618-sync-automation/05_PLAN.md --dry-run` to output parsed JSON tasks.
  *Depends On:* Step 1.A

### Step 2.B: Implement Topological Sort and Idempotency
- [x] Step 2.B: Implement scripts/sync.py Topological Sort and Idempotency
  *Target File:* scripts/sync.py
  *Verification:* Run `python3 scripts/sync.py --plan plans/feature/20260618-sync-automation/05_PLAN.md --dry-run` and verify DAG sequencing and duplicate checks against local logs.
  *Depends On:* Step 2.A

### Step 3.A: Implement gh Issue Provisioning & Commenter
- [x] Step 3.A: Implement scripts/sync.py gh Issue Provisioner and Commenter
  *Target File:* scripts/sync.py
  *Verification:* Run `agy brew:sync --plan plans/feature/20260618-sync-automation/05_PLAN.md --epic 1` to create task issues and verify the Stage 6 comment is posted to the Epic on GitHub.
  *Depends On:* Step 2.B

---

## Detailed Step Configurations

#### Step 1.A Create commands/brew:sync.toml
*Target File:* commands/brew:sync.toml
*Verification:* Run `agy plugin validate .`
Create the flat namespace command file matching `agy` schemas, which instructs the compiler how to map and invoke `scripts/sync.py` with standard arguments.

#### Step 2.A Implement scripts/sync.py Markdown Parser
*Target File:* scripts/sync.py
*Verification:* Run unit tests or dry-run validation scripts.
*Depends On:* Step 1.A
Implement the line-by-line regex parsing module using standard Python `re` to cleanly extract steps, labels, checkbox states, and section-specific headers (`*Target File:*`, `*Verification:*`, `*Depends On:*`).

#### Step 2.B Implement scripts/sync.py Topological Sort and Idempotency
*Target File:* scripts/sync.py
*Verification:* Run with sample circular and serial plans to verify sorting validation.
*Depends On:* Step 2.A
Implement a topological sort solver that sequences the steps correctly based on `*Depends On:*` metadata. Compare task titles against active open issues in the GitHub repository using `gh issue list --json title` to identify skipped duplicate tasks.

#### Step 3.A Implement scripts/sync.py gh Issue Provisioner and Commenter
*Target File:* scripts/sync.py
*Verification:* Execute `agy brew:sync --plan plans/feature/20260618-sync-automation/05_PLAN.md --epic 1` and view live issues on GitHub.
*Depends On:* Step 2.B
Implement the provisioning module that calls `gh issue create` for missing steps, automatically sets their metadata in the body, and posts a final handshake comment to the parent Epic notifying that tasks are ready for Phase 6 review.
