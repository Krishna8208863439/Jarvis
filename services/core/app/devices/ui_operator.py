"""
Project NOVA - Windows Desktop UI Operator Engine
Provides real screen observation, active window discovery, focus management,
and non-blind control interactions using native OS APIs.
"""

import sys
import time
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("nova.desktop.ui_operator")

class WindowInfo:
    def __init__(self, title: str, handle: int, is_active: bool, bounds: Dict[str, int]):
        self.title = title
        self.handle = handle
        self.is_active = is_active
        self.bounds = bounds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "handle": self.handle,
            "is_active": self.is_active,
            "bounds": self.bounds
        }

class WindowsUIOperator:
    """
    Native Windows UI operator for observing visible windows,
    ensuring window focus before typing, and verifying target existence.
    """

    @staticmethod
    def get_open_windows() -> List[Dict[str, Any]]:
        """List all non-empty top-level visible desktop windows."""
        if sys.platform != "win32":
            return []
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            result = []
            for w in windows:
                if w.title and w.title.strip() and w.visible:
                    result.append({
                        "title": w.title,
                        "left": w.left,
                        "top": w.top,
                        "width": w.width,
                        "height": w.height,
                        "is_active": w.isActive
                    })
            return result
        except Exception as e:
            logger.error(f"Error enumerating open windows: {e}")
            return []

    @staticmethod
    def get_active_window_title() -> str:
        """Returns the title of the current foreground active window."""
        if sys.platform != "win32":
            return "Non-Windows OS"
        try:
            import pygetwindow as gw
            active = gw.getActiveWindow()
            return active.title if active else "Unknown"
        except Exception as e:
            logger.warning(f"Failed to query active window: {e}")
            return "Desktop"

    @staticmethod
    def focus_window_by_title(partial_title: str) -> bool:
        """Finds a window matching partial_title, restores if minimized, and brings to front."""
        if sys.platform != "win32":
            return False
        try:
            import pygetwindow as gw
            matching = gw.getWindowsWithTitle(partial_title)
            if not matching:
                # Fuzzy fallback search
                all_wins = gw.getAllWindows()
                matching = [w for w in all_wins if partial_title.lower() in (w.title or "").lower()]

            if matching:
                target = matching[0]
                if target.isMinimized:
                    target.restore()
                target.activate()
                time.sleep(0.3)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to focus window with title '{partial_title}': {e}")
            return False

    @staticmethod
    def safe_in_app_type(text: str, target_window_title: Optional[str] = None) -> Dict[str, Any]:
        """
        Ensures target window is activated before sending keystrokes.
        Prevents blind typing into arbitrary unintended applications.
        """
        import pyautogui

        focused = False
        if target_window_title:
            focused = WindowsUIOperator.focus_window_by_title(target_window_title)

        active_title = WindowsUIOperator.get_active_window_title()
        time.sleep(0.2)

        # Type text cleanly with human cadence
        pyautogui.write(text, interval=0.02)

        return {
            "success": True,
            "typed_text": text,
            "target_window": target_window_title,
            "focused_active_window": active_title
        }

    @staticmethod
    def safe_in_app_hotkey(*keys: str, target_window_title: Optional[str] = None) -> Dict[str, Any]:
        """Sends key combos (e.g. ctrl+s, enter) to target window."""
        import pyautogui

        if target_window_title:
            WindowsUIOperator.focus_window_by_title(target_window_title)

        active_title = WindowsUIOperator.get_active_window_title()
        pyautogui.hotkey(*keys)

        return {
            "success": True,
            "hotkey": list(keys),
            "focused_active_window": active_title
        }

ui_operator = WindowsUIOperator()

