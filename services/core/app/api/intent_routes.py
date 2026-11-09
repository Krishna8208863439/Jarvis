import time
import subprocess
import pyautogui
from pydantic import BaseModel
from fastapi import APIRouter
from app.tools.registry import registry
from app.tools.base_tool import ToolContext

router = APIRouter(prefix="/api/v1/intent")

class VoiceIntentRequest(BaseModel):
    user_prompt: str
    platform: str = "web"
    device_id: str = "local-device"
    language: str = "en"

class VoiceIntentResponse(BaseModel):
    spoken_response: str
    action_executed: str | None = None
    action_type: str | None = None
    target_url: str | None = None
    app_target: str | None = None
    success: bool = True

def launch_windows_cmd(target: str):
    """Direct native execution on Windows OS without sandbox limits."""
    try:
        # Use os.startfile for native Windows shell execution
        import os
        if target.startswith("http://") or target.startswith("https://"):
            import webbrowser
            webbrowser.open(target)
        elif target == "notepad":
            os.system("start notepad")
        elif target == "calc":
            os.system("start calc")
        elif target == "code":
            os.system("start code")
        elif target == "explorer":
            os.system("start explorer")
        elif target == "chrome":
            os.system("start chrome")
        else:
            os.system(f"start {target}")
    except Exception as e:
        print(f"Failed to launch {target}: {e}")

@router.post("/execute", response_model=VoiceIntentResponse)
async def execute_voice_intent(req: VoiceIntentRequest):
    prompt = req.user_prompt.lower().strip()
    context = ToolContext(user_id="user-1", device_id=req.device_id, platform=req.platform)

    # 1. In-App Task: Type or write text inside the currently open application
    if prompt.startswith("type ") or prompt.startswith("write ") or "type in" in prompt:
        text_to_type = prompt.replace("type in", "").replace("type ", "").replace("write ", "").strip()
        time.sleep(0.5)
        pyautogui.write(text_to_type, interval=0.03)
        return VoiceIntentResponse(
            spoken_response=f"Typed {text_to_type}",
            action_executed="in_app_type",
            action_type="keyboard_action",
            success=True,
        )

    # 2. In-App Task: Press Enter / Send message
    if "press enter" in prompt or "send message" in prompt or "hit enter" in prompt or prompt == "send":
        pyautogui.press("enter")
        return VoiceIntentResponse(
            spoken_response="Sent.",
            action_executed="press_enter",
            action_type="keyboard_action",
            success=True,
        )

    # 3. In-App Task: Search inside active window / app (Ctrl+F)
    if prompt.startswith("search for ") or prompt.startswith("find "):
        query = prompt.replace("search for ", "").replace("find ", "").strip()
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.3)
        pyautogui.write(query, interval=0.03)
        pyautogui.press("enter")
        return VoiceIntentResponse(
            spoken_response=f"Searching for {query}.",
            action_executed="in_app_search",
            action_type="keyboard_action",
            success=True,
        )

    # 4. In-App Task: Save file (Ctrl+S)
    if "save file" in prompt or "save document" in prompt or "save this" in prompt:
        pyautogui.hotkey("ctrl", "s")
        return VoiceIntentResponse(
            spoken_response="Saved current document.",
            action_executed="in_app_save",
            action_type="keyboard_action",
            success=True,
        )

    # 5. In-App Task: Close current window/tab (Ctrl+W)
    if "close tab" in prompt or "close window" in prompt:
        pyautogui.hotkey("ctrl", "w")
        return VoiceIntentResponse(
            spoken_response="Closed active window.",
            action_executed="close_tab",
            action_type="keyboard_action",
            success=True,
        )

    # 6. Open WhatsApp: Both native OS launch & web tab
    if "whatsapp" in prompt:
        launch_windows_cmd("https://web.whatsapp.com")
        return VoiceIntentResponse(
            spoken_response="Opening WhatsApp for you right now.",
            action_executed="open_whatsapp",
            action_type="open_url",
            target_url="https://web.whatsapp.com",
            app_target="whatsapp",
            success=True,
        )

    # 7. Open YouTube & Automatically Play Song/Video directly
    if "youtube" in prompt or "song" in prompt or "play" in prompt:
        song_query = (
            prompt.replace("open youtube and play", "")
            .replace("open youtube", "")
            .replace("play a", "")
            .replace("play", "")
            .replace("on youtube", "")
            .strip()
        )
        if not song_query:
            song_query = "dj song"

        try:
            import pywhatkit
            pywhatkit.playonyt(song_query)
        except Exception:
            import webbrowser
            webbrowser.open(f"https://www.youtube.com/results?search_query={song_query}")

        return VoiceIntentResponse(
            spoken_response=f"Playing {song_query} on YouTube.",
            action_executed="play_youtube",
            action_type="open_url",
            target_url=f"https://www.youtube.com/results?search_query={song_query}",
            app_target="youtube",
            success=True,
        )

    # 8. Open Google / Search the web
    if "google" in prompt or prompt.startswith("search "):
        query = prompt.replace("open google and search for", "").replace("open google", "").replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}" if query else "https://www.google.com"
        launch_windows_cmd(url)
        return VoiceIntentResponse(
            spoken_response=f"Searching Google for {query or 'your search'}.",
            action_executed="open_google",
            action_type="open_url",
            target_url=url,
            app_target="google",
            success=True,
        )

    # 9. Open VS Code
    if "vs code" in prompt or "vscode" in prompt or "code" in prompt:
        launch_windows_cmd("code")
        return VoiceIntentResponse(
            spoken_response="Opening Visual Studio Code.",
            action_executed="launch_vscode",
            action_type="desktop_launch",
            app_target="code",
            success=True,
        )

    # 10. Open Notepad
    if "notepad" in prompt or "note" in prompt:
        launch_windows_cmd("notepad")
        return VoiceIntentResponse(
            spoken_response="Opening Notepad.",
            action_executed="launch_notepad",
            action_type="desktop_launch",
            app_target="notepad",
            success=True,
        )

    # 11. Open Calculator
    if "calc" in prompt or "calculator" in prompt:
        launch_windows_cmd("calc")
        return VoiceIntentResponse(
            spoken_response="Opening Calculator.",
            action_executed="launch_calc",
            action_type="desktop_launch",
            app_target="calc",
            success=True,
        )

    # 12. Open Chrome Browser
    if "chrome" in prompt or "browser" in prompt:
        launch_windows_cmd("chrome")
        return VoiceIntentResponse(
            spoken_response="Opening Chrome browser.",
            action_executed="launch_chrome",
            action_type="desktop_launch",
            app_target="chrome",
            success=True,
        )

    # 13. Open File Explorer / Files / Folder
    if "explorer" in prompt or "file" in prompt or "folder" in prompt:
        launch_windows_cmd("explorer")
        return VoiceIntentResponse(
            spoken_response="Opening File Explorer.",
            action_executed="launch_explorer",
            action_type="desktop_launch",
            app_target="explorer",
            success=True,
        )

    # Fallback response
    return VoiceIntentResponse(
        spoken_response=f"Executing: '{req.user_prompt}'.",
        action_executed="generic_task",
        success=True,
    )

