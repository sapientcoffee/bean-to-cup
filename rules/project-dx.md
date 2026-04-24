---
trigger: always_on
---

### Workstation Portal DX & Best Practices

- **Walkthroughs**: If your changes are significant, always generate and update `walkthrough.md` to demonstrate proof of thorough testing. Attach this file to any PRs.
- **CLI Tools over GUIs**: When handling git, always prefer using the `gh` CLI over standard `git` commands for raising PRs, following the `github-workflow` skill.
- **Dependency Management**: Platform Engineering means preventing bloat. Think twice, and ask the user for permission, before proposing any new `npm install`.
