---
name: asciinema
description: Record terminal interactions and compile them to animated GIFs. Use during walkthroughs or on-demand recording sessions.
---

# Asciinema Terminal Recording Skill

This skill allows agents to programmatically record terminal sessions, type out scenarios character-by-character, and render them as beautiful, high-quality animated `.gif` and `.cast` files.

## 1. Automated Playback Scenarios

When you need to record a repeatable walkthrough, construct a JSON scenario file.

### 1.1 Scenario Schema
Save your scenario file (e.g. `walkthrough_scenario.json`) inside the active feature's plan directory. Use the following schema:

```json
{
  "prompt": "agy ☕ ",
  "steps": [
    {
      "type": "comment",
      "text": "# Let's compile and validate the plugin",
      "delay": 1.0,
      "speed": 0.04
    },
    {
      "type": "command",
      "text": "agy plugin validate .",
      "delay": 2.0,
      "speed": 0.04
    }
  ]
}
```

*   `prompt`: (String, Optional) The terminal prompt displayed to the left of commands. Defaults to `agy ☕ `.
*   `steps`: (Array of Objects) The steps to execute sequentially.
    *   `type`: Must be `"comment"` (animated text output with trailing newline) or `"command"` (animated text output followed by sub-process execution).
    *   `text`: The commentary or shell command to run.
    *   `delay`: (Float, Optional) Time in seconds to pause after execution/printing. Defaults to `1.0`.
    *   `speed`: (Float, Optional) Delay in seconds between individual keystrokes during typing animation. Defaults to `0.04`.

---

## 2. Running the Recording

Trigger the terminal recording engine using the `brew:record` CLI command.

### 2.1 Contextual Recording (Stage 8 Walkthrough)
When recording a verification walkthrough for an active Brew:
1.  Save the scenario JSON file to the Brew's plan directory:
    `plans/feature/<brew-timestamp-slug>/walkthrough_scenario.json`.
2.  Execute the CLI command targeting that plan folder:
    ```bash
    agy brew:record --scenario plans/feature/<brew-timestamp-slug>/walkthrough_scenario.json --output plans/feature/<brew-timestamp-slug>/walkthrough
    ```
3.  Once complete, embed the resulting `.gif` asset directly inside your `08_WALKTHROUGH.md` report:
    ```markdown
    ![Walkthrough Demo](walkthrough.gif)
    ```
4.  Stage all generated files (`.cast`, `.gif`, `.json`) in Git:
    ```bash
    git add plans/feature/<brew-timestamp-slug>/
    ```

### 2.2 Standalone On-Demand Recording
To capture arbitrary interactive terminal sessions:
1.  Run the CLI command without scenario flags:
    ```bash
    agy brew:record --output docs/recordings/my-interactive-demo
    ```
2.  Type your commands inside the spawned shell.
3.  Type `exit` or press `Ctrl-D` to complete recording and auto-compile the `.gif`.
