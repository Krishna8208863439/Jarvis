import logging
from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult
from app.policy.engine import PolicyEngine

logger = logging.getLogger("nova.tools.registry")

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name} [{tool.risk_tier.value}]")

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())

    async def execute_tool(
        self, tool_name: str, arguments: dict, context: ToolContext, is_confirmed: bool = False
    ) -> ToolExecutionResult:
        tool = self.get(tool_name)
        if not tool:
            return ToolExecutionResult(success=False, error=f"Tool {tool_name} not found in registry")

        # Evaluate risk policy
        PolicyEngine.evaluate(tool, context, is_ui_confirmed=is_confirmed)
        return await tool.execute(arguments, context)

# Global Tool Registry
registry = ToolRegistry()

