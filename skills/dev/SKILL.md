---
name: dev
description: Start the local development environment (backend and frontend)
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

# Local Development Skill

This skill spins up and manages the local developer server environment for both the backend API server and frontend static client application.

## 1. Objective
To automate the launch and continuous running of development servers, ensuring dependencies are resolved and providing active localhost URLs for easy browser-based verification.

## 2. Workflow Steps

1. **Install Dependencies**:
   - Execute `npm install` to update and resolve any outdated or missing packages.

2. **Launch Backend Server**:
   - Start the backend Express API server using `node server.js`.
   - **CRITICAL**: Launch this as a background process (`is_background = true` / detached process) so that execution is not blocked.
   - Note: The backend server defaults to running on port `3001`.

3. **Launch Frontend Client**:
   - Start the Vite development server using `npm run dev`.
   - **CRITICAL**: Launch this as a background process (`is_background = true` / detached process) so that execution is not blocked.
   - Note: Vite typically defaults to running on port `5173`.

4. **Verify Active Processes**:
   - Confirm that both background servers have successfully started and are listening on their respective ports.
   - Provide the active localhost URLs to the user or subsequent browser automation agents.

## 3. Configuration & Ports
*   **Backend Server**: Port `3001` (http://localhost:3001)
*   **Frontend Client**: Port `5173` (http://localhost:5173)

## 4. Execution Example
Run the development stack:
```bash
agy dev
```
