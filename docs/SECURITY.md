# Project NOVA: Security & Privacy Specification

## Core Principles
1. **Zero Secret Leakage**: AI provider keys (OpenAI, Anthropic) and TTS/STT provider credentials are strictly isolated to the server-side Core Hub.
2. **Audio Data Privacy**:
   - Audio is streamed ephemerally for processing; raw audio waveforms are never permanently retained unless the user explicitly enables debug logging.
   - Visible visual indicators are mandatory whenever the microphone is active.
3. **Emergency Disarm**: Local "NOVA STOP" trigger interrupts playback and cancels running task queues immediately without round-tripping to LLM.
4. **Prompt Injection Defense**:
   - Untrusted sources (retrieved web data, emails, third-party docs) are encapsulated as untrusted payload strings.
   - LLM cannot execute tools directly based on content text without intent corroboration and policy checks.

