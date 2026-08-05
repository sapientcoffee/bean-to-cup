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
    repo_template = os.path.join(repo_root, "templates", "visual-dashboard.html")
    if os.path.exists(repo_template):
        return repo_template

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


def ensure_dashboard(plan_dir, moniker, timestamp=None):
    """
    Checks if visual-dashboard.html exists in plan_dir.
    If missing, creates it from template and populates placeholders.
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

    if not os.path.exists(target_dashboard):
        print(f"Instantiating missing dashboard from template ({template_path}) -> {target_dashboard}")
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace("{{MONIKER}}", moniker)
        content = content.replace("{{TIMESTAMP}}", timestamp)
        active_plan_rel = os.path.join(plan_dir, "05_PLAN.md")
        content = content.replace("plans/feature/{{MONIKER}}/05_PLAN.md", active_plan_rel)

        with open(target_dashboard, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(f"Preserving existing dashboard at {target_dashboard}")

    return target_dashboard


def update_section(dashboard_path, section_marker, new_content):
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
    else:
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
    update_section(dashboard_path, "VPO:RAW_PRD", f'<div class="raw-prd-box" id="raw-prd-box">{raw_escaped}</div>')

    # 2. Extract Problem Statement / Overview
    overview_match = re.search(r"## (?:Objective|Problem Statement|Overview)\n+(.*?)(?=\n## |\Z)", prd_raw, re.DOTALL | re.IGNORECASE)
    overview_text = overview_match.group(1).strip() if overview_match else "Product Requirements Document initialized."
    overview_html = f"""<div class="card">
  <h3>Objective & Business Impact</h3>
  <p>{html.escape(overview_text).replace(chr(10), '<br>')}</p>
</div>"""
    update_section(dashboard_path, "VPO:OVERVIEW", overview_html)

    # 3. Extract User Stories
    stories_html = ['<div class="grid cols-2">']
    stories = re.findall(r"- \*\*As a\b.*?(?=\n- \*\*As a|\n## |\Z)", prd_raw, re.DOTALL | re.IGNORECASE)
    if not stories:
        # Fallback bullet parsing
        stories = re.findall(r"- As a .*?(?=\n- As a |\n## |\Z)", prd_raw, re.DOTALL | re.IGNORECASE)

    for idx, story_text in enumerate(stories, 1):
        clean_text = html.escape(story_text.strip().lstrip("- "))
        stories_html.append(f"""  <div class="story">
    <span class="story-id">US-{idx:02d}</span>
    <div class="role">User Story</div>
    <div class="want">{clean_text}</div>
  </div>""")
    stories_html.append('</div>')
    update_section(dashboard_path, "VPO:STORIES", "\n".join(stories_html))

    # 4. Extract Acceptance Criteria / Scenarios
    criteria_html = ['<div class="grid cols-2">']
    scenarios = re.findall(r"### (?:Scenario|Criteria|Given).*\n+.*?(?=\n### |\n## |\Z)", prd_raw, re.IGNORECASE)
    if not scenarios:
        scenarios = re.findall(r"- Given .*?(?=\n- Given |\n## |\Z)", prd_raw, re.IGNORECASE)

    for idx, scen_text in enumerate(scenarios, 1):
        clean_scen = html.escape(scen_text.strip().lstrip("- "))
        criteria_html.append(f"""  <div class="scenario">
    <div class="title"><span class="tag">AC-{idx:02d}</span> Acceptance Criterion</div>
    <p style="font-size: 14px; margin: 0;">{clean_scen.replace(chr(10), '<br>')}</p>
  </div>""")
    criteria_html.append('</div>')
    update_section(dashboard_path, "VPO:CRITERIA", "\n".join(criteria_html))

    # 5. Extract Constraints & NFRs
    nfr_match = re.search(r"## Non-Functional Requirements.*?\n+(.*?)(?=\n## |\Z)", prd_raw, re.DOTALL | re.IGNORECASE)
    nfr_text = nfr_match.group(1).strip() if nfr_match else "Standard enterprise NFRs active."
    constraints_html = f"""<div class="card">
  <h3>Non-Functional Requirements & Security Posture</h3>
  <p style="font-size: 14px; white-space: pre-wrap;">{html.escape(nfr_text)}</p>
</div>"""
    update_section(dashboard_path, "VPO:CONSTRAINTS", constraints_html)

    mirror_artifact(dashboard_path)


def sync_glossary(plan_dir, moniker="feature", active_stage="Stage 1"):
    """
    Parses docs/glossary.md and docs/adr/ directly and updates visual-dashboard.html.
    Flags newly added terms introduced in later stages.
    Zero temporary snippet files created on disk.
    """
    dashboard_path = ensure_dashboard(plan_dir, moniker)

    repo_root = find_repo_root()
    glossary_path = os.path.join(repo_root, "docs", "glossary.md")
    adr_dir = os.path.join(repo_root, "docs", "adr")

    # Render Glossary Terms
    if os.path.exists(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary_raw = f.read()

        terms_html = ['<div class="grid cols-2">']
        # Extract term blocks (### Term)
        term_blocks = re.findall(r"### (.*?)\n+(.*?)(?=\n### |\n## |\Z)", glossary_raw, re.DOTALL)
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


def mirror_artifact(dashboard_path, target_filename="00_visual-dashboard.html"):
    """
    Copies visual-dashboard.html directly to all active AGY conversation brain directories.
    """
    brain_dirs = find_brain_dirs()
    if brain_dirs:
        for brain_dir in brain_dirs:
            os.makedirs(brain_dir, exist_ok=True)
            artifact_path = os.path.join(brain_dir, target_filename)
            shutil.copy2(dashboard_path, artifact_path)
            print(f"Successfully mirrored AGY UI artifact to file://{artifact_path}")
    else:
        print("Note: Brain directory not found for artifact mirroring; skipping.")


def main():
    parser = argparse.ArgumentParser(description="Central Visual Dashboard Lifecycle Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ensure subcommand
    parser_ensure = subparsers.add_parser("ensure", help="Ensure visual-dashboard.html exists in target plan directory")
    parser_ensure.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_ensure.add_argument("--moniker", required=True, help="Feature slug / moniker")
    parser_ensure.add_argument("--timestamp", help="Optional timestamp override")

    # sync-prd subcommand
    parser_sync_prd = subparsers.add_parser("sync-prd", help="Directly parse 02_PRD.md and update visual-dashboard.html with full fidelity")
    parser_sync_prd.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_prd.add_argument("--moniker", default="feature", help="Feature slug / moniker")

    # sync-glossary subcommand
    parser_sync_glossary = subparsers.add_parser("sync-glossary", help="Directly parse docs/glossary.md & docs/adr/ and update visual-dashboard.html with addition flags")
    parser_sync_glossary.add_argument("--plan-dir", required=True, help="Path to plan directory")
    parser_sync_glossary.add_argument("--moniker", default="feature", help="Feature slug / moniker")
    parser_sync_glossary.add_argument("--stage", default="Stage 1", help="Active SDLC stage name for addition badges")

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

    args = parser.parse_args()

    if args.command == "ensure":
        target_dashboard = ensure_dashboard(args.plan_dir, args.moniker, args.timestamp)
        mirror_artifact(target_dashboard)

    elif args.command == "sync-prd":
        sync_prd(args.plan_dir, args.moniker)

    elif args.command == "sync-glossary":
        sync_glossary(args.plan_dir, args.moniker, args.stage)

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
        mirror_artifact(target_dashboard, args.target_filename)


if __name__ == "__main__":
    main()
