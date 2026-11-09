"""
Project NOVA - Windows Native Process Lifecycle & Window State Controller
Provides process supervision, allowlist validation, graceful termination,
and active window bounds monitoring.
"""

import sys
import psutil
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("nova.desktop.process_controller")

ALLOWLISTED_BINARIES = {
    "notepad.exe": "Notepad",
    "calc.exe": "Calculator",
    "explorer.exe": "File Explorer",
    "cmd.exe": "Command Prompt",
    "powershell.exe": "PowerShell",
    "taskmgr.exe": "Task Manager",
    "chrome.exe": "Google Chrome",
    "msedge.exe": "Microsoft Edge",
    "firefox.exe": "Mozilla Firefox",
    "brave.exe": "Brave Browser",
    "code.cmd": "Visual Studio Code",
    "code.exe": "Visual Studio Code",
    "winword.exe": "Microsoft Word",
    "excel.exe": "Microsoft Excel",
    "powerpnt.exe": "Microsoft PowerPoint",
    "spotify.exe": "Spotify",
    "vlc.exe": "VLC Media Player",
    "telegram.exe": "Telegram Desktop",
    "whatsapp.exe": "WhatsApp"
}

class WindowsProcessController:
    """Manages process life cycle, allowlisting, and health checks on Windows."""

    @staticmethod
    def is_process_running(process_name: str) -> bool:
        """Checks if any process matching process_name is currently active."""
        p_lower = process_name.lower().replace(".exe", "")
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info.get("name") or ""
                if p_lower in name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    @staticmethod
    def get_running_allowlisted_apps() -> List[Dict[str, Any]]:
        """Returns details on all currently running allowlisted desktop applications."""
        running = []
        for proc in psutil.process_iter(["pid", "name", "create_time"]):
            try:
                p_name = (proc.info.get("name") or "").lower()
                for binary, friendly_name in ALLOWLISTED_BINARIES.items():
                    if binary in p_name:
                        running.append({
                            "name": friendly_name,
                            "binary": binary,
                            "pid": proc.info.get("pid")
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return running

    @staticmethod
    def terminate_process_by_name(process_name: str) -> bool:
        """Gracefully terminates a running process by name."""
        p_lower = process_name.lower().replace(".exe", "")
        killed = False
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info.get("name") or ""
                if p_lower in name.lower():
                    proc.terminate()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return killed

process_controller = WindowsProcessController()

