# Project NOVA: Architecture Specification

## 1. System Overview
Project NOVA (Neural Operating & Virtual Assistant) utilizes a Hub-and-Device-Agent topology:
- **NOVA Core (Hub)**: Manages intelligence, speech pipeline orchestration, database persistence, risk policy evaluation, and device agent dispatching.
- **NOVA Clients / Agents**: Native agents running on Web, Windows, macOS, Linux, Android, and iOS.

## 2. Risk Policy Model
- **TIER 0 (SAFE)**: Read-only queries, local telemetry, read battery/time/weather. No confirmation required.
- **TIER 1 (REVERSIBLE)**: App launching, volume changes, creating alarms/reminders. Immediate execution with audit logging.
- **TIER 2 (SENSITIVE)**: Outbound communication (SMS, emails, chat), modifying or writing documents. Explicit visual confirmation with recipient and preview.
- **TIER 3 (DANGEROUS)**: File deletion, shell commands, financial transactions. Explicit on-screen confirmation + secondary auth. Voice-only confirmations are strictly prohibited.

## 3. Communication Protocol
Clients maintain a persistent secure WebSocket (WSS) link to the Core Hub:
- Binary frames: Opus audio chunks (STT upstream, TTS downstream)
- JSON frames: Control packets, state transitions, tool execution requests, confirmation flows.

