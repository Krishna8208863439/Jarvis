# QA Bug Register: Project NOVA

| Bug ID | Component | Description | Root Cause | Fix Applied | Status |
|---|---|---|---|---|:---:|
| **BUG-001** | `operator_engine.py` | "Open YouTube" intent triggered empty query playback rather than launching website | Keyword checking routed all YouTube occurrences to `pywhatkit.playonyt("")` | Disambiguated "open youtube" to open direct URL in default browser | **FIXED** |
| **BUG-002** | `productivity_tools.py` | Automated tests hung during document generation on Windows | Unattended `os.startfile()` opened default editor, blocking test runner | Added `NO_AUTO_OPEN` environment check for headless test execution | **FIXED** |
| **BUG-003** | `context_resolver.py` | Punctuation in voice confirmation ("Yes, send it") caused regex check failure | String matching was exact rather than sanitized of punctuation | Applied regex alphanumeric cleaning before phrase matching | **FIXED** |
| **BUG-004** | `react_engine.py` | Tool execution failed in ReAct loop with "Tool not found in registry" | Productivity tools were not registered before ReAct instantiation | Added explicit registration of `CreateWordDocumentTool`, etc. | **FIXED** |
| **BUG-005** | `voiceRecognition.ts` | Speech recognition terminated silently after browser silence timeout | Web Speech API fires `onend` on speech pauses | Added persistent auto-restart loop with `shouldKeepListening` flag and 200ms debounce | **FIXED** |

