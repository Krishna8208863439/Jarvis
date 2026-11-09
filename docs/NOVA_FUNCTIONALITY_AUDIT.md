# PROJECT NOVA – UNIVERSAL OPERATOR ARCHITECTURAL AUDIT & ROADMAP

**Version:** 2.0-Universal  
**System Role:** Universal AI Computer & Mobile Operator  
**Core Directive:** SPEAK → UNDERSTAND → PLAN → ACCESS → EXECUTE → VERIFY → COMPLETE

---

## 1. EXECUTIVE SUMMARY & CODEBASE INVENTORY

A comprehensive audit of the Project NOVA codebase (`services/core`, `apps/web`, `apps/desktop`, `apps/mobile`, `packages/protocol`) was conducted against the **Universal Computer & Mobile Operator** specification.

The foundation is functional:
- All **19 backend tests** pass (`pytest`).
- Next.js Web frontend compiles cleanly (`next build`, 0 type errors).
- WebSockets, audio pipelines (STT/TTS), and risk policy tiers are in place.

However, the current architecture suffers from a core limitation: **it treats applications as a static hardcoded switch statement rather than a dynamically discovered universe of tools and OS capabilities.** 

To fulfill your vision of NOVA as an autonomous operator that can "complete an assignment", "research and make a presentation", or "open and operate any installed app", NOVA must evolve from an *application launcher* to an *autonomous application operator*.

---

## 2. AUDIT OF CURRENT SUBSYSTEMS & GAPS

| Subsystem | Current State | Critical Gap | Required Architectural Upgrade |
|---|---|---|---|
| **Application Registry** | Hardcoded list in `intent_routes.py` (Notepad, Calc, Code, Chrome, WhatsApp, YouTube) | If an app isn't explicitly coded in python `if/elif`, NOVA cannot find, launch, or control it. | **Universal Dynamic App Discovery Engine**: Scans Windows Registry (`App Paths`, `Uninstall`), Start Menu shortcuts (`.lnk`), `PATH`, macOS `/Applications`, and mobile package registries. |
| **Capability Model** | Binary: "Launch URL" or "Launch Binary" | Cannot distinguish between *Discovery*, *Launching*, *Reading*, *Interacting*, and *Modifying*. | **6-Tier Capability Matrix** per application (`DISCOVERY`, `LAUNCH`, `READ`, `INTERACT`, `MODIFY`, `AUTOMATE`). |
| **Task Execution** | Static single-tool trigger or pre-baked 2-step mock workflow | Cannot dynamically formulate multi-step plans for complex requests like *"complete my assignment"* or *"make a presentation"*. | **Autonomous ReAct Task Planner**: Dynamically generates sub-goals, selects discovered tools, tracks state transitions, and supports interactive clarification. |
| **Document & Productivity** | Simple `.txt` writing in `desktop_tools.py` | Cannot generate Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`), or parse/summarize PDFs. | **Universal Productivity Connectors**: Native python libraries (`python-docx`, `python-pptx`, `openpyxl`, `pypdf`) with structured formatting & preview. |
| **UI & In-App Automation** | Blind key typing (`pyautogui.write`) | Does not inspect UI elements or verify that target windows are in focus. | **Windows UI Automation (UIA) & Accessibility Bridge**: Inspects window titles, control elements, input fields, and verifies focus before interaction. |
| **Browser Automation** | Opens browser tabs via `webbrowser.open` or `cmd start` | Cannot read web pages, scrape content, fill forms, or interact with web apps autonomously. | **Secure Headless/Headful Browser Operator**: Controlled Playwright/HTTP scraping agent that extracts sanitized DOM trees and completes web workflows. |
| **Device Mesh & Target Routing** | Local registry in memory | Desktop cannot dynamically route mobile tasks (*"Open Maps on my Android phone"*). | **Hub-and-Device Multi-Agent Protocol**: WebSocket dispatch routing by `target_device_id` and device capability query. |

---

## 3. TARGET ARCHITECTURE: THE UNIVERSAL OPERATOR

```
                                  +---------------------------------------+
                                  |         NOVA CORE INTELLIGENCE        |
                                  | - Dual LLM Adapters (OpenAI/Anthropic)|
                                  | - Autonomous Multi-Step ReAct Planner |
                                  | - Context & Follow-up State Engine    |
                                  | - User-Approved Memory Store          |
                                  | - 4-Tier Security & Risk Engine       |
                                  +-------------------+-------------------+
                                                      |
                         +----------------------------+----------------------------+
                         |                                                         |
                         v                                                         v
         +-------------------------------+                         +-------------------------------+
         |   DYNAMIC APPLICATION MESH    |                         |    PRODUCTIVITY & DATA SUITE  |
         | - Windows Registry Scanner    |                         | - Office Doc Gen (.docx/.pptx)|
         | - Start Menu & Path Discovery |                         | - Spreadsheet Engine (.xlsx)  |
         | - Capability Classifier (0-5) |                         | - PDF Parser & Summarizer     |
         | - Fallback Manual Register    |                         | - File Search & Organizer     |
         +---------------+---------------+                         +---------------+---------------+
                         |                                                         |
                         +----------------------------+----------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |       EXECUTION & VERIFICATION        |
                                  | - Native OS Shell & Process Manager   |
                                  | - UI Automation (UIA / Accessibility) |
                                  | - Browser Operator (Playwright/Scrape)|
                                  | - Verification (File Exists / Process)|
                                  | - Spoken Human Audio Feedback         |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                          +-----------------------+
                                          |   FUTURISTIC WEB UI   |
                                          | - App Center Hub      |
                                          | - Multi-Step Planner  |
                                          | - Real Waveform / Orb |
                                          | - Desktop/Mobile HUD  |
                                          +-----------------------+
