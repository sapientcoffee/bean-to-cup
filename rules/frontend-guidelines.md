---
trigger: model_decision
---

### Frontend React & Vite Guidelines

- **Icons**: Always prefer `lucide-react` for adding new icons. Do not pull in other icon libraries.
- **Environment Variables**: We use Vite. Access environment variables using `import.meta.env`, NOT `process.env`.
- **Components**: Write functional components using modern React Hooks. Keep components small, modular, and focused on a single responsibility.
- **Styling**: Ensure components are responsive and adhere to existing design aesthetics. We value high-quality, modern UX without relying on bloated libraries.