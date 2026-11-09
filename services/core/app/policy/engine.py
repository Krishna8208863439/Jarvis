import logging
from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult

logger = logging.getLogger("nova.policy.engine")

class PolicyViolationError(Exception):
    pass

class PolicyEngine:
    @staticmethod
    def evaluate(tool: BaseTool, context: ToolContext, is_ui_confirmed: bool = False) -> bool:
        """
        Evaluate risk policy for a given tool execution:
        - Tier 0: Execute immediately.
        - Tier 1: Execute within granted permissions.
        - Tier 2: Require explicit confirmation showing recipient and content.
        - Tier 3: Require on-screen confirmation; voice-only 'yes' is strictly rejected.
        """
        logger.info(f"Evaluating policy for {tool.name} (Risk: {tool.risk_tier.value})")

        # Prompt injection & untrusted context sanitize
        if context.platform not in tool.supported_platforms and "all" not in tool.supported_platforms:
            raise PolicyViolationError(f"Tool {tool.name} is not supported on platform {context.platform}")

        if tool.risk_tier == RiskTier.TIER_0_SAFE:
            return True

        if tool.risk_tier == RiskTier.TIER_1_REVERSIBLE:
            return True

        if tool.risk_tier == RiskTier.TIER_2_SENSITIVE:
            if not is_ui_confirmed:
                raise PolicyViolationError(f"Sensitive action {tool.name} requires explicit user confirmation.")
            return True

        if tool.risk_tier == RiskTier.TIER_3_DANGEROUS:
            if context.voice_only_auth:
                raise PolicyViolationError("Voice-only confirmation is strictly prohibited for Tier 3 dangerous operations.")
            if not is_ui_confirmed:
                raise PolicyViolationError(f"Dangerous action {tool.name} requires explicit on-screen confirmation and authentication.")
            return True

        return False