```

---

## 4. PHASED REFACTORING & IMPLEMENTATION PLAN

Following your strict phased engineering guidelines:

### **Phase 1: Architecture & Dynamic Application Discovery Engine**
- Build `services/core/app/devices/app_discovery.py`:
  - Scans Windows `HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths` and `HKCU`.
  - Scans Start Menu `.lnk` shortcuts (`%ProgramData%\Microsoft\Windows\Start Menu\Programs` & `%AppData%`).
  - Scans system `PATH` executables.
  - Generates typed application records: `app_id`, `name`, `executable_path`, `launch_method`, `capabilities`, `risk_tier`.
  - Implements dynamic search and manual user-registration endpoint.

### **Phase 2: Universal Autonomous Task Planner & Intent Engine**
- Upgrade `task_planner.py` to an autonomous goal-oriented planner:
  - Takes natural prompts (e.g. *"complete my assignment on quantum computing and save a presentation"*).
  - Deconstructs prompt into sub-goals: Research $\to$ Synthesize $\to$ Document Create $\to$ Verify $\to$ Voice Report.
  - Links directly to discovered applications and productivity tools dynamically.
  - Supports follow-ups: *"make it shorter"*, *"add 2 more slides"*, *"save it to my desktop"*.

### **Phase 3: Universal Productivity & Document Generation Connectors**
- Implement real document generators in `services/core/app/tools/productivity_tools.py`:
  - Word documents (`.docx`) with headings, paragraphs, bullet points.
  - PowerPoint presentations (`.pptx`) with professional slide titles, content cards, and theme formatting.
  - Excel spreadsheets (`.xlsx`) with calculated rows and table headers.
  - Real PDF reader and summarizer.
  - File verification step confirming file exists and byte length > 0 before reporting success.

### **Phase 4: Browser Operator & YouTube Autonomous Controller**
- Upgrade media and internet automation:
  - Deep YouTube query resolver directly extracting top video identifiers and launching auto-play streams.
  - Web research scraper that extracts clean article texts without advertisement pollution or malicious script execution.
  - Media controls (Play, Pause, Stop, Volume).

### **Phase 5: Windows UI Automation & Desktop In-App Operator**
- Integrate Windows UI Automation:
  - Safe window focus management.
  - In-app typing, keyboard shortcuts, and control triggers.
  - Process verification checking whether target application PID is actually active.

### **Phase 6: Web Dashboard Application Center & Interactive HUD**
- Upgrade Next.js Frontend:
  - Add **Application Center** panel listing discovered installed applications with search, launch triggers, and capability badges.
  - Live Interactive Task Execution Timeline displaying real step-by-step progress and approval modals for Tier 2/3 operations.
  - Fully responsive mobile/desktop HUD layout.

### **Phase 7: Comprehensive Automated Testing & End-to-End Verification**
- Expand pytest test suite:
  - Unit tests for application discovery.
  - Unit tests for dynamic task planning.
  - End-to-end tests for document creation (`.docx`, `.pptx`, `.xlsx`, `.txt`).
  - Security audit and risk tier policy verification.

---

## 5. TEST & ACCEPTANCE STRATEGY

Every single phase will include concrete pytest automated tests and live interactive execution verification. No mocks will be marked as complete.
- **Rule Check**: All code written directly to workspace files.
- **Security Check**: No exposed API keys in frontend code; zero arbitrary unvalidated shell string execution.
- **Verification Rule**: Every action reports actual file paths, process IDs, or tool execution outputs.

---

## 6. READY TO PROCEED

The audit is complete and the architecture is mapped. Please reply with **"CONTINUE"** to begin **Phase 1: Dynamic Application Discovery Engine & Registry**!
