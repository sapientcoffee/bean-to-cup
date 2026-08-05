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

| SDLC Stage | Stage Name | Section Comment Marker |
| :--- | :--- | :--- |
| **Stage 0** | Discovery / Ideation | `<!-- VD:OVERVIEW -->` ... `<!-- /VD:OVERVIEW -->` |
| **Stage 1** | Glossary & ADRs | `<!-- VG:GLOSSARY -->` ... `<!-- /VG:GLOSSARY -->`<br>`<!-- VG:ADR -->` ... `<!-- /VG:ADR -->` |
| **Stage 2** | PRD Visual Surfaces | `<!-- VPO:OVERVIEW -->`, `<!-- VPO:STORIES -->`, `<!-- VPO:CRITERIA -->`, `<!-- VPO:FLOWS -->`, `<!-- VPO:CONSTRAINTS -->`, `<!-- VPO:PROTO -->`, `<!-- VPO:QUESTIONS -->`, `<!-- VPO:COMMENTS -->` |
| **Stage 4** | Technical Design Spec | `<!-- VA:OVERVIEW -->`, `<!-- VA:ARCHITECTURE -->`, `<!-- VA:DATA -->`, `<!-- VA:SECURITY -->`, `<!-- VA:SRE -->` |
| **Stage 7** | Interactive Kanban Board | Built-in `#kanban` workspace & `#mermaidContainer` |

---

## 3. Protocol & Execution Steps

Whenever an SDLC skill requires `visual-dashboard.html`:

### Step 1: Ensure Dashboard Exists
Check if `visual-dashboard.html` exists in the active plan directory (`plans/<feature-slug>/<timestamp>/`). If missing, instantiate it from the self-contained template (`resources/visual-dashboard.html`) and replace `{{MONIKER}}` and `{{TIMESTAMP}}`:

```bash
python3 <skill-dir>/scripts/manage_dashboard.py ensure --plan-dir "plans/<feature-slug>/<timestamp>" --moniker "<feature-slug>"
```
*(Or invoke via repo root `python3 scripts/manage_dashboard.py ensure ...`)*

### Step 2: Update Active Stage Section
Update only the section corresponding to the current stage while preserving all other previously generated stage tabs:

```bash
python3 <skill-dir>/scripts/manage_dashboard.py update --plan-dir "plans/<feature-slug>/<timestamp>" --section "<MARKER>" --file "<path-to-content-file>"
```
*(Or pass inline content via `--content "<html-snippet>")*

### Step 3: Dual-Write / Mirror Artifact for AGY UI Rendering
Mirror the resulting dashboard directly to the active AGY conversation brain artifacts directory (`<appDataDir>/brain/<conversation-id>/00_visual-dashboard.html`) so it renders live in the chat UI panel:

```bash
python3 <skill-dir>/scripts/manage_dashboard.py mirror --plan-dir "plans/<feature-slug>/<timestamp>"
```

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
