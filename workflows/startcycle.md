---
description: Start the Automated Development Pipeline sequence with a new idea
---

When the user types `/startcycle <idea>`, orchestrate the development process strictly using the defined pipeline stages and capabilities.

### Execution Sequence:
1. Execute the **Requirements Definition** stage (using the `write-specs` skill) with the `<idea>`.
   *(Wait for the user to explicitly approve the spec. If the user provides feedback or adds comments directly to the Markdown file, re-run this stage to revise the document. Loop this step until they type "Approved").*
2. Execute the **Implementation Pipeline** stage (using the `generate-code` skill).
3. Execute the **Quality Gate** stage (using the `audit-code` skill).
4. Execute the **Deployment Automation** stage (using the `deploy-app` skill).
