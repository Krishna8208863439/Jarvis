import abc
from enum import Enum
from pydantic import BaseModel, Field

class RiskTier(str, Enum):
    TIER_0_SAFE = "TIER_0_SAFE"               # Read-only actions (search, weather, battery)
    TIER_1_REVERSIBLE = "TIER_1_REVERSIBLE"   # Open apps, volume, reminders
    TIER_2_SENSITIVE = "TIER_2_SENSITIVE"     # Send messages, emails, modify docs
    TIER_3_DANGEROUS = "TIER_3_DANGEROUS"     # Delete files, terminal commands, payment

class ToolContext(BaseModel):
    user_id: str
    device_id: str
    platform: str
    voice_only_auth: bool = False

class ToolExecutionResult(BaseModel):
    success: bool
    data: dict = Field(default_factory=dict)
    message: str = ""
    error: str | None = None

class BaseTool(abc.ABC):
    name: str
    description: str
    parameters: dict
    risk_tier: RiskTier
    supported_platforms: list[str]

    @abc.abstractmethod
    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        """Execute the tool safely."""
        pass

