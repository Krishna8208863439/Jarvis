# QA Known Limitations: Project NOVA

## 1. Operating System Boundaries
- **Windows UI Automation**: Non-blind typing relies on foreground window activation via Win32 `pygetwindow`. If the target application is running with elevated Administrator privileges, standard non-elevated Python processes cannot inject keystrokes into it due to Windows UIPI (User Interface Privilege Isolation).
- **macOS / Linux**: Window inspection currently uses Windows-specific APIs. Cross-platform execution falls back to process spawning and web browser automation.

## 2. Browser Sandbox Boundaries
- **Web Speech API**: In Chrome and Edge, speech recognition terminates after periods of silence by browser design. NOVA mitigates this with an automated 200ms auto-restart watchdog (`shouldKeepListening`), but browser permission must remain granted in the URL bar.
- **Microphone Permissions**: If microphone access is denied in the browser settings, voice input transitions gracefully to the `ERROR` state with user-facing recovery instructions.

## 3. Mobile Device Mesh
- **Background Wake Word on Mobile**: Native Android and iOS security policies suspend background microphone listening unless running an explicit native Foreground Service with a persistent notification. Mobile mesh operations currently use push-triggered Intent routing.

