import os
import subprocess
import logging
from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult

logger = logging.getLogger("nova.tools.desktop")

# Strict Allowlisted Binaries & Executable Applications
ALLOWED_APPS = {
    "vscode": "code",
    "code": "code",
    "chrome": "chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "explorer": "explorer",
}

class DesktopLaunchAppTool(BaseTool):
    name = "desktop.launch_app"
    description = "Launch a verified, allowlisted desktop application safely."
    risk_tier = RiskTier.TIER_1_REVERSIBLE
    supported_platforms = ["windows", "macos", "linux"]
    parameters = {
        "type": "object",
        "properties": {
            "app_name": {
                "type": "string",
                "description": "Name of allowlisted application (e.g., code, chrome, notepad)"
            }
        },
        "required": ["app_name"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        app_name = arguments.get("app_name", "").lower().strip()
        binary = ALLOWED_APPS.get(app_name)

        if not binary:
            return ToolExecutionResult(
                success=False,
                error=f"Application '{app_name}' is not in the desktop security allowlist."
            )

        try:
            # Safe launch using isolated subprocess array without shell=True
            subprocess.Popen([binary], shell=False)
            return ToolExecutionResult(
                success=True,
                data={"launched": binary},
                message=f"Application '{binary}' launched successfully on {context.platform}."
            )
        except Exception as e:
            logger.error(f"Failed to launch application {binary}: {e}")
            return ToolExecutionResult(
                success=False,
                error=f"Failed to launch application: {str(e)}"
            )

class DesktopCreateDocumentTool(BaseTool):
    name = "desktop.create_document"
    description = "Create and save an approved document or report file in the desktop environment."
    risk_tier = RiskTier.TIER_2_SENSITIVE
    supported_platforms = ["windows", "macos", "linux"]
    parameters = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string", "description": "Target filename (e.g. report.txt)"},
            "content": {"type": "string", "description": "Text content to save"}
        },
        "required": ["file_name", "content"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        file_name = arguments.get("file_name", "nova_report.txt")
        content = arguments.get("content", "")

        # Write to user Desktop or fallback to current directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop_dir):
            desktop_dir = os.getcwd()
        os.makedirs(desktop_dir, exist_ok=True)
        target_path = os.path.join(desktop_dir, file_name)

        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

            return ToolExecutionResult(
                success=True,
                data={"path": target_path, "bytes_written": len(content)},
                message=f"Document successfully created at {target_path}"
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                error=f"Could not write file: {str(e)}"
            )
