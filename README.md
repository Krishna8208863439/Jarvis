# PROJECT NOVA
## Universal Personal AI Voice Assistant
**Neural Operating & Virtual Assistant**

NOVA is a secure, voice-first, cross-platform personal AI assistant inspired by JARVIS, designed to execute real device actions across Android, iOS, Windows, macOS, Linux, and Web via a Hub-and-Device-Agent architecture.

---

## 🏛 Architecture Overview

```
                                +---------------------------+
                                |      NOVA CORE HUB        |
                                | (FastAPI / PyTorch / LLM) |
                                +-------------+-------------+
                                              |
                   +--------------------------+--------------------------+
                   | (WSS / TLS)              | (WSS / TLS)              | (WSS / TLS)
                   v                          v                          v
      +-------------------------+   +-------------------+   +-------------------------+
      |      Web Client         |   |  Desktop Client   |   |      Mobile Client      |
      |   (Next.js / Zustand)   |   |   (Tauri / Rust)  |   |   (React Native/Expo)   |
      +-------------------------+   +-------------------+   +-------------------------+
```

---

## 📦 Monorepo Structure

```
nova/
├── apps/
│   ├── web/               # Next.js 14 web client (Orb, Dashboard, Live STT/TTS)
│   ├── desktop/           # Tauri desktop client with native system hooks
│   └── mobile/            # React Native / Expo development build client
├── services/
│   └── core/              # Python FastAPI Hub (Brain, Memory, Tools, Policies, DB)
├── packages/
│   ├── ui/                # Shared UI design system & components
│   ├── protocol/          # Shared TypeScript & Python message schemas & risk types
│   └── voice-client/      # Client-side audio processing (VAD, Opus streaming)
├── docs/                  # Architecture, Permissions, Limitations & API specs
├── docker-compose.yml     # Local orchestration (Core + PostgreSQL)
├── pnpm-workspace.yaml    # Workspace definition
└── turbo.json             # Turborepo build pipeline
```

---

## 🚀 Getting Started (Phase 0)

### Prerequisites
- Node.js >= 20.x
- Python >= 3.11
- pnpm >= 9.x
- Docker & Docker Compose (optional for local DB)

### Quick Start
1. Install dependencies:
   ```bash
   pnpm install
   ```
2. Start local PostgreSQL and services:
   ```bash
   docker-compose up -d
   ```
3. Start Core API:
   ```bash
   cd services/core
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
4. Start Web Client:
   ```bash
   pnpm --filter @nova/web dev
   ```

Visit `http://localhost:3000` for Web Dashboard and `http://localhost:8000/health` for Backend Health status.

