# ☕ Brew: Asciinema Terminal Recording Skill (01_GLOSSARY.md)

This glossary establishes the Ubiquitous Language for the **Asciinema Terminal Recording** feature. It ensures alignment between the agent, the CLI compiler, and the developer when discussing, recording, converting, and embedding CLI sessions.

---

## 1. Domain Terms

**Cast File (`.cast`)**:
The raw JSON-formatted session log produced by `asciinema rec`. It records timing and raw ANSI character output.
*Avoid*: log file, script recording, binary record

**Cast Visualizer / SVG Renderer**:
An engine or CLI utility (e.g., `svgterm` or `agg` - asciinema gif generator) that reads a `.cast` file and converts it into a visually stunning, animated SVG or GIF asset.
*Avoid*: converter, image capture, terminal screenshot

**Pre-scripted Scenario / Recording Script**:
A predefined YAML or Bash automation file that lists commands to be executed sequentially in a pseudo-terminal (PTY) to ensure clean, error-free, and perfectly timed recordings.
*Avoid*: test script, batch file, execution script

**Recording Harness**:
The wrapper subagent or utility responsible for configuring the PTY, ensuring the required recording binaries are available, setting prompt aesthetics (e.g., custom PS1), and orchestrating the execution of a pre-scripted scenario.
*Avoid*: runner, recorder shell
