---
name: visual-dashboard
description: Central capability to check, instantiate, preserve, update, and mirror the unified visual-dashboard.html artifact across all SDLC stages in any environment.
---

<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# ☕ Skill: Visual Dashboard Manager

This skill serves as the single central authority for checking, instantiating, preserving, updating, and mirroring the unified master `visual-dashboard.html` artifact across all SDLC stages (Stage 0 to Stage 9) in an environment-agnostic manner.

Conforms to the official [Google Antigravity Skills Specification](https://antigravity.google/docs/skills).

## 1. Objective
To maintain efficiency, modularity, and high signal-to-noise ratio by eliminating duplicate dashboard initialization boilerplate across SDLC skills and enforcing the **"Create-if-Missing, Preserve & Update"** lifecycle protocol and automatic AGY UI artifact mirroring.

## 2. Standard SDLC Section Markers

The master dashboard HTML contains dedicated comment block markers for each stage:

| SDLC Stage | Stage Name | Section Comment Markers / Parser Subcommand |
| :--- | :--- | :--- |
| **Stage 0** | Discovery / Ideation | `<!-- VD:RAW_IDEATION -->`, `<!-- VD:OVERVIEW -->` (`sync-ideation`) |
| **Stage 1** | Glossary & ADRs | `<!-- VG:GLOSSARY -->`, `<!-- VG:ADR -->` (`sync-glossary`) |
| **Stage 2** | PRD Visual Surfaces | `<!-- VPO:RAW_PRD -->`, `<!-- VPO:OVERVIEW -->`, `<!-- VPO:STORIES -->`, `<!-- VPO:CRITERIA -->`, `<!-- VPO:CONSTRAINTS -->` (`sync-prd`) |
| **Stage 3** | Context Extraction | `<!-- VX:RAW_EXTRACTION -->`, `<!-- VX:OVERVIEW -->`, `<!-- VX:FINDINGS -->`, `<!-- VX:REFERENCES -->` (`sync-extraction`) |
| **Stage 4** | Technical Design Spec | `<!-- VA:RAW_SPEC -->`, `<!-- VA:OVERVIEW -->`, `<!-- VA:ARCHITECTURE -->`, `<!-- VA:FILEMAP -->`, `<!-- VA:API -->`, `<!-- VA:SCHEMA -->` (`sync-spec`) |
| **Stage 5** | Execution Planning | `<!-- VP:RAW_PLAN -->`, `<!-- VP:OVERVIEW -->`, `<!-- VP:SLICES -->`, `<!-- VP:CONTRACTS -->` (`sync-plan`) |
| **Stage 7** | TDD Implementation | `<!-- VV:RAW_VERIFICATION -->`, `<!-- VV:OVERVIEW -->`, `<!-- VV:SLICES -->`, `<!-- VV:TESTS -->` (`sync-verification`) |
| **Stage 8** | Walkthrough Recap | `<!-- VIR:RAW_RECAP -->`, `<!-- VIR:OVERVIEW -->`, `<!-- VIR:TASKS -->`, `<!-- VIR:CHANGES -->`, `<!-- VIR:VERIFY -->` (`sync-recap`) |

---

## 3. Protocol & Execution Steps

Whenever an SDLC skill requires `visual-dashboard.html`:

### Step 1: Ensure Dashboard Exists & Auto-Sync
Check if `visual-dashboard.html` exists in the active plan directory (`plans/<feature-slug>/<timestamp>/`). Run `auto-sync` to automatically scan for all stage markdown files, parse present artifacts, set tracker badges, and mirror artifacts:

```bash
python3 scripts/manage_dashboard.py auto-sync --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"
```

### Step 2: Stage-Specific Sync or Section Update
Optionally execute stage-specific synchronization or direct marker updates:

```bash
python3 scripts/manage_dashboard.py sync-extraction --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"
```

### Step 3: Dual-Write / Mirror Artifact for AGY UI Rendering
`auto-sync` automatically mirrors the master dashboard (`00_visual-dashboard.html`) and stage markdown files (`00_ideation.md`, `02_prd.md`, `03_extraction.md`, `04_spec.md`, `05_plan.md`, `07_verification.md`, `08_walkthrough.md`) directly to the active AGY conversation brain artifacts directory (`<appDataDir>/brain/<conversation-id>/`) so all stage outputs render live in the chat UI panel.

---

## 4. Self-Contained Skill Directory Structure
Aligned with `https://antigravity.google/docs/skills`, this skill maintains a self-contained package layout:
```
skills/visual-dashboard/
├── SKILL.md                          (Skill instructions & metadata)
├── scripts/
│   └── manage_dashboard.py          (Deterministic CLI management script)
└── resources/
    └── visual-dashboard.html        (Master HTML dashboard template)
```

## 5. Environment-Agnostic Guarantee
- **Template Path Resolution**: The script automatically locates `resources/visual-dashboard.html` inside the skill directory, repo root `templates/visual-dashboard.html`, or global installed plugin path.
- **AGY UI Artifact Mirroring**: Automatically discovers active conversation brain directories (`~/.gemini/antigravity-cli/brain/<conversation-id>/` and `~/.gemini/antigravity/brain/<conversation-id>/`) to keep the side-panel Artifact viewer in sync.
- **Zero Hardcoded Paths**: Never hardcode user home directories in skill instructions or commands.
