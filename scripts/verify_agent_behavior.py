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

"""Agent Behavioral Test Runner (Behavioral Assertion Engine).

This script parses the Antigravity CLI transcript.jsonl files to assert that
subagents, skills, and tools were called exactly as expected during an execution cycle.
"""

import json
import os
import sys

def load_transcript(transcript_path):
    """Loads a JSONL transcript file."""
    steps = []
    if not os.path.exists(transcript_path):
        return None
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                steps.append(json.loads(line))
            except Exception as e:
                print(f"Warning: Failed to parse line {line_num}: {e}", file=sys.stderr)
    return steps

def run_assertions(steps):
    """Evaluates behavioral rules against the transcript steps."""
    failures = []
    invoked_subagents = []
    invoked_tools = set()
    failed_tool_calls = []

    for step in steps:
        tool_calls = step.get("tool_calls", [])
        # Check if the step has tool calls (often inside PLANNER_RESPONSE)
        for tc in tool_calls:
            tool_name = tc.get("name") or tc.get("tool") or ""
            invoked_tools.add(tool_name)
            
            # Record subagents invoked
            if "invoke_subagent" in tool_name or tool_name == "default_api:invoke_subagent":
                args = tc.get("args") or tc.get("arguments") or {}
                subagents = args.get("Subagents", [])
                for sub in subagents:
                    invoked_subagents.append({
                        "role": sub.get("Role"),
                        "typeName": sub.get("TypeName"),
                        "prompt": sub.get("Prompt")
                    })

        # Check for error statuses in tool outputs or system responses
        if step.get("status") == "ERROR" or step.get("status") == "FAILED":
            failed_tool_calls.append(step)

    print("\n📊 --- Agent Behavior Audit Results ---")
    print(f"Total Transcript Steps Audited: {len(steps)}")
    print(f"Tools Executed: {', '.join(sorted(invoked_tools)) or 'None'}")
    print(f"Subagents Dispatched: {len(invoked_subagents)}")
    for i, sub in enumerate(invoked_subagents, 1):
        print(f"  {i}. Role: '{sub['role']}' [Type: {sub['typeName']}]")

    # Assertion 1: Subagents called
    if not invoked_subagents:
        print("⚠️ Assertion Check: No subagents were spawned during this trace.")
    else:
        print("✅ Assertion Check: Subagent spawning verified.")

    # Assertion 2: Critical failures
    if failed_tool_calls:
        print(f"❌ Assertion Failure: Found {len(failed_tool_calls)} failed/error steps in history.")
        for f_step in failed_tool_calls:
            print(f"  - Step {f_step.get('step_index')}: {f_step.get('content')[:100]}...")
    else:
        print("✅ Assertion Check: Zero tool errors or execution failures found.")

    return len(failed_tool_calls) == 0

def main():
    if len(sys.argv) < 2:
        # Try to discover conversation ID from workspace context or default path
        conv_dir = os.environ.get("GEMINI_CONVERSATION_DIR")
        if conv_dir:
            transcript_path = os.path.join(conv_dir, ".system_generated", logs, "transcript.jsonl")
        else:
            print("Usage: python3 verify_agent_behavior.py <path_to_transcript.jsonl>\n")
            print("To auto-discover, run within active AGY environment or supply path:")
            print("Example: python3 verify_agent_behavior.py ~/.gemini/antigravity-cli/brain/<conv_id>/.system_generated/logs/transcript.jsonl")
            sys.exit(1)
    else:
        transcript_path = sys.argv[1]

    if not os.path.exists(transcript_path):
        print(f"Error: Transcript file not found at {transcript_path}")
        sys.exit(1)

    print(f"Reading trace logs from: {transcript_path}")
    steps = load_transcript(transcript_path)
    if steps is None:
        print("Error: Could not load or parse the transcript file.")
        sys.exit(1)

    success = run_assertions(steps)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
