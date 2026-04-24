---
description: Run local backend API validation scripts
---
This workflow executes the local `.mjs` scripts designed to validate the integration with the Google Cloud Workstations API. Ensure that Application Default Credentials (ADC) are configured.

1. Run the initial API client tests.
// turbo
node test_api.mjs

2. Run secondary API validation.
// turbo
node test_api2.mjs

3. Run Workstations-specific tests.
// turbo
node test_ws.mjs

4. Run wildcard list validation.
// turbo
node test_wildcard.mjs
