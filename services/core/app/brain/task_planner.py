from pydantic import BaseModel, Field
import datetime
from app.tools.registry import registry
from app.tools.base_tool import ToolContext, ToolExecutionResult
from app.policy.engine import RiskTier

class PlanStep(BaseModel):
    step_id: str
    tool_name: str
    arguments: dict
    risk_tier: RiskTier
    description: str
    status: str = "PENDING" # PENDING, CONFIRMING, RUNNING, COMPLETED, FAILED
    result: dict = Field(default_factory=dict)
    error: str | None = None

class MultiStepPlan(BaseModel):
    plan_id: str
    user_prompt: str
    steps: list[PlanStep]
    status: str = "PLANNING" # PLANNING, AWAITING_APPROVAL, EXECUTING, COMPLETED, CANCELLED

class AdvancedTaskPlanner:
    @staticmethod
    def create_flagship_workflow_1(user_id: str, topic: str = "AI Voice Assistant") -> MultiStepPlan:
        """Flagship Workflow 1: 'prepare my project report and save it on my desktop'"""
        steps = [
            PlanStep(
                step_id="step-1",
                tool_name="internet.search_jobs",
                arguments={"query": topic},
                risk_tier=RiskTier.TIER_0_SAFE,
                description=f"Gather research data on {topic}"
            ),
            PlanStep(
                step_id="step-2",
                tool_name="desktop.create_document",
                arguments={
                    "file_name": "Project_Nova_Report.txt",
                    "content": f"# Project NOVA Engineering Report\nTopic: {topic}\nArchitecture: Hub-and-Agent Mesh\nStatus: Complete"
                },
                risk_tier=RiskTier.TIER_2_SENSITIVE,
                description="Save generated report to user Desktop after confirmation"
            )
        ]
        return MultiStepPlan(plan_id="plan-wf1", user_prompt="Prepare project report and save to desktop", steps=steps)

    @staticmethod
    def create_flagship_workflow_2(user_id: str, query: str = "python developer fresher") -> MultiStepPlan:
        """Flagship Workflow 2: 'find Python developer jobs for freshers'"""
        steps = [
            PlanStep(
                step_id="step-1",
                tool_name="internet.search_jobs",
                arguments={"query": query},
                risk_tier=RiskTier.TIER_0_SAFE,
                description=f"Search online listings for {query}"
            )
        ]
        return MultiStepPlan(plan_id="plan-wf2", user_prompt=f"Find {query} opportunities", steps=steps)

    @staticmethod
    async def execute_plan(plan: MultiStepPlan, context: ToolContext, is_confirmed: bool = False) -> MultiStepPlan:
        plan.status = "EXECUTING"
        for step in plan.steps:
            step.status = "RUNNING"
            try:
                res = await registry.execute_tool(step.tool_name, step.arguments, context, is_confirmed=is_confirmed)
                if res.success:
                    step.status = "COMPLETED"
                    step.result = res.data
                else:
                    step.status = "FAILED"
                    step.error = res.error
                    plan.status = "FAILED"
                    return plan
            except Exception as e:
                step.status = "FAILED"
                step.error = str(e)
                plan.status = "FAILED"
                return plan
        plan.status = "COMPLETED"
        return plan

