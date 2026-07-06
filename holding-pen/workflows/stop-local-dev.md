---
description: Stop local development server instances
---
This workflow forcefully stops the Vite development server and the backend Express server that were started in the background.

1. Stop the backend Node.js server.
// turbo
pkill -f "node server.js" || echo "Backend server not running"

2. Stop the frontend Vite server.
// turbo
pkill -f "vite" || echo "Frontend server not running"

3. Optionally, as a fallback, ensure the backend port (3001) is cleared.
// turbo
fuser -k 3001/tcp || echo "Port 3001 is already clear"
