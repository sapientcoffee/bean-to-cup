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
End-to-End Test Suite for Fully Populated Visual Dashboard.
Generates all Stage 0 to Stage 8 SDLC artifacts and Red-Team Audit reports,
runs manage_dashboard auto-sync, and verifies that every dashboard tab, audit pane,
badge, and metric is 100% populated.
"""

import os
import re
import shutil
import sys
import unittest

def find_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, ".."))

repo_root = find_repo_root()
sys.path.insert(0, os.path.join(repo_root, "skills", "visual-dashboard", "scripts"))

import manage_dashboard


class TestDashboardE2EFullPopulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.plan_dir = os.path.join(repo_root, "plans", "e2e-dashboard-full")
        os.makedirs(cls.plan_dir, exist_ok=True)
        cls.populate_all_stage_artifacts(cls.plan_dir)

    @classmethod
    def populate_all_stage_artifacts(cls, plan_dir):
        """Writes mock stage files for Stage 0 through Stage 8 and Red-Team Audits."""
        
        # Stage 0: 00_IDEATION.md
        with open(os.path.join(plan_dir, "00_IDEATION.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 0: Discovery & Product Ideation

## Problem Statement
Baristas need automated grind size calibration and real-time shot extraction telemetry to guarantee shot consistency.

## Target Personas
- **Coffee Connoisseur**: Demands exact extraction temperature (93.5°C) and particle size distribution.
- **Barista Swarm Operator**: Requires real-time telemetry streaming into Google Cloud Monitoring.

## Customer User Journeys (CUJs)
1. Connoisseur requests calibrated espresso extraction.
2. Swarm Coordinator routes request to Grind Specialist and Telemetry Specialist.
3. Machine executes shot and emits JSON telemetry logs.

## ADK Routing Topology
```mermaid
flowchart TD
  User([User Request]) --> Coordinator{Swarm Coordinator}
  Coordinator -->|Calibrate Particles| GrindSpec[Grind Specialist]
  Coordinator -->|Log Metric| TelemetrySpec[Telemetry Specialist]
  GrindSpec --> Shot[Shot Extraction Complete]
  TelemetrySpec --> Shot
```

## Telemetry Schema
```json
{
  "brew_id": "brew_1001",
  "temperature_celsius": 93.5,
  "extraction_seconds": 26.5,
  "status": "perfect_extraction"
}
```
""")

        # Stage 1: docs/glossary.md & ADR
        adr_dir = os.path.join(repo_root, "docs", "adr")
        os.makedirs(adr_dir, exist_ok=True)
        with open(os.path.join(adr_dir, "0001-use-fastapi-telemetry.md"), "w", encoding="utf-8") as f:
            f.write("""# ADR 0001: Use FastAPI for Shot Extraction Telemetry

## Status
Accepted

## Context
High-frequency extraction telemetry requires async event handling.
""")

        # Stage 2: 02_PRD.md & 02_RED_TEAM_AUDIT.md
        with open(os.path.join(plan_dir, "02_PRD.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 2: Product Requirements Document (PRD)

## Objective
Provide a unified REST API for calibrating shot extractions with strict latency guarantees.

## User Stories
- **As a Barista**, I want to calibrate particle sizes automatically so that shot extractions take exactly 25-28 seconds.
- **As an SRE**, I want Cloud Logging JSON logs so that error budgets are automatically tracked.

## Acceptance Criteria (Gherkin)
```gherkin
Given a calibration request with temperature 93.5C
When the grind specialist receives the payload
Then adjust particle size setting to 4.2
And emit a 200 OK calibration response
```

## Non-Functional Requirements (NFRs)
- **Reliability**: 99.9% uptime SLA.
- **Performance**: Latency < 100ms for calibration API calls.
""")

        with open(os.path.join(plan_dir, "02_RED_TEAM_AUDIT.md"), "w", encoding="utf-8") as f:
            f.write("""# 🛡️ Red-Team Adversarial Audit: Stage 2 PRD

## Executive Summary
- **Risk Level**: HIGH
- **Flaws Identified**: 2

## 🚨 Critical / High Flaws
1. **Unbounded Rate Limit in Calibration API**: High concurrent calibration requests could exhaust memory.
   - **Scenario**: 200 requests/second burst.
   - **Recommendation & Applied Mitigation**: Enforced token-bucket rate limiter (15 req/sec cap) in PRD NFRs.

2. **Unvalidated Temperature Bounds**: Negative or extreme temperatures (>150°C) could trigger machine thermal cut-off.
   - **Scenario**: Payload containing `temperature_celsius: 999.0`.
   - **Recommendation & Applied Mitigation**: Added range validation schema [80°C, 100°C].

## 🔒 Security & Boundary Check
- [x] Authentication & Authorization checked
- [x] Input sanitization specified
- [x] Rate limits and timeout bounds defined
""")

        # Stage 3: 03_EXTRACTION.md
        with open(os.path.join(plan_dir, "03_EXTRACTION.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 3: Context Extraction Report

## Codebase Research Findings
- **Entrypoint**: `press_service/main.py`
- **Dependencies**: FastAPI, Pydantic v2, Cloud Logging SDK
- **Existing Contracts**: `contracts/telemetry_schema.json`
""")

        # Stage 4: 04_SPEC.md & 04_RED_TEAM_AUDIT.md
        with open(os.path.join(plan_dir, "04_SPEC.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 4: Technical Specification

## Technical Outcomes
Deliver a thread-safe calibration service with PostgreSQL schema migrations.

## Component Architecture
```mermaid
architecture-beta
  group api(cloud)[Cloud Infrastructure]
  service router(internet)[FastAPI Router] in api
  service engine(server)[Calibration Engine] in api
  service db(database)[PostgreSQL DB] in api

  router:L -- R:engine
  engine:L -- R:db
```

## API Specification
- `POST /v1/calibration`: Accepts temperature & volume, returns particle setting.
- `GET /v1/telemetry`: Fetches last 50 shot telemetry records.
""")

        with open(os.path.join(plan_dir, "04_RED_TEAM_AUDIT.md"), "w", encoding="utf-8") as f:
            f.write("""# 🛡️ Red-Team Adversarial Audit: Stage 4 Spec

## Executive Summary
- **Risk Level**: MEDIUM
- **Flaws Identified**: 1

## 🚨 Critical / High Flaws
1. **Database Lock Contention under Concurrency**: Concurrent transactions on calibration settings table can cause deadlock.
   - **Scenario**: Simultaneous calibration updates for the same `brew_id`.
   - **Recommendation & Applied Mitigation**: Configured row-level optimistic locking with retry backoff in Spec Section 3.1.

## 🔒 Security & Boundary Check
- [x] Database lock safety verified
- [x] Connection pooling bounds specified
""")

        # Stage 5: 05_PLAN.md & 05_RED_TEAM_AUDIT.md
        with open(os.path.join(plan_dir, "05_PLAN.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 5: Execution Plan

## Implementation Slices
- [x] **Slice 1 (Parallel)**: Setup Pydantic calibration model and schemas.
- [x] **Slice 2 (Serial)**: Implement FastAPI calibration endpoint router.
- [x] **Slice 3 (Parallel)**: Integrate Cloud Logging telemetry exporter.
- [x] **Slice 4 (Serial)**: Execute end-to-end integration test suite.
""")

        with open(os.path.join(plan_dir, "05_RED_TEAM_AUDIT.md"), "w", encoding="utf-8") as f:
            f.write("""# 🛡️ Red-Team Adversarial Audit: Stage 5 Execution Plan

## Executive Summary
- **Risk Level**: LOW
- **Flaws Identified**: 0

## 🚨 Critical / High Flaws
None. All race condition risks addressed in TDD verification checklist.

## 🔒 Security & Boundary Check
- [x] TDD verification harness specified for every slice
- [x] Parallel vs Serial execution lanes verified
""")

        # Stage 7: 07_VERIFICATION.md
        with open(os.path.join(plan_dir, "07_VERIFICATION.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 7: TDD Implementation & Verification

## Verification Summary
- **Total Tests**: 12
- **Passed**: 12
- **Coverage**: 98.5%

## Verification Log
```text
tests/test_calibration.py::test_valid_calibration PASSED
tests/test_calibration.py::test_rate_limiting PASSED
tests/test_telemetry.py::test_json_format PASSED
```
""")

        # Stage 8: 08_WALKTHROUGH.md
        with open(os.path.join(plan_dir, "08_WALKTHROUGH.md"), "w", encoding="utf-8") as f:
            f.write("""# Stage 8: Verification Walkthrough & Recap

## Executive Summary
Feature implementation complete and fully verified. All 4 TDD slices executed cleanly.

## Key Changes
- Created `press_service/calibration.py` router
- Implemented Pydantic calibration validation
- Added token bucket rate limiter middleware

## Empirical Proof
- Unit & Contract test suite passed (12/12)
- Zero lint errors reported
""")

    def test_auto_sync_fully_populates_dashboard(self):
        """Runs auto_sync and asserts that every single tab section marker & audit pane is populated."""
        manage_dashboard.auto_sync(self.plan_dir, moniker="e2e-dashboard-full")

        dash_path = os.path.join(self.plan_dir, "visual-dashboard.html")
        self.assertTrue(os.path.exists(dash_path), "visual-dashboard.html was not generated")

        with open(dash_path, "r", encoding="utf-8") as f:
            html = f.read()

        # 1. Assert all stage badges are marked Complete
        for stage_num in range(6):
            self.assertIn(f'id="badge-stage-{stage_num}">🟢 Complete', html, f"Stage {stage_num} badge not marked Complete")
        self.assertIn('id="badge-stage-7">🟢 Complete', html, "Stage 7 badge not marked Complete")
        self.assertIn('id="badge-stage-8">🟢 Complete', html, "Stage 8 badge not marked Complete")

        # 2. Assert metrics calculation (100% complete slices)
        self.assertIn('id="mainProgressText">100%</div>', html)
        self.assertIn('id="completedTasksText">4 / 4</div>', html)
        self.assertIn('id="currentStageBadge">Stage 8</div>', html)

        # 3. Assert Section Markers contain populated content
        self.assertIn("Baristas need automated grind size calibration", html)  # Stage 0 Discovery
        self.assertIn("ADR 0001: Use FastAPI for Shot Extraction Telemetry", html)  # Stage 1 ADRs
        self.assertIn("Provide a unified REST API for calibrating shot extractions", html)  # Stage 2 PRD
        self.assertIn("Entrypoint**: `press_service/main.py`", html)  # Stage 3 Extraction
        self.assertIn("Deliver a thread-safe calibration service", html)  # Stage 4 Spec
        self.assertIn("Implementation Slices", html)  # Stage 5 Plan
        self.assertIn("Verification Summary", html)  # Stage 7 Verification
        self.assertIn("Feature implementation complete and fully verified", html)  # Stage 8 Recap

        # 4. Assert Red-Team Audit & Mitigation Panes
        self.assertIn("🛡️ Adversarial Red-Team Audit &amp; Mitigations", html)
        self.assertIn("File: <code>02_RED_TEAM_AUDIT.md</code>", html)
        self.assertIn("Unbounded Rate Limit in Calibration API", html)
        self.assertIn("Enforced token-bucket rate limiter", html)
        self.assertIn("File: <code>04_RED_TEAM_AUDIT.md</code>", html)
        self.assertIn("Database Lock Contention under Concurrency", html)


if __name__ == "__main__":
    unittest.main()
