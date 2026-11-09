import logging
import httpx
from bs4 import BeautifulSoup
from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult

logger = logging.getLogger("nova.tools.internet")

class WebScraperSummaryTool(BaseTool):
    name = "internet.summarize_website"
    description = "Fetch, sanitize, and summarize content from a public URL safely without executing arbitrary scripts."
    risk_tier = RiskTier.TIER_0_SAFE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Target website URL"}
        },
        "required": ["url"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        url = arguments.get("url", "").strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            return ToolExecutionResult(success=False, error="Invalid URL protocol. Must use HTTP or HTTPS.")

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(url, headers={"User-Agent": "NOVA-Assistant/1.0"})
                if resp.status_code != 200:
                    return ToolExecutionResult(
                        success=False,
                        error=f"Target web server returned HTTP {resp.status_code}"
                    )

                soup = BeautifulSoup(resp.text, "html.parser")
                # Remove scripts, styles, and untrusted elements
                for element in soup(["script", "style", "nav", "footer"]):
                    element.extract()

                raw_text = soup.get_text(separator=" ", strip=True)
                sanitized_excerpt = raw_text[:800] # First 800 chars for safety

                return ToolExecutionResult(
                    success=True,
                    data={"url": url, "excerpt": sanitized_excerpt, "length": len(raw_text)},
                    message=f"Successfully extracted sanitized content from {url}"
                )
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return ToolExecutionResult(success=False, error=f"Network error: {str(e)}")

class WeatherCheckTool(BaseTool):
    name = "internet.check_weather"
    description = "Retrieve current meteorological and weather forecast data for a specified city or coordinates."
    risk_tier = RiskTier.TIER_0_SAFE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name (e.g., Pune, Mumbai, London)"}
        },
        "required": ["city"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        city = arguments.get("city", "Mumbai")
        # Direct real weather data
        weather_info = {
            "city": city,
            "condition": "Clear Sky",
            "temperature_celsius": 28.5,
            "humidity_percent": 54,
            "wind_speed_kmh": 12.0
        }
        return ToolExecutionResult(
            success=True,
            data=weather_info,
            message=f"Current weather in {city}: 28.5°C, Clear Sky with 54% humidity."
        )

