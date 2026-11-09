import pytest
from app.tools.registry import registry
from app.tools.internet_tools import WebScraperSummaryTool, WeatherCheckTool
from app.tools.base_tool import ToolContext

registry.register(WebScraperSummaryTool())
registry.register(WeatherCheckTool())

@pytest.mark.asyncio
async def test_weather_check_tool():
    context = ToolContext(user_id="u1", device_id="d1", platform="all")
    res = await registry.execute_tool("internet.check_weather", {"city": "Pune"}, context)
    assert res.success is True
    assert res.data["city"] == "Pune"
    assert "temperature_celsius" in res.data

@pytest.mark.asyncio
async def test_web_scraper_invalid_protocol():
    context = ToolContext(user_id="u1", device_id="d1", platform="all")
    res = await registry.execute_tool("internet.summarize_website", {"url": "ftp://malicious.com"}, context)
    assert res.success is False
    assert "Invalid URL protocol" in res.error

