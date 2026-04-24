---
trigger: model_decision
---

### Backend Express Guidelines

- **Error Handling**: Every Express route handler MUST be wrapped with our `asyncHandler` pattern to guarantee that any unhandled promise rejections are correctly forwarded to the global Express error middleware.
- **Google Cloud APIs**: The GCP SDK (`@google-cloud/workstations`) can occasionally be slow or rate-limited. Always anticipate these failures, write graceful fallback responses, and return clear HTTP status codes.
- **File Headers**: All new backend source files must include the standard Google Apache 2.0 license header.