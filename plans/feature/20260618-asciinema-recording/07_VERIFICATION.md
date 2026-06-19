# ☕ Brew: Asciinema Terminal Recording Skill (07_VERIFICATION.md)

This document outlines the Test-Driven Development (TDD) and verification strategy to ensure complete, functional, and self-healing terminal recording capabilities.

---

## 1. Automated Unit & Integration Tests

Because this feature relies on terminal simulation and external subprocesses (`asciinema`, `tmux`, and `agg`), we will perform direct programmatic validation of key logical modules:

### 1.1 Dependency Resolution & Architecture Detection
*   **Test**: Run `scripts/record.py`'s binary checker function.
*   **Assertion**:
    - Correctly identifies machine architecture (`x86_64` or `aarch64`).
    - Successfully checks for the presence of local/system `agg` and `tmux`.
    - If `agg` is missing, downloads the correct static binary, saves it to `.agents/bin/agg`, sets execute permissions (`chmod +x`), and caches it for future use.

### 1.2 Scenario Parsing
*   **Test**: Run a dry-run parsing of a sample JSON scenario.
*   **Assertion**:
    - Successfully reads `prompt` and standard JSON array of `steps`.
    - Validates presence of necessary fields (`type`, `text`, `delay`).

### 1.3 Simulation Playback Engine (`scripts/playback.py`)
*   **Test**: Invoke `scripts/playback.py` with a dummy scenario.
*   **Assertion**:
    - Output matches expected character timing (animated typing).
    - Executed shell commands successfully execute and stream outputs back to stdout.

---

## 2. Command Compilation & Integration

### 2.1 Schema Compliance
*   **Test**: Run `agy plugin validate .`.
*   **Assertion**:
    - The CLI compiles without errors.
    - `brew:record` command successfully registers.

### 2.2 End-to-End Recording Run
*   **Test**: Run `agy brew:record --scenario plans/feature/20260618-asciinema-recording/test_scenario.json`.
*   **Assertion**:
    - Spawns a containerized TMUX session of exactly `100x30` dimensions.
    - Records the terminal output using `asciinema`.
    - Automatically downloads and invokes `agg` to generate a high-quality, animated `.gif` file.
    - Verifies that the `.cast` and `.gif` files exist and are populated.
