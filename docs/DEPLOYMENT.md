# Project NOVA: Production Deployment & Verification Guide

## 1. Production Docker Images

### Core Backend Hub
```dockerfile
# services/core/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Next.js Web Dashboard
```dockerfile
# apps/web/Dockerfile
FROM node:22-alpine AS runner
WORKDIR /app
COPY package.json pnpm-workspace.yaml turbo.json ./
COPY apps/web ./apps/web
COPY packages ./packages
RUN npm install -g pnpm && pnpm install --frozen-lockfile && pnpm --filter @nova/web build
EXPOSE 3000
CMD ["pnpm", "--filter", "@nova/web", "start"]
```

---

## 2. Security & Compliance Checklist
- [x] Zero API keys or secrets exposed to client-side frontend.
- [x] Strict 4-Tier Risk Engine: Tier 3 actions require on-screen confirmation and secondary auth. Voice-only confirmations are rejected.
- [x] Local on-device Emergency Stop ("NOVA STOP") executes with zero LLM latency.
- [x] Device revocation instantly revokes access across the device mesh.
- [x] Allowlisted desktop executables: no arbitrary string shell commands.
- [x] User-approved memory storage with edit and delete capabilities.

---

## 3. Platform Distribution
- **Windows / macOS / Linux**: Tauri bundler produces native `.msi`, `.dmg`, or `.AppImage` packages.
- **Android**: `cd apps/mobile && npx expo run:android --variant release`
- **iOS**: `cd apps/mobile && npx expo run:ios --configuration Release`

