# ☕ Brew: Decision Traceability & Auto-Sync (04_SPEC.md)

## 1. CLI TOML Design (`commands/brew:sync.toml`)

The CLI command is defined at the root commands namespace:
```toml
description = "Parse 05_PLAN.md and synchronize tasks to GitHub issues"
prompt = """
You are running the `brew:sync` command. Your goal is to parse the active implementation plan and sync its tasks to GitHub issues.

Your instructions:
1. Parse the command-line arguments:
   - `--plan <path>`: Optional path to the plan file (defaults to finding the first `05_PLAN.md` under `plans/feature/*`).
   - `--epic <id>`: Optional GitHub Epic Issue number (if not provided, attempt to auto-detect from 02_PRD.md or the git branch/logs).
2. Execute the sync runner script:
   ```bash
   python3 scripts/sync.py [flags]
   ```
3. Report the synced issues, skipped duplicates, and the human gate coordination comment.
"""
```

---

## 2. Core Python Script (`scripts/sync.py`)

### 2.1 Component Architecture
```
┌────────────────────────────────────────────────────────┐
│                        sync.py                         │
├────────────────────────────────────────────────────────┤
│ 1. Parse Args (argparse)                               │
│ 2. Find Active 05_PLAN.md & 02_PRD.md                  │
│ 3. Parse Markdown Task Model                           │
│ 4. Fetch Active GitHub Issues (gh issue list)          │
│ 5. Perform Idempotency Filtering                       │
│ 6. Create Missing Tasks (gh issue create)              │
│ 7. Comment on Parent Epic (gh issue comment)           │
└────────────────────────────────────────────────────────┘
```

### 2.2 Parsing Schema & Grammar
*   **Checkbox Regex:** `r'^\s*[\-\*]\s+\[([ xX])\]\s+(Step\s+([\w\.]+))[:\-]\s*(.*)$'`
*   **Header Regex:** `r'^####\s+(Step\s+[\w\.]+)\s*(.*)$'`
*   **Metadata Regexes:**
    *   Target File: `r'^\s*[*\-\s]*target file:\s*([\w\-./]+)'`
    *   Verification: `r'^\s*[*\-\s]*verification:\s*(.+)'`
    *   Depends On: `r'^\s*[*\-\s]*depends on:\s*([\w\s.,]+)'`

### 2.3 Topological Sort Solver
The solver processes the list of tasks. For each task, it builds its incoming and outgoing dependency edges. It verifies that no circular references exist (generating a validation error if found).

---

## 3. Threat Model

1.  **Command Injection via Arguments:**
    *   *Threat:* Passing untrusted strings (e.g. malformed markdown headers or plan paths) into shell command executions.
    *   *Mitigation:* We will execute `subprocess.run` with `shell=False` and pass arguments as an explicit array. Raw user string interpolation into shells is strictly forbidden.
2.  **Authentication and Privilege Escalation:**
    *   *Threat:* Storing long-lived tokens in files or exposing secrets in code logs.
    *   *Mitigation:* The script relies entirely on the local `gh` configuration. If `gh auth status` returns non-zero, the script exits immediately with a clean error instructing the user to run `gh auth login`. No custom credentials will be captured or handled.

---

## 4. Telemetry & Error Handling

-   **Log Levels:** Clean, console-colored logs prefixed with timestamp and status indicators:
    *   `[INFO] [Sync] Synced Step 1.A successfully (#142)`
    *   `[SKIP] [Sync] Step 1.B already exists (#143)`
    *   `[ERROR] [Parser] Circular dependency detected: Step 1.A <-> Step 1.B`
-   **Graceful Rollback:** If issue creation fails midway (e.g. network timeout), log the error and cleanly output the list of issues that *were* created, avoiding any state corruption.
