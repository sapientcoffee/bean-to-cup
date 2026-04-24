# Developer Rules and Guidelines

Welcome to the Workstation Portal project! As a Platform Engineer, our goal is to eliminate friction and provide an excellent developer experience (DX). Please adhere to these rules when working on this project:

## 1. Code Quality & Formatting
*   **ES Modules:** This project uses ECMAScript Modules (`"type": "module"` in `package.json`). Ensure all new Node.js files use `.mjs` or ES6 `import`/`export` syntax.
*   **Linting:** Run `npm run lint` before finalizing any PR or workflow. Code must be clean and free of ESLint warnings.
*   **License Headers:** All new source code files MUST include the appropriate Google Apache 2.0 license header. Use the `google-license-manager` skill to automatically append these headers when creating new files.

## 2. Frontend Development (React & Vite)
*   **Vite First:** We use Vite for lightning-fast HMR. Do not introduce Webpack or other bundlers.
*   **No Heavy Dependencies:** Avoid adding large third-party libraries unless absolutely necessary. Keep the bundle size small.
*   **UX/UI Excellence:** As a user-facing portal, aesthetics are highly important. Ensure elements are responsive, accessible, and visually aligned with Google/modern design standards (using `lucide-react` for icons).

## 3. Backend Development (Express)
*   **Error Handling:** Always use the `asyncHandler` pattern for Express routes to ensure caught promise rejections are passed to the global error handler.
*   **Graceful Degradation:** The GCP SDK (`@google-cloud/workstations`) can sometimes be slow or rate-limited. Architect APIs to fail gracefully and return clear, actionable error messages to the frontend.

## 4. Git & GitHub Workflow
*   **Clear Commits:** Use the `github-workflow` skill to ensure commits are well-documented, atomic, and PRs are cleanly structured with testing walkthroughs.
*   **Walkthroughs:** Any significant feature addition should include an Antigravity walkthrough (`walkthrough.md`) attached to the pull request to demonstrate testing and validation.
