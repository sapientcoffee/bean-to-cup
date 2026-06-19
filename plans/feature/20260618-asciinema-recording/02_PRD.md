# ☕ Brew: Asciinema Terminal Recording Skill (02_PRD.md)

## 1. Product Overview & User Persona
As a developer or automation agent using the **Bean-to-Cup** CLI plugin repository, I want a standardized, robust, and self-healing terminal recording system so that I can automatically capture, convert, and embed technical demonstrations (both interactive and pre-scripted) inside READMEs and Walkthroughs.

---

## 2. Requirements & Features

### 2.1 Hybrid Execution Model
*   **Interactive Mode**: When run with no scenario argument, launch a subshell under `asciinema rec` directly. Allow the user to run commands interactively, saving the cast file when they type `exit` or hit `Ctrl-D`.
*   **Scripted/Automated Mode**: Accept a YAML scenario file. Execute each command programmatically inside a pseudo-terminal (PTY) with realistic typing delays, comments printed as "live typing", and automatic command execution.

### 2.2 Output Management & Conversion
*   **Local Cast Preservation**: Always save the raw JSON Lines `.cast` file to allow replay or future compilation.
*   **Automated GIF/SVG Compilation**: If a compiler tool (like `agg`) is available or can be fetched, compile the `.cast` file to a beautiful, animated GIF/SVG file.
*   **Optional Remote Upload**: If the `--upload` flag is passed, invoke `asciinema upload` to retrieve a public player link.

### 2.3 Self-Healing Dependency Resolution
*   **Asciinema CLI**: Check system path. If missing, look for a local fallback or error gracefully with installation commands.
*   **AGG GIF Compiler**: Check system path. If missing, attempt to download the official pre-compiled Linux binary from GitHub Releases into the workspace `.agents/bin/` folder. Gracefully skip GIF generation if downloads fail, outputting a clear warning.

### 2.4 Contextual Storage
*   **Walkthrough Integration**: When run during a Brew's Stage 8 Walkthrough, save assets to `plans/feature/<brew-timestamp>/<name>.gif` and automatically stage them in git.
*   **Standalone Usage**: When run on-demand via `agy brew:record`, save to `docs/recordings/<name>.gif`.

---

## 3. Non-Goals
*   Capturing desktop GUI or mouse movements (strictly CLI/PTY text only).
*   Providing a custom web-based player (we rely on native Markdown gif/svg rendering or asciinema.org player).
*   Handling audio recording.

---

## 4. Acceptance Criteria
1.  Running `agy brew:record` with no args opens an interactive shell session. Exiting the shell writes a `.cast` file to `docs/recordings/` and attempts to compile it to a `.gif`.
2.  Running `agy brew:record --scenario my_scenario.yaml` executes the steps programmatically with custom delays and typing animations, saving the outputs without requiring user keystrokes.
3.  If `agg` is missing, the command downloads the binary to `.agents/bin/` and successfully uses it.
4.  Recorded files during a Brew walkthrough are saved directly under that Brew's plan directory and automatically staged in Git.
