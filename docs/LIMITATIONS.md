# Project NOVA: Platform Limitations & Boundary Constraints

## Web
- Audio capture strictly requires HTTPS or localhost context and explicit user permission.
- Wake-word detection is constrained to active tab life cycle.
- Sandboxed environment prohibits direct local OS execution or unauthorized filesystem access.

## Android
- Continuous background microphone capture requires an active foreground service with notification.
- Deep application automation relies on Intent resolution and public APIs.
- Optional AccessibilityService must be transparently disclosed to users.

## iOS
- Background microphone listening is restricted by iOS security model.
- Interaction relies on foreground sessions, App Intents, URL Schemes, and system Shortcuts.
- System-wide unrestricted process control is unavailable by platform design.

## Desktop (Windows, macOS, Linux)
- macOS requires user-granted Screen Recording and Accessibility permissions for window and screenshot automation.
- Linux automation must negotiate differences between Wayland and X11 display servers.
- Shell commands operate under an allowlist policy with input sanitization; arbitrary string shell evaluation is blocked.

