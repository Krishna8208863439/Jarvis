# QA Platform Compatibility Matrix: Project NOVA

| Target Platform | Compatibility Level | Supported Capabilities | Documented Limitations |
|---|---|---|---|
| **Windows 11 (Host)** | **FULLY_SUPPORTED** | App discovery via `winreg`/Start Menu, native process execution, window focus & restoration (`pygetwindow`), non-blind typing (`pyautogui`), Office generation (`.docx`, `.pptx`, `.xlsx`), YouTube direct autoplay. | Windows desktop permissions required for system utility launching. |
| **Web Browser (Chrome/Edge/Firefox)** | **FULLY_SUPPORTED** | Web Speech API speech-to-text, neural speech synthesis, Web Audio API frequency visualizer, real-time transcript streaming, approval modals. | Web Speech API requires user microphone permission grant. |
| **Android (Mobile Mesh)** | **PARTIAL (Scaffolding)** | Intent payload synthesis (`android.intent.action.VIEW`), WhatsApp URI dispatch, mobile telemetry models. | Full background wake-word requires native Android Foreground Service. |
| **iOS / iPadOS (Mobile Mesh)**| **PARTIAL (Scaffolding)** | Universal Link and URL scheme payload synthesis. | System sandboxing prevents background OS-level UI automation. |
| **Linux / macOS** | **CROSS-PLATFORM BASE** | Python FastAPI core, ReAct reasoning engine, browser research, file generation. | Window automation currently targets Win32 API (`pygetwindow`). |

