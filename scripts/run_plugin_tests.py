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
Central Test Orchestrator for Bean-to-Cup Plugin.
Runs Tier 1 (Schema), Tier 2 (Unit), and Tier 3 (Headless E2E Workflow) test suites.
"""

import argparse
import os
import sys
import unittest


def find_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, ".."))


def main():
    parser = argparse.ArgumentParser(description="Bean-to-Cup Plugin Test Runner.")
    parser.add_argument(
        "--tier",
        choices=["1", "2", "3", "all"],
        default="all",
        help="Specific test tier to run (1: Schema, 2: Unit, 3: Headless E2E, all: All Tiers)."
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run fast pre-commit checks (Tiers 1 & 2 only)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose test output."
    )

    args = parser.parse_args()
    repo_root = find_repo_root()
    tests_dir = os.path.join(repo_root, "tests")

    if not os.path.exists(tests_dir):
        print(f"Error: Tests directory not found at {tests_dir}", file=sys.stderr)
        sys.exit(1)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if args.fast:
        print("⚡ Running Fast Pre-Commit Validation Suite (Tiers 1 & 2)...")
        suite.addTests(loader.discover(tests_dir, pattern="test_skills_schema.py"))
        suite.addTests(loader.discover(tests_dir, pattern="test_hooks_and_scripts.py"))
        suite.addTests(loader.discover(tests_dir, pattern="test_manage_dashboard.py"))
    elif args.tier == "1":
        print("🔍 Running Tier 1: Static Schema & Frontmatter Validation...")
        suite.addTests(loader.discover(tests_dir, pattern="test_skills_schema.py"))
        suite.addTests(loader.discover(tests_dir, pattern="test_hooks_and_scripts.py"))
    elif args.tier == "2":
        print("🧪 Running Tier 2: Functional Unit Tests...")
        suite.addTests(loader.discover(tests_dir, pattern="test_manage_dashboard.py"))
    elif args.tier == "3":
        print("🤖 Running Tier 3: SDLC Headless E2E Workflow Harness...")
        suite.addTests(loader.discover(tests_dir, pattern="test_sdlc_headless_e2e.py"))
    else:
        print("☕ Running Complete Plugin Test Suite (Tiers 1, 2, and 3)...")
        suite.addTests(loader.discover(tests_dir, pattern="test_*.py"))

    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
