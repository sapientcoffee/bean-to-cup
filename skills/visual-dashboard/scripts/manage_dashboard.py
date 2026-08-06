#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Central Visual Dashboard Lifecycle Manager.
Provides environment-agnostic checking, creation, preservation, direct markdown sync,
stage section updating, and automatic AGY brain artifact mirroring for visual-dashboard.html.
Conforms to Google Antigravity Skills specification (https://antigravity.google/docs/skills).
"""

import argparse
import datetime
import html
import os
import re
import shutil
import subprocess
import sys


def find_repo_root():
    """Finds the root directory of the repository dynamically."""
    env_dir = os.environ.get("AGY_PLUGIN_DIR") or os.environ.get("BEAN_TO_CUP_DIR")
    if env_dir and os.path.exists(os.path.join(env_dir, "templates", "visual-dashboard.html")):
        return os.path.abspath(env_dir)

    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if os.path.exists(os.path.join(git_root, "templates", "visual-dashboard.html")):
            return git_root
    except Exception:
        pass

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    if os.path.exists(os.path.join(parent_dir, "templates", "visual-dashboard.html")):
        return parent_dir

    return os.getcwd()


def get_template_path():
    """Returns absolute path to visual-dashboard.html template searching multiple candidate locations."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    sibling_resource = os.path.abspath(os.path.join(script_dir, "..", "resources", "visual-dashboard.html"))
    if os.path.exists(sibling_resource):
        return sibling_resource

    repo_root = find_repo_root()
    skill_resource = os.path.join(repo_root, "skills", "visual-dashboard", "resources", "visual-dashboard.html")
    if os.path.exists(skill_resource):
        return skill_resource

    home_dir = os.path.expanduser("~")
    plugin_template = os.path.join(
        home_dir, ".gemini", "skills", "bean-to-cup", "skills", "visual-dashboard", "resources", "visual-dashboard.html"
    )
    if os.path.exists(plugin_template):
        return plugin_template

    return sibling_resource


def find_brain_dirs():
    """
    Locates all active Antigravity (AGY) conversation brain artifact directories
    across ~/.gemini/antigravity-cli/brain/ and ~/.gemini/antigravity/brain/.
    """
    dirs = []
    home_dir = os.path.expanduser("~")
    conv_id = os.environ.get("AGY_CONVERSATION_ID") or os.environ.get("CONVERSATION_ID")
    explicit_brain = os.environ.get("AGY_BRAIN_DIR")

    if explicit_brain and os.path.exists(explicit_brain):
        dirs.append(explicit_brain)

    parents = [
        os.path.join(home_dir, ".gemini", "antigravity-cli", "brain"),
        os.path.join(home_dir, ".gemini", "antigravity", "brain"),
    ]

    for brain_parent in parents:
        if conv_id:
            conv_path = os.path.join(brain_parent, conv_id)
            if os.path.exists(os.path.dirname(conv_path)):
                os.makedirs(conv_path, exist_ok=True)
                if conv_path not in dirs:
                    dirs.append(conv_path)

        if os.path.exists(brain_parent):
            entries = [
                os.path.join(brain_parent, d)
                for d in os.listdir(brain_parent)
                if os.path.isdir(os.path.join(brain_parent, d))
            ]
            if entries:
                entries.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                latest = entries[0]
                if latest not in dirs:
                    dirs.append(latest)

    return dirs


def get_model_and_thinking_info(override_model=None, override_thinking=None):
    """
    Detects model version and thinking mode from parameters, environment, or default fallback.
    """
    model = (
        override_model
        or os.environ.get("AGY_MODEL_VERSION")
        or os.environ.get("AGY_MODEL")
        or os.environ.get("GEMINI_MODEL")
        or os.environ.get("MODEL_NAME")
        or "Gemini 3.6 Flash"
    )
    thinking = (
        override_thinking
        or os.environ.get("AGY_THINKING_MODE")
        or os.environ.get("THINKING_MODE")
        or os.environ.get("GEMINI_THINKING_MODE")
        or "Medium"
    )
    return model, thinking


def ensure_dashboard(plan_dir, moniker, timestamp=None, model_version=None, thinking_mode=None, force=False):
    """
    Checks if visual-dashboard.html exists in plan_dir.
    If missing or outdated, creates/upgrades it from template and populates placeholders.
    Returns path to the dashboard HTML file.
    """
    template_path = get_template_path()

    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(plan_dir, exist_ok=True)
    target_dashboard = os.path.join(plan_dir, "visual-dashboard.html")

    if not timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    model_ver, thinking = get_model_and_thinking_info(model_version, thinking_mode)

    if force or not os.path.exists(target_dashboard):
        print(f"Instantiating missing/upgraded dashboard from template ({template_path}) -> {target_dashboard}")
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace("{{MONIKER}}", moniker)
        content = content.replace("{{TIMESTAMP}}", timestamp)
        content = content.replace("{{MODEL_VERSION}}", model_ver)
        content = content.replace("{{THINKING_MODE}}", thinking)
        active_plan_rel = os.path.join(plan_dir, "05_PLAN.md")
        content = content.replace("plans/feature/{{MONIKER}}/05_PLAN.md", active_plan_rel)

        with open(target_dashboard, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        with open(target_dashboard, "r", encoding="utf-8") as f:
            content = f.read()

        # Automatically upgrade outdated dashboard instances missing new markers or features
        if "<!-- VP:OVERVIEW -->" not in content or "demo-toggle" not in content:
            print(f"Upgrading outdated dashboard at {target_dashboard} to match latest template...")
            return ensure_dashboard(plan_dir, moniker, timestamp, model_version, thinking_mode, force=True)

        print(f"Preserving existing dashboard at {target_dashboard}")

        updated = content.replace("{{MODEL_VERSION}}", model_ver).replace("{{THINKING_MODE}}", thinking)
        updated = re.sub(r'<span class="mono" id="modelLabel">.*?</span>', f'<span class="mono" id="modelLabel">{html.escape(model_ver)}</span>', updated)
        updated = re.sub(r'<span class="mono" id="thinkingLabel">.*?</span>', f'<span class="mono" id="thinkingLabel">{html.escape(thinking)}</span>', updated)

        if updated != content:
            with open(target_dashboard, "w", encoding="utf-8") as f:
                f.write(updated)

    return target_dashboard


def update_section(dashboard_path, section_marker, new_content, optional=False):
    """
    Updates the content between <!-- MARKER --> and <!-- /MARKER --> comment blocks directly.
    """
    if not os.path.exists(dashboard_path):
        print(f"Error: Dashboard file does not exist at {dashboard_path}", file=sys.stderr)
        sys.exit(1)

    with open(dashboard_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = f"<!-- {section_marker} -->"
    end_marker = f"<!-- /{section_marker} -->"

    pattern = re.escape(start_marker) + r"(.*?)" + re.escape(end_marker)
    replacement = f"{start_marker}\n{new_content}\n{end_marker}"

    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully updated section [{section_marker}] in {dashboard_path}")
    elif not optional:
        print(f"Warning: Marker [{start_marker}] not found in {dashboard_path}", file=sys.stderr)


def sync_prd(plan_dir, moniker="feature"):
    """
    Parses 02_PRD.md directly and updates visual-dashboard.html with full-fidelity HTML cards.
    Zero temporary snippet files created on disk.
    """
    dashboard_path = ensure_dashboard(plan_dir, moniker)

    prd_candidates = [
        os.path.join(plan_dir, "02_PRD.md"),
        os.path.join(".plans", "02_PRD.md"),
        "02_PRD.md",
    ]
    prd_path = next((p for p in prd_candidates if os.path.exists(p)), None)

    if not prd_path:
        print(f"Warning: No 02_PRD.md found under {plan_dir}", file=sys.stderr)
        return

    with open(prd_path, "r", encoding="utf-8") as f:
        prd_raw = f.read()

    # 1. Update Raw PRD text container
    raw_escaped = html.escape(prd_raw)
    update_section(dashboard_path, "VPO:RAW_PRD", f'<div class="raw-prd-box" id="raw-prd-box">{raw_escaped}</div>', optional=True)

    # 2. Render all sections into full-fidelity HTML cards
    blocks = [
        f"""<button class="raw-prd-toggle-btn" onclick="const box = document.getElementById('raw-prd-box'); box.style.display = box.style.display === 'block' ? 'none' : 'block';" style="margin-bottom:12px;">
  📄 View Raw 02_PRD.md Document
</button>"""
    ]

    sections = re.split(r"(?=\n##\s+)", prd_raw)
    for sec in sections:
        sec_str = sec.strip()
        if not sec_str:
            continue
        lines = sec_str.split("\n", 1)
        header_line = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        title = re.sub(r"^#+\s*", "", header_line).strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        if not body and not title:
            continue
        rendered_body = render_markdown_content(body)
        blocks.append(f"""<div class="card" style="margin-bottom:16px;">
  <h3 style="margin-bottom:12px;">📄 {html.escape(title)}</h3>
  <div style="font-size: 14px; color: var(--fg); white-space: pre-wrap; line-height: 1.6;">{rendered_body}</div>
</div>""")

    update_section(dashboard_path, "VPO:OVERVIEW", "\n\n".join(blocks))
    mirror_artifact(dashboard_path)


def sync_glossary(plan_dir, moniker="feature", active_stage="Stage 1"):
    """
    Parses docs/glossary.md and docs/adr/ directly and updates visual-dashboard.html.
    Flags newly added terms introduced in later stages.
    Zero temporary snippet files created on disk.
    """
    dashboard_path = ensure_dashboard(plan_dir, moniker)

    glossary_path = None
    curr_dir = os.path.abspath(plan_dir)
    while curr_dir and curr_dir != os.path.dirname(curr_dir):
        cand = os.path.join(curr_dir, "docs", "glossary.md")
        if os.path.exists(cand):
            glossary_path = cand
            break
        curr_dir = os.path.dirname(curr_dir)

    if not glossary_path:
        repo_root = find_repo_root()
        fallback = os.path.join(repo_root, "docs", "glossary.md")
        if os.path.exists(fallback):
            glossary_path = fallback

    adr_dir = os.path.join(find_repo_root(), "docs", "adr")

    # Render Glossary Terms
    if glossary_path and os.path.exists(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary_raw = f.read()

        terms_html = ['<div class="grid cols-2">']
        # Extract term blocks (### Term or **Term**:)
        term_blocks = re.findall(r"(?:###|\*\*)\s*(.*?)(?:\*\*)?:?\n+(.*?)(?=\n(?:###|\*\*)|$)", glossary_raw, re.DOTALL)
        for term_title, term_body in term_blocks:
            clean_title = html.escape(term_title.strip())
            clean_body = html.escape(term_body.strip()).replace(chr(10), '<br>')

            # Check for stage addition flags (e.g., [Added Stage 2] or [New])
            added_badge = ""
            if "[Added Stage" in term_title or "[NEW]" in term_title or active_stage in ("Stage 2", "Stage 4", "Stage 7"):
                added_badge = f' <span class="badge added">ADDED ({html.escape(active_stage)})</span>'

            terms_html.append(f"""  <div class="card">
    <div class="term-title">{clean_title}{added_badge}</div>
    <p style="font-size: 14px; color: var(--fg); margin: 0;">{clean_body}</p>
  </div>""")
        terms_html.append('</div>')
        update_section(dashboard_path, "VG:GLOSSARY", "\n".join(terms_html))

    # Render ADRs
    if os.path.exists(adr_dir):
        adrs_html = ['<div class="grid cols-2">']
        adr_files = sorted([f for f in os.listdir(adr_dir) if f.endswith(".md")])
        for adr_f in adr_files:
            adr_path = os.path.join(adr_dir, adr_f)
            with open(adr_path, "r", encoding="utf-8") as f:
                adr_text = f.read()
            title_match = re.search(r"# (.*)", adr_text)
            adr_title = title_match.group(1).strip() if title_match else adr_f
            adrs_html.append(f"""  <div class="card">
    <div class="term-title">📄 {html.escape(adr_title)}</div>
    <p style="font-size: 13px; color: var(--muted); margin: 4px 0 0;">File: <code>docs/adr/{html.escape(adr_f)}</code></p>
  </div>""")
        adrs_html.append('</div>')
        update_section(dashboard_path, "VG:ADR", "\n".join(adrs_html))

    mirror_artifact(dashboard_path)


def mirror_artifact(dashboard_path, target_filename="00_visual-dashboard.html", brain_dir=None):
    """
    Copies visual-dashboard.html directly to all active AGY conversation brain directories.
    """
    if brain_dir:
        brain_dirs = [brain_dir]
    else:
        brain_dirs = find_brain_dirs()

    if brain_dirs:
        for b_dir in brain_dirs:
            os.makedirs(b_dir, exist_ok=True)
            artifact_path = os.path.join(b_dir, target_filename)
            if os.path.exists(artifact_path):
                try:
                    os.chmod(artifact_path, 0o644)
                except Exception:
                    pass
            try:
                shutil.copy2(dashboard_path, artifact_path)
            except PermissionError:
                try:
                    os.remove(artifact_path)
                    shutil.copy2(dashboard_path, artifact_path)
                except Exception as e:
                    print(f"Warning: Failed to mirror artifact to {artifact_path}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Failed to mirror artifact to {artifact_path}: {e}", file=sys.stderr)
def find_stage_file(plan_dir, filename):
    candidates = [
        os.path.join(plan_dir, filename),
        os.path.join(".plans", filename),
        filename,
    ]
    return next((p for p in candidates if os.path.exists(p)), None)


def render_markdown_content(md_text):
    """Helper to convert markdown elements (tables, code blocks, headers) to clean HTML."""
    # 1. Extract code blocks
    code_blocks = []
    def save_code(m):
        lang = m.group(1) or ""
        code = m.group(2)
        if lang.lower() == "mermaid":
            code_blocks.append(f'<pre class="mermaid">\n{html.escape(code.strip())}\n</pre>')
        else:
            code_blocks.append(f'<pre><code class="language-{lang or "text"}">{html.escape(code.strip())}</code></pre>')
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    md_text = re.sub(r"```(\w*)\n(.*?)```", save_code, md_text, flags=re.DOTALL)

    # 2. Extract tables
    def replace_table(match):
        table_str = match.group(0).strip()
        lines = [l.strip() for l in table_str.split("\n") if l.strip()]
        if len(lines) < 2:
            return table_str

        headers = [c.strip() for c in lines[0].strip("|").split("|")]
        rows = []
        start_idx = 2 if len(lines) > 1 and ":" in lines[1] or "-" in lines[1] else 1
        for line in lines[start_idx:]:
            cols = [c.strip() for c in line.strip("|").split("|")]
            rows.append(cols)

        tbl = ['<table class="va-table" style="width:100%; border-collapse:collapse; margin:12px 0; font-size:13px;">', '<thead><tr style="border-bottom:2px solid var(--border); background:var(--surface);">']
        for h in headers:
            tbl.append(f'<th style="text-align:left; padding:8px; font-weight:600;">{html.escape(h)}</th>')
        tbl.append('</tr></thead><tbody>')
        for r in rows:
            tbl.append('<tr style="border-bottom:1px solid var(--border);">')
            for c in r:
                tbl.append(f'<td style="padding:8px;">{html.escape(c)}</td>')
            tbl.append('</tr>')
        tbl.append('</tbody></table>')
        return "\n".join(tbl)

    tbl_pattern = r"\|[^\n]+\|\n\|[\s:\-\|]+\|\n(?:\|[^\n]+\|\n?)+"
    md_text = re.sub(tbl_pattern, replace_table, md_text)

    # 3. Restore code blocks
    for idx, block in enumerate(code_blocks):
        md_text = md_text.replace(f"__CODE_BLOCK_{idx}__", block)

    return md_text


def sync_ideation(plan_dir, moniker="feature"):
    """Parses 00_IDEATION.md and populates Stage 0 (Discovery) with 100% full-fidelity rendered sections."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "00_IDEATION.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    update_section(dashboard_path, "VD:RAW_IDEATION", f'<div class="raw-prd-box" id="raw-ideation-box">{html.escape(raw)}</div>', optional=True)

    blocks = [
        f"""<button class="raw-prd-toggle-btn" onclick="const box = document.getElementById('raw-ideation-box'); box.style.display = box.style.display === 'block' ? 'none' : 'block';" style="margin-bottom:12px;">
  📄 View Raw 00_IDEATION.md Document
</button>"""
    ]

    # Split markdown by top-level section headers (## Section)
    sections = re.split(r"(?=\n##\s+)", raw)

    for sec in sections:
        sec_str = sec.strip()
        if not sec_str:
            continue

        # Extract title
        lines = sec_str.split("\n", 1)
        header_line = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        title = re.sub(r"^#+\s*", "", header_line).strip()
        # Remove markdown horizontal rules at bottom of section body
        body = re.sub(r"\n---\s*$", "", body).strip()

        if not body and not title:
            continue

        # Convert markdown elements (tables, code blocks) in body
        rendered_body = render_markdown_content(body)

        blocks.append(f"""<div class="card" style="margin-bottom:16px;">
  <h3 style="margin-bottom:12px;">💡 {html.escape(title)}</h3>
  <div style="font-size: 14px; color: var(--fg); white-space: pre-wrap; line-height: 1.6;">{rendered_body}</div>
</div>""")

    update_section(dashboard_path, "VD:OVERVIEW", "\n\n".join(blocks))
    return True


def render_full_markdown_cards(dashboard_path, raw_md, raw_marker, overview_marker, doc_name):
    """Renders 100% full-fidelity section cards from markdown into the specified section markers."""
    raw_escaped = html.escape(raw_md)
    raw_box_id = f"raw-{raw_marker.lower().replace(':', '-')}-box"
    update_section(dashboard_path, raw_marker, f'<div class="raw-prd-box" id="{raw_box_id}">{raw_escaped}</div>', optional=True)

    blocks = [
        f"""<button class="raw-prd-toggle-btn" onclick="const box = document.getElementById('{raw_box_id}'); box.style.display = box.style.display === 'block' ? 'none' : 'block';" style="margin-bottom:12px;">
  📄 View Raw {doc_name} Document
</button>"""
    ]

    sections = re.split(r"(?=\n##\s+)", raw_md)
    for sec in sections:
        sec_str = sec.strip()
        if not sec_str:
            continue
        lines = sec_str.split("\n", 1)
        header_line = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        title = re.sub(r"^#+\s*", "", header_line).strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        if not body and not title:
            continue
        rendered_body = render_markdown_content(body)
        blocks.append(f"""<div class="card" style="margin-bottom:16px;">
  <h3 style="margin-bottom:12px;">📄 {html.escape(title)}</h3>
  <div style="font-size: 14px; color: var(--fg); white-space: pre-wrap; line-height: 1.6;">{rendered_body}</div>
</div>""")

    update_section(dashboard_path, overview_marker, "\n\n".join(blocks))


def sync_prd(plan_dir, moniker="feature"):
    """Parses 02_PRD.md and populates Stage 2 (Product Requirements Document)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "02_PRD.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VPO:RAW_PRD", "VPO:OVERVIEW", "02_PRD.md")
    for extra in ["VPO:STORIES", "VPO:CRITERIA", "VPO:FLOWS", "VPO:CONSTRAINTS", "VPO:PROTO", "VPO:QUESTIONS", "VPO:COMMENTS"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def sync_extraction(plan_dir, moniker="feature"):
    """Parses 03_EXTRACTION.md and populates Stage 3 (Context Extraction)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "03_EXTRACTION.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VX:RAW_EXTRACTION", "VX:OVERVIEW", "03_EXTRACTION.md")
    for extra in ["VX:FINDINGS", "VX:REFERENCES", "VX:ARCH", "VX:QUESTIONS"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def sync_spec(plan_dir, moniker="feature"):
    """Parses 04_SPEC.md and populates Stage 4 (Technical Spec)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "04_SPEC.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VA:RAW_SPEC", "VA:OVERVIEW", "04_SPEC.md")
    for extra in ["VA:ARCHITECTURE", "VA:FILEMAP", "VA:CODE", "VA:API", "VA:SCHEMA", "VA:PROTO", "VA:QUESTIONS", "VA:COMMENTS"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def sync_plan(plan_dir, moniker="feature"):
    """Parses 05_PLAN.md and populates Stage 5 (Execution Planning)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "05_PLAN.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VP:RAW_PLAN", "VP:OVERVIEW", "05_PLAN.md")
    for extra in ["VP:SLICES", "VP:CONTRACTS", "VP:RISKS"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def sync_verification(plan_dir, moniker="feature"):
    """Parses 07_VERIFICATION.md and populates Stage 7 (TDD Implementation)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "07_VERIFICATION.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VV:RAW_VERIFICATION", "VV:OVERVIEW", "07_VERIFICATION.md")
    for extra in ["VV:SLICES", "VV:TESTS"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def sync_recap(plan_dir, moniker="feature"):
    """Parses 08_WALKTHROUGH.md and populates Stage 8 (Walkthrough Recap)."""
    dashboard_path = ensure_dashboard(plan_dir, moniker)
    filepath = find_stage_file(plan_dir, "08_WALKTHROUGH.md")
    if not filepath:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    render_full_markdown_cards(dashboard_path, raw, "VIR:RAW_RECAP", "VIR:OVERVIEW", "08_WALKTHROUGH.md")
    for extra in ["VIR:TASKS", "VIR:FILES", "VIR:CHANGES", "VIR:ARCH", "VIR:CONTRACTS", "VIR:UI", "VIR:VERIFY", "VIR:NOTES"]:
        update_section(dashboard_path, extra, "", optional=True)
    return True


def update_tracker_badges(dashboard_path, stage_files_present):
    """
    Updates the Stage Tracker Board badges in visual-dashboard.html based on actual stage files found.
    """
    if not os.path.exists(dashboard_path):
        return

    with open(dashboard_path, "r", encoding="utf-8") as f:
        content = f.read()

    for stage_num in range(10):
        badge_id = f"badge-stage-{stage_num}"
        has_file = stage_files_present.get(stage_num, False)

        if has_file:
            badge_html = f'<span class="badge new" id="{badge_id}">🟢 Complete</span>'
        else:
            if stage_num == 6 and stage_files_present.get(5, False) and not stage_files_present.get(7, False):
                badge_html = f'<span class="badge mod" id="{badge_id}" style="background:#ddf4ff; color:#0969da;">🛑 Gate Active</span>'
            else:
                badge_html = f'<span class="badge" id="{badge_id}" style="background:var(--faint); color:var(--muted);">⚪ Pending</span>'

        pattern = rf'<span class="badge[^"]*" id="{badge_id}".*?</span>'
        content = re.sub(pattern, badge_html, content)

    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(content)


def auto_sync(plan_dir, moniker="feature", brain_dir=None):
    """
    Scans plan_dir for all SDLC stage files, runs individual parsers for present artifacts,
    updates Stage Tracker Board badges dynamically, and mirrors all generated files.
    """
    dashboard_path = ensure_dashboard(plan_dir, moniker)

    stage_file_map = {
        0: "00_IDEATION.md",
        1: "docs/glossary.md",
        2: "02_PRD.md",
        3: "03_EXTRACTION.md",
        4: "04_SPEC.md",
        5: "05_PLAN.md",
        7: "07_VERIFICATION.md",
        8: "08_WALKTHROUGH.md",
    }

    stage_presence = {}

    if sync_ideation(plan_dir, moniker):
        stage_presence[0] = True

    repo_root = find_repo_root()
    if os.path.exists(os.path.join(repo_root, "docs", "glossary.md")):
        sync_glossary(plan_dir, moniker)
        stage_presence[1] = True

    if find_stage_file(plan_dir, "02_PRD.md"):
        sync_prd(plan_dir, moniker)
        stage_presence[2] = True

    if sync_extraction(plan_dir, moniker):
        stage_presence[3] = True

    if sync_spec(plan_dir, moniker):
        stage_presence[4] = True

    if sync_plan(plan_dir, moniker):
        stage_presence[5] = True

    if sync_verification(plan_dir, moniker):
        stage_presence[7] = True

    if sync_recap(plan_dir, moniker):
        stage_presence[8] = True

    update_tracker_badges(dashboard_path, stage_presence)
    mirror_artifact(dashboard_path, brain_dir=brain_dir)

    brain_dirs = [brain_dir] if brain_dir else find_brain_dirs()
    if brain_dirs:
        for b_dir in brain_dirs:
            os.makedirs(b_dir, exist_ok=True)
            for s_num, s_file in stage_file_map.items():
                found_path = find_stage_file(plan_dir, s_file)
                if found_path:
                    target_name = s_file.lower().replace("docs/", "")
                    t_path = os.path.join(b_dir, target_name)
                    if os.path.exists(t_path):
                        try:
                            os.chmod(t_path, 0o644)
                        except Exception:
                            pass
                    try:
                        shutil.copy2(found_path, t_path)
                    except Exception:
                        pass

    print(f"🟢 auto-sync completed for plan directory: {plan_dir}")


def main():
    parser = argparse.ArgumentParser(description="Central Visual Dashboard Lifecycle Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ensure subcommand
    parser_ensure = subparsers.add_parser("ensure", help="Ensure visual-dashboard.html exists in target plan directory")
    parser_ensure.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_ensure.add_argument("--moniker", required=True, help="Feature slug / moniker")
    parser_ensure.add_argument("--timestamp", help="Optional timestamp override")

    # auto-sync subcommand
    parser_auto = subparsers.add_parser("auto-sync", help="Automatically scan and sync all stage files in target plan directory")
    parser_auto.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_auto.add_argument("--moniker", default="feature", help="Feature slug / moniker")
    parser_auto.add_argument("--artifacts-dir", "--brain-dir", dest="brain_dir", help="Explicit target brain/artifacts directory")

    # sync-ideation subcommand
    parser_sync_ideation = subparsers.add_parser("sync-ideation", help="Parse 00_IDEATION.md and update visual-dashboard.html")
    parser_sync_ideation.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_ideation.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-prd subcommand
    parser_sync_prd = subparsers.add_parser("sync-prd", help="Directly parse 02_PRD.md and update visual-dashboard.html with full fidelity")
    parser_sync_prd.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_prd.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-glossary subcommand
    parser_sync_glossary = subparsers.add_parser("sync-glossary", help="Directly parse docs/glossary.md & docs/adr/ and update visual-dashboard.html")
    parser_sync_glossary.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_glossary.add_argument("--moniker", default="feature", help="Feature slug / moniker")
    parser_sync_glossary.add_argument("--stage", default="Stage 1", help="Active SDLC stage name for addition badges")

    # sync-extraction subcommand
    parser_sync_extraction = subparsers.add_parser("sync-extraction", help="Parse 03_EXTRACTION.md and update visual-dashboard.html")
    parser_sync_extraction.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_extraction.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-spec subcommand
    parser_sync_spec = subparsers.add_parser("sync-spec", help="Parse 04_SPEC.md and update visual-dashboard.html")
    parser_sync_spec.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_spec.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-plan subcommand
    parser_sync_plan = subparsers.add_parser("sync-plan", help="Parse 05_PLAN.md and update visual-dashboard.html")
    parser_sync_plan.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_plan.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-verification subcommand
    parser_sync_verification = subparsers.add_parser("sync-verification", help="Parse 07_VERIFICATION.md and update visual-dashboard.html")
    parser_sync_verification.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_verification.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-recap subcommand
    parser_sync_recap = subparsers.add_parser("sync-recap", help="Parse 08_WALKTHROUGH.md and update visual-dashboard.html")
    parser_sync_recap.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_recap.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # update subcommand
    parser_update = subparsers.add_parser("update", help="Update specific section inside visual-dashboard.html")
    parser_update.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_update.add_argument("--section", required=True, help="Section marker")
    parser_update.add_argument("--content", help="Raw HTML content string to insert")
    parser_update.add_argument("--file", help="Path to file containing HTML content to insert")

    # mirror subcommand
    parser_mirror = subparsers.add_parser("mirror", help="Dual-write visual-dashboard.html to active chat UI brain artifacts directory")
    parser_mirror.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_mirror.add_argument("--target-filename", default="00_visual-dashboard.html", help="Target filename in brain directory")
    parser_mirror.add_argument("--artifacts-dir", "--brain-dir", dest="brain_dir", help="Explicit target brain/artifacts directory")

    args = parser.parse_args()

    if args.command == "ensure":
        target_dashboard = ensure_dashboard(args.plan_dir, args.moniker, args.timestamp)
        mirror_artifact(target_dashboard)

    elif args.command == "auto-sync":
        auto_sync(args.plan_dir, args.moniker, brain_dir=args.brain_dir)

    elif args.command == "sync-ideation":
        sync_ideation(args.plan_dir, args.moniker)

    elif args.command == "sync-prd":
        sync_prd(args.plan_dir, args.moniker)

    elif args.command == "sync-glossary":
        sync_glossary(args.plan_dir, args.moniker, args.stage)

    elif args.command == "sync-extraction":
        sync_extraction(args.plan_dir, args.moniker)

    elif args.command == "sync-spec":
        sync_spec(args.plan_dir, args.moniker)

    elif args.command == "sync-plan":
        sync_plan(args.plan_dir, args.moniker)

    elif args.command == "sync-verification":
        sync_verification(args.plan_dir, args.moniker)

    elif args.command == "sync-recap":
        sync_recap(args.plan_dir, args.moniker)

    elif args.command == "update":
        target_dashboard = os.path.join(args.plan_dir, "visual-dashboard.html")
        content_to_insert = ""
        if args.file and os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                content_to_insert = f.read()
        elif args.content:
            content_to_insert = args.content
        else:
            print("Error: Either --content or --file must be specified for update", file=sys.stderr)
            sys.exit(1)

        update_section(target_dashboard, args.section, content_to_insert)
        mirror_artifact(target_dashboard)

    elif args.command == "mirror":
        target_dashboard = os.path.join(args.plan_dir, "visual-dashboard.html")
        mirror_artifact(target_dashboard, target_filename=args.target_filename, brain_dir=args.brain_dir)


if __name__ == "__main__":
    main()

