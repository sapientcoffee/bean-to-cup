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
Visual Dashboard Lifecycle Manager Unit Test Suite.
Tests ensure_dashboard, update_section, auto_sync, and artifact mirroring.
"""

import os
import shutil
import sys
import tempfile
import unittest

def find_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, ".."))

repo_root = find_repo_root()
sys.path.insert(0, os.path.join(repo_root, "skills", "visual-dashboard", "scripts"))

import manage_dashboard


class TestManageDashboard(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="dashboard_test_")
        self.plan_dir = os.path.join(self.temp_dir, "plans", "feature", "test-feature")
        os.makedirs(self.plan_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ensure_dashboard_creates_file(self):
        dash_path = manage_dashboard.ensure_dashboard(self.plan_dir, "test-feature", timestamp="2026-08-05 12:00")
        self.assertTrue(os.path.exists(dash_path))

        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("test-feature", content)
        self.assertIn("2026-08-05 12:00", content)

    def test_update_section_replaces_content(self):
        dash_path = manage_dashboard.ensure_dashboard(self.plan_dir, "test-feature")
        section = "VP:OVERVIEW"
        new_html = "<div class='custom-test-card'>UnitTest Card</div>"

        manage_dashboard.update_section(dash_path, section, new_html)

        with open(dash_path, "r", encoding="utf-8") as f:
            updated_content = f.read()

        self.assertIn(new_html, updated_content)
        self.assertIn(f"<!-- {section} -->", updated_content)
        self.assertIn(f"<!-- /{section} -->", updated_content)

    def test_auto_sync_scans_and_updates_badges(self):
        # Create mock stage files
        with open(os.path.join(self.plan_dir, "00_IDEATION.md"), "w", encoding="utf-8") as f:
            f.write("# Ideation Phase\n## Problem\nNeed a test counter.")

        with open(os.path.join(self.plan_dir, "02_PRD.md"), "w", encoding="utf-8") as f:
            f.write("# Product Requirements Document\n## Objective\nBuild a test counter.")

        with open(os.path.join(self.plan_dir, "05_PLAN.md"), "w", encoding="utf-8") as f:
            f.write("# Execution Plan\n## Overview\nTest plan slice.")

        brain_dir = os.path.join(self.temp_dir, "mock_brain")
        os.makedirs(brain_dir, exist_ok=True)

        manage_dashboard.auto_sync(self.plan_dir, moniker="test-feature", brain_dir=brain_dir)

        dash_path = os.path.join(self.plan_dir, "visual-dashboard.html")
        self.assertTrue(os.path.exists(dash_path))

        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check badges for completed stages
        self.assertIn('id="badge-stage-0">🟢 Complete', content)
        self.assertIn('id="badge-stage-2">🟢 Complete', content)
        self.assertIn('id="badge-stage-5">🟢 Complete', content)

        # Check artifact mirroring in mock_brain
        mirrored_dash = os.path.join(brain_dir, "00_visual-dashboard.html")
        mirrored_prd = os.path.join(brain_dir, "02_prd.md")
        mirrored_plan = os.path.join(brain_dir, "05_plan.md")

        self.assertTrue(os.path.exists(mirrored_dash), "Mirrored dashboard file missing in brain directory")
        self.assertTrue(os.path.exists(mirrored_prd), "Mirrored PRD file missing in brain directory")
        self.assertTrue(os.path.exists(mirrored_plan), "Mirrored Plan file missing in brain directory")


if __name__ == "__main__":
    unittest.main()
