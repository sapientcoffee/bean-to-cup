# Contributing to Bean to Cup

First off, thank you for considering contributing to the Bean to Cup portal! 

## Code of Conduct

By participating in this project, you agree to abide by the standard Google Open Source [Code of Conduct](https://opensource.google/conduct/).

## Our Goals

Bean to Cup is designed to eliminate friction and provide an excellent developer experience (DX). We value:
- **Simplicity:** Keep solutions focused and lean.
- **Aesthetics:** User-facing components should be modern, polished, and responsive.
- **Reliability:** Handle errors gracefully, especially when interacting with cloud APIs.

## How Can I Contribute?

### Pull Requests
1. **Fork the repo** and create your branch from `main`.
2. **License Headers:** All new source files MUST include the Google Apache 2.0 license header. Use the `google-license-manager` skill to automate this.
3. **Project Standards:**
    - Use **ES Modules** (import/export syntax).
    - Use **Vite** for frontend development.
    - Use **lucide-react** for icons.
    - Always wrap Express route handlers in an `asyncHandler` pattern.
4. **Linting:** Run `npm run lint` before submitting your PR.
5. **Testing:** Any significant feature addition should include a walkthrough demonstrating validation.

## Technical Guidelines

For detailed technical standards, please refer to the rules in the repository:
- `rules/general.md`
- `rules/backend-guidelines.md`
- `rules/frontend-guidelines.md`

## License

By contributing to this project, you agree that your contributions will be licensed under its [Apache 2.0 License](LICENSE).
