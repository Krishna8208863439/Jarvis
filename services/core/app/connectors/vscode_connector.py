"""
Project NOVA - Universal VS Code & Developer Automation Connector
Handles project directory scaffolding, file generation, test runner execution,
and error inspection for live development tasks.
"""

import os
import subprocess
import logging
from typing import Dict, Any, List

logger = logging.getLogger("nova.connectors.vscode")

class VSCodeConnector:
    """
    Connects NOVA to developer environments (VS Code, terminal, git),
    scaffolding complete Python/JS projects and executing tests.
    """

    @staticmethod
    def create_project_scaffold(project_name: str, files: Dict[str, str], target_dir: str = ".") -> Dict[str, Any]:
        """Creates directory, writes source files, and opens project in VS Code."""
        project_path = os.path.join(target_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        created_files = []
        for filename, content in files.items():
            filepath = os.path.join(project_path, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            created_files.append(filename)

        # Open in VS Code if command is available
        try:
            subprocess.Popen(f"code \"{project_path}\"", shell=True)
        except Exception as e:
            logger.warning(f"Could not launch VS Code directly: {e}")

        return {
            "status": "PROJECT_CREATED",
            "project_name": project_name,
            "project_path": project_path,
            "files": created_files
        }

    @staticmethod
    def run_tests_and_verify(project_path: str, test_command: str = "pytest") -> Dict[str, Any]:
        """Runs test command in project path and returns execution status."""
        try:
            result = subprocess.run(
                test_command,
                cwd=project_path,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[:500],
                "stderr": result.stderr[:500],
                "returncode": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

vscode_connector = VSCodeConnector()

