"""
Project NOVA - Dynamic Universal Application Discovery Engine
Scans the local operating system (Windows Registry, Start Menu, PATH)
to build an extensible registry of installed applications with capability classification.
"""

import os
import sys
import shutil
import logging
from typing import List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("nova.apps.discovery")

class AppCapability(str):
    DISCOVERY = "DISCOVERY"     # Discovered on device
    LAUNCH = "LAUNCH"           # Executable launch verified
    READ = "READ"               # Text/UI reading supported
    INTERACT = "INTERACT"       # In-app typing/shortcuts supported
    MODIFY = "MODIFY"           # File/document editing supported
    AUTOMATE = "AUTOMATE"       # Deep API / Accessibility automation

class RegisteredApp(BaseModel):
    app_id: str
    name: str
    platform: str = "windows"
    executable_path: Optional[str] = None
    package_id: Optional[str] = None
    launch_command: str
    is_available: bool = True
    capabilities: List[str] = Field(default_factory=lambda: [AppCapability.DISCOVERY, AppCapability.LAUNCH, AppCapability.INTERACT])
    category: str = "Productivity" # Browser, Productivity, Media, Development, System
    last_verified: Optional[str] = None

class UniversalAppRegistry:
    def __init__(self):
        self._apps: dict[str, RegisteredApp] = {}
        self._bootstrap_known_applications()
        if sys.platform == "win32":
            self.scan_windows_system()

    def _bootstrap_known_applications(self):
        """Standard applications pre-configured with known default executable identifiers."""
        known_defaults = [
            # System & Utilities
            ("notepad", "Notepad", "notepad.exe", "System"),
            ("calc", "Calculator", "calc.exe", "System"),
            ("explorer", "File Explorer", "explorer.exe", "System"),
            ("cmd", "Command Prompt", "cmd.exe", "System"),
            ("powershell", "PowerShell", "powershell.exe", "System"),
            ("taskmgr", "Task Manager", "taskmgr.exe", "System"),
            
            # Web Browsers
            ("chrome", "Google Chrome", "chrome.exe", "Browser"),
            ("msedge", "Microsoft Edge", "msedge.exe", "Browser"),
            ("firefox", "Mozilla Firefox", "firefox.exe", "Browser"),
            ("brave", "Brave Browser", "brave.exe", "Browser"),

            # Development
            ("code", "Visual Studio Code", "code.cmd", "Development"),
            ("git", "Git Bash", "git-bash.exe", "Development"),
            
            # Productivity & Office
            ("excel", "Microsoft Excel", "excel.exe", "Productivity"),
            ("winword", "Microsoft Word", "winword.exe", "Productivity"),
            ("powerpnt", "Microsoft PowerPoint", "powerpnt.exe", "Productivity"),

            # Media & Communication
            ("spotify", "Spotify", "spotify.exe", "Media"),
            ("vlc", "VLC Media Player", "vlc.exe", "Media"),
            ("telegram", "Telegram Desktop", "telegram.exe", "Communication"),
            ("whatsapp", "WhatsApp", "whatsapp:", "Communication"),
        ]

        for app_id, name, exe, cat in known_defaults:
            path = shutil.which(exe) or shutil.which(exe.replace(".exe", ""))
            self._apps[app_id] = RegisteredApp(
                app_id=app_id,
                name=name,
                platform="windows",
                executable_path=path,
                launch_command=exe,
                is_available=True,
                category=cat,
                capabilities=[
                    AppCapability.DISCOVERY,
                    AppCapability.LAUNCH,
                    AppCapability.INTERACT,
                    AppCapability.MODIFY if cat in ["Productivity", "Development"] else AppCapability.READ
                ]
            )

    def scan_windows_system(self):
        """Scan Windows App Paths and Start Menu shortcuts for all user-installed applications."""
        if sys.platform != "win32":
            return

        try:
            import winreg

            # 1. Scan App Paths registry (Both HKLM and HKCU)
            reg_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
            ]

            for hkey, subkey in reg_paths:
                try:
                    with winreg.OpenKey(hkey, subkey) as root_key:
                        num_subkeys, _, _ = winreg.QueryInfoKey(root_key)
                        for i in range(num_subkeys):
                            try:
                                key_name = winreg.EnumKey(root_key, i)
                                with winreg.OpenKey(root_key, key_name) as app_key:
                                    raw_path, _ = winreg.QueryValueEx(app_key, "")
                                    exe_path = raw_path.strip('"')
                                    if exe_path and os.path.exists(exe_path):
                                        clean_id = key_name.lower().replace(".exe", "")
                                        display_name = clean_id.capitalize()
                                        if clean_id in self._apps:
                                            self._apps[clean_id].executable_path = exe_path
                                            self._apps[clean_id].launch_command = f'"{exe_path}"'
                                            self._apps[clean_id].is_available = True
                                        else:
                                            self._apps[clean_id] = RegisteredApp(
                                                app_id=clean_id,
                                                name=display_name,
                                                platform="windows",
                                                executable_path=exe_path,
                                                launch_command=f'"{exe_path}"',
                                                is_available=True,
                                                category="Discovered Application",
                                                capabilities=[AppCapability.DISCOVERY, AppCapability.LAUNCH, AppCapability.INTERACT]
                                            )
                            except Exception:
                                continue
                except Exception:
                    continue
        except Exception as e:
            logger.warning(f"Windows registry app scan skipped: {e}")

        # 2. Scan Windows Start Menu Shortcuts (.lnk files)
        try:
            start_dirs = [
                os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
                os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            ]
            for start_dir in start_dirs:
                if not os.path.exists(start_dir):
                    continue
                for root, _, files in os.walk(start_dir):
                    for file in files:
                        if file.lower().endswith(".lnk") and not file.lower().startswith("uninstall"):
                            lnk_name = file[:-4].strip()
                            clean_id = lnk_name.lower().replace(" ", "")
                            full_path = os.path.join(root, file)

                            # Map common Office and productivity aliases to core IDs
                            mapped_id = None
                            if clean_id in ["word", "microsoftword"]:
                                mapped_id = "winword"
                            elif clean_id in ["excel", "microsoftexcel"]:
                                mapped_id = "excel"
                            elif clean_id in ["powerpoint", "microsoftpowerpoint"]:
                                mapped_id = "powerpnt"
                            elif clean_id in ["googlechrome"]:
                                mapped_id = "chrome"
                            elif clean_id in ["visualstudiocode"]:
                                mapped_id = "code"

                            target_id = mapped_id or clean_id
                            if target_id in self._apps:
                                self._apps[target_id].launch_command = f'"{full_path}"'
                                self._apps[target_id].executable_path = full_path
                                self._apps[target_id].is_available = True
                            else:
                                self._apps[clean_id] = RegisteredApp(
                                    app_id=clean_id,
                                    name=lnk_name,
                                    platform="windows",
                                    executable_path=full_path,
                                    launch_command=f'"{full_path}"',
                                    is_available=True,
                                    category="Start Menu Application",
                                    capabilities=[AppCapability.DISCOVERY, AppCapability.LAUNCH, AppCapability.INTERACT]
                                )
        except Exception as e:
            logger.warning(f"Windows Start Menu scan skipped: {e}")

    def search_app(self, query: str) -> Optional[RegisteredApp]:
        """Fuzzy search installed applications by name or id."""
        q = query.lower().strip()
        # Direct key match
        if q in self._apps:
            return self._apps[q]

        # Common aliases
        alias_map = {
            "browser": "chrome",
            "google chrome": "chrome",
            "vs code": "code",
            "vscode": "code",
            "visual studio code": "code",
            "word": "winword",
            "ms word": "winword",
            "microsoft word": "winword",
            "sheets": "excel",
            "spreadsheet": "excel",
            "ms excel": "excel",
            "microsoft excel": "excel",
            "slides": "powerpnt",
            "powerpoint": "powerpnt",
            "ppt": "powerpnt",
            "presentation": "powerpnt",
            "calculator": "calc",
            "files": "explorer",
            "folder": "explorer",
            "my files": "explorer",
            "this pc": "explorer",
            "terminal": "wt",
            "windows terminal": "wt",
        }
        target_id = alias_map.get(q)
        if target_id and target_id in self._apps:
            return self._apps[target_id]

        # Name or alias match
        for app in self._apps.values():
            if q in app.name.lower() or q in app.app_id:
                return app

        return None

    def register_manual_app(self, app_id: str, name: str, launch_command: str, category: str = "Custom") -> RegisteredApp:
        """Allow user to manually register any custom installed app."""
        app = RegisteredApp(
            app_id=app_id.lower().strip(),
            name=name,
            platform="windows",
            executable_path=launch_command if os.path.exists(launch_command) else None,
            launch_command=launch_command,
            is_available=True,
            category=category,
            capabilities=[AppCapability.DISCOVERY, AppCapability.LAUNCH, AppCapability.INTERACT]
        )
        self._apps[app.app_id] = app
        return app

    def list_apps(self, category: Optional[str] = None) -> List[RegisteredApp]:
        apps = list(self._apps.values())
        if category:
            apps = [a for a in apps if a.category.lower() == category.lower()]
        return apps

app_registry = UniversalAppRegistry()
