import pytest
from app.tools.registry import registry
from app.tools.desktop_tools import DesktopLaunchAppTool, DesktopCreateDocumentTool
from app.tools.base_tool import ToolContext

registry.register(DesktopLaunchAppTool())
registry.register(DesktopCreateDocumentTool())

@pytest.mark.asyncio
async def test_launch_allowlisted_desktop_app_validation():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows")
    # Disallowed binary
    res = await registry.execute_tool(
        "desktop.launch_app", {"app_name": "malicious_script"}, context
    )
    assert res.success is False
    assert "not in the desktop security allowlist" in res.error

@pytest.mark.asyncio
async def test_create_desktop_document_sensitive_tool():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows")
    res = await registry.execute_tool(
        "desktop.create_document",
        {"file_name": "nova_test_report.txt", "content": "NOVA Phase 6 Verification Test"},
        context,
        is_confirmed=True # Tier 2 confirmed
    )
    assert res.success is True
    assert res.data["bytes_written"] > 0

