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

"""Stage-Specific Test Orchestrator & Bootstrapper.

This script automates seeding, isolation sandbox setup, and output validation 
for individual SDLC stages (Stages 0 to 9) to facilitate rapid stage-in-isolation testing.
"""

import argparse
import os
import sys

# Define stages and their required inputs / outputs
STAGE_CONFIGS = {
    "2": {
        "name": "PRD Generation (Stage 2)",
        "inputs": ["01_GLOSSARY.md"],
        "outputs": ["02_PRD.md"],
        "default_mock_inputs": {
            "01_GLOSSARY.md": "# Ubiquitous Glossary: Coffee Queue\n\n## Barista Queue\nAn ordered registry of active coffee requests.\n"
        }
    },
    "3": {
        "name": "Context Extraction / Research (Stage 3)",
        "inputs": ["02_PRD.md"],
        "outputs": ["03_EXTRACTION.md"],
        "default_mock_inputs": {
            "02_PRD.md": "# Product Requirements Document: Coffee Queue\n\n## Problem Statement\nWe need to track queue count.\n\n## In-Scope\n- GET /api/queue retrieves count.\n"
        }
    },
    "4": {
        "name": "Technical Specification (Stage 4)",
        "inputs": ["02_PRD.md", "03_EXTRACTION.md"],
        "outputs": ["04_SPEC.md"],
        "default_mock_inputs": {
            "02_PRD.md": "# Product Requirements Document: Coffee Queue\n## Problem Statement\nWe need to track queue count.\n",
            "03_EXTRACTION.md": "# Technical Extraction: Factual Code Map\n## Existing Endpoints\n- `server.js:10` registers GET /api/health\n"
        }
    },
    "5": {
        "name": "Execution Planning (Stage 5)",
        "inputs": ["04_SPEC.md"],
        "outputs": ["05_PLAN.md"],
        "default_mock_inputs": {
            "04_SPEC.md": "# Technical Specification: Coffee Queue\n## Contracts\n- GET /api/queue -> returns { \"count\": int }\n"
        }
    },
    "7": {
        "name": "TDD Implementation (Stage 7)",
        "inputs": ["04_SPEC.md", "05_PLAN.md"],
        "outputs": ["07_VERIFICATION.md"],
        "default_mock_inputs": {
            "04_SPEC.md": "# Technical Specification: Coffee Queue\n## Contracts\n- GET /api/queue -> returns { \"count\": int }\n",
            "05_PLAN.md": "# Implementation Plan\n- [ ] Task 1: Write mock endpoint\n- [ ] Task 2: Validate API tests\n"
        }
    },
    "8": {
        "name": "Walkthrough Evidence (Stage 8)",
        "inputs": ["07_VERIFICATION.md"],
        "outputs": ["08_WALKTHROUGH.md"],
        "default_mock_inputs": {
            "07_VERIFICATION.md": "# Verification Report: Coffee Queue\nAll backend endpoints green.\n"
        }
    }
}

def setup_sandbox(sandbox_path, stage_key, feature_slug):
    """Prepares the sandbox directory with mock input assets for the target stage."""
    config = STAGE_CONFIGS.get(stage_key)
    if not config:
        print(f"Error: Stage '{stage_key}' config not found.")
        sys.exit(1)

    print(f"\n🧱 Bootstrapping Sandbox for: {config['name']}")
    
    # Establish plan paths
    plan_dir = os.path.join(sandbox_path, "plans", "feature", feature_slug, "test-run")
    os.makedirs(plan_dir, exist_ok=True)
    
    # Run simple git init if not present
    if not os.path.exists(os.path.join(sandbox_path, ".git")):
        print("  - Initializing git repository in sandbox...")
        os.system(f"git init -b main {sandbox_path} >/dev/null 2>&1")

    # Seed Mock Inputs
    print("📋 Seeding Mock Input Artifacts:")
    for filename, content in config["default_mock_inputs"].items():
        filepath = os.path.join(plan_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Created Mock Input: {filename} -> {filepath}")

    print("\n🚀 Ready to run the stage test inside your sandbox!")
    print("----------------------------------------------------------------------")
    print(f"1. Navigate to: {sandbox_path}")
    print("2. Open the Antigravity TUI ('agy') or agent prompt and run:")
    
    if stage_key == "2":
        print(f"   > \"Please read the Socratic glossary in {plan_dir}/01_GLOSSARY.md and compile the PRD 02_PRD.md in that directory.\"")
    elif stage_key == "3":
        print(f"   > \"Please run context-free research on {plan_dir}/02_PRD.md and compile the 03_EXTRACTION.md facts.\"")
    elif stage_key == "4":
        print(f"   > \"Please dispatch @architect to design 04_SPEC.md from {plan_dir}/02_PRD.md and {plan_dir}/03_EXTRACTION.md.\"")
    elif stage_key == "5":
        print(f"   > \"Please dispatch @architect to generate the 05_PLAN.md checklist from {plan_dir}/04_SPEC.md.\"")
    elif stage_key == "7":
        print(f"   > \"Please dispatch @engineer to execute the implementation checklist from {plan_dir}/05_PLAN.md.\"")
    elif stage_key == "8":
        print(f"   > \"Please run the automated walkthrough and record terminal evidence inside {plan_dir}/08_WALKTHROUGH.md.\"")
    print("----------------------------------------------------------------------")

def validate_outputs(sandbox_path, stage_key, feature_slug):
    """Checks if the target stage's outputs have been successfully written."""
    config = STAGE_CONFIGS.get(stage_key)
    if not config:
        return

    plan_dir = os.path.join(sandbox_path, "plans", "feature", feature_slug, "test-run")
    print(f"\n🔍 Validating Outputs for: {config['name']}")
    
    all_present = True
    for out_file in config["outputs"]:
        filepath = os.path.join(plan_dir, out_file)
        if os.path.exists(filepath):
            print(f"  ✅ Found Output Artifact: {out_file} (Success)")
        else:
            print(f"  ❌ Missing Expected Output Artifact: {out_file}")
            all_present = False

    if all_present:
        print("🎉 Stage Isolation Test Succeeded! Output artifacts verified.")
    else:
        print("⚠️ Stage Isolation Test Failed or Pending execution.")

def main():
    parser = argparse.ArgumentParser(description="Bean-to-Cup Stage-Specific Isolated Testing Harness.")
    parser.add_argument("--stage", required=True, choices=list(STAGE_CONFIGS.keys()), help="Target stage key to test.")
    parser.add_argument("--sandbox", default="scratch/sandbox-app", help="Path to your target testing sandbox.")
    parser.add_argument("--feature", default="test-feature", help="Feature name slug for mock plan folders.")
    parser.add_argument("--validate", action="store_true", help="Validate output artifacts after a run.")

    args = parser.parse_args()

    sandbox_path = os.path.abspath(args.sandbox)

    if args.validate:
        validate_outputs(sandbox_path, args.stage, args.feature)
    else:
        setup_sandbox(sandbox_path, args.stage, args.feature)

if __name__ == "__main__":
    main()
