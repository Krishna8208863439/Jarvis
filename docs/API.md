# Project NOVA: API Reference

## Health & Status
- `GET /health`
  - Response: `{"status": "healthy", "service": "NOVA Core Hub", "timestamp": "...", "version": "0.1.0"}`
- `GET /api/v1/system/status`
  - Returns device mesh connection count, active sessions, and database status.

## Real-time WebSocket Protocol
- `WS /ws`
  - Upstream audio streaming & downstream TTS playback.
  - Device agent RPC and execution coordination.

