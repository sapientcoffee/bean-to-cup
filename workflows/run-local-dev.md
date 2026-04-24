---
description: Start the local development environment
---
This workflow starts both the backend Express server and the frontend Vite development server.

1. Install dependencies if necessary.
// turbo
npm install

2. Start the backend server in the background. Note: this runs on port 3001 by default.
// turbo
node server.js &

3. Start the Vite frontend development server.
// turbo
npm run dev
