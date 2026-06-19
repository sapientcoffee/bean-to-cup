# ☕ Brew: Asciinema Terminal Recording Skill (04_SPEC.md)

This Specification defines the architecture, physical contracts, and data schemas for the Asciinema Terminal Recording feature.

---

## 1. Physical Contracts & Files

The feature consists of the following new files:

1.  **CLI Command**: `commands/brew:record.toml`
2.  **Agent Skill**: `skills/asciinema/SKILL.md`
3.  **Orchestrator & Playback Script**: `scripts/record.py`
4.  **Local Binaries Directory**: `.agents/bin/` (specifically for housing the downloaded `agg` executable).

---

## 2. Command Schema: `commands/brew:record.toml`

The TOML configuration for the `agy` compiler:

```toml
description = "Record terminal interaction (interactive shell or pre-scripted scenario)"
prompt = """
You are running the `brew:record` command to record terminal actions.

Your instructions:
1. Parse the command flags:
   - `--scenario <path>`: Path to a scenario JSON file for automated playback.
   - `--output <path>`: Where to save the output `.cast` and `.gif` files.
   - `--upload`: If present, uploads the resulting `.cast` file to asciinema.org.
2. Execute the orchestrator script:
   `python3 scripts/record.py [flags]`
3. Output the recording results and rendering paths to the user.
"""
```

---

## 3. Scenario Schema (JSON)
To keep the plugin lightweight and zero-dependency, the pre-scripted scenario file uses the standard JSON format:

```json
{
  "prompt": "agy ☕ ",
  "steps": [
    {
      "type": "comment",
      "text": "# Checking git status",
      "delay": 1.0
    },
    {
      "type": "command",
      "text": "git status -s",
      "delay": 1.5
    }
  ]
}
```

---

## 4. Script Architecture: `scripts/record.py`

The python script will handle two modes, leveraging `tmux` for premium isolation if available.

### 4.1 Dependency Resolution & Self-Healing
1.  **Asciinema CLI**: Look up system `PATH`. If missing, raise install warning.
2.  **TMUX**: Look up system `PATH`. If missing, output a warning and fall back to direct (un-isolated) PTY shell execution.
3.  **AGG GIF Compiler**: Check system `PATH`. If missing, check local `.agents/bin/agg`. If missing, query `platform.machine()` and programmatically download the official static binary for Linux from GitHub Releases to `.agents/bin/agg` and make it executable.

### 4.2 Interactive Mode (No `--scenario`)
If no scenario is specified:
*   If `tmux` is available, launch:
    `asciinema rec <output_path>.cast -c "tmux new-session -A -s agy_interactive"`
    This provides an isolated, attachable tmux environment for the user.
*   Otherwise, fallback to direct:
    `asciinema rec <output_path>.cast`

### 4.3 Automated Mode (With `--scenario`)
If a scenario file is specified:
1.  Read the scenario JSON file.
2.  Determine output path. Default to `docs/recordings/<timestamp>.cast`.
3.  **TMUX-Containerized Playback (Preferred)**:
    - Spawn a detached tmux session with standardized grid geometry (e.g. 100 columns, 30 rows):
      `tmux new-session -d -s agy_rec -x 100 -y 30 "asciinema rec -c 'python3 scripts/playback.py <scenario_path>' <output_path>.cast"`
    - Poll tmux with `tmux has-session -t agy_rec` to monitor the playback until completion.
    - This guarantees 100% stable resolution, zero physical key pollution, and headless execution.
4.  **PTY Fallback (Backup)**:
    - If `tmux` is unavailable, execute `asciinema rec -c "python3 scripts/playback.py <scenario_path>" <output_path>.cast` directly.

### 4.4 Simulation Playback Engine: `scripts/playback.py`
Inside the isolated environment, `playback.py` reads the scenario:
*   Prints the custom `prompt`.
*   For each step:
    *   If `comment`: Types comment character-by-character to stdout, then prints newline and sleeps `delay`.
    *   If `command`: Types command character-by-character, prints newline, executes the command via `subprocess.Popen` (capturing and streaming actual stdout/stderr), and sleeps `delay`.

---

## 5. Walkthrough Integration
When the `walkthrough` or standard verification runs, subagents will use the `skills/asciinema/SKILL.md` instructions to write a verification script, run `agy brew:record --scenario scenario.json`, and embed the rendered `.gif` in their `08_WALKTHROUGH.md` reports.
