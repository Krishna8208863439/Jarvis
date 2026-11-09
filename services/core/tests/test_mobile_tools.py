import pytest
from app.tools.registry import registry
from app.tools.mobile_tools import MobileOpenAppTool, MobileGetBatteryTool
from app.tools.base_tool import ToolContext

registry.register(MobileOpenAppTool())
registry.register(MobileGetBatteryTool())

@pytest.mark.asyncio
async def test_mobile_open_whatsapp_intent():
    context = ToolContext(user_id="u1", device_id="pixel-8", platform="android")
    res = await registry.execute_tool(
        "mobile.open_app",
        {"app_id": "whatsapp", "query": "Hello from NOVA"},
        context,
        is_confirmed=True
    )
    assert res.success is True
    assert res.data["app_id"] == "whatsapp"

@pytest.mark.asyncio
async def test_mobile_battery_telemetry_safe():
    context = ToolContext(user_id="u1", device_id="iphone-15", platform="ios")
    res = await registry.execute_tool(
        "mobile.get_battery",
        {},
        context,
        is_confirmed=False # Tier 0 Safe requires no confirmation
    )
    assert res.success is True
    assert res.data["battery_level"] == 0.88

