import pytest
from app.brain.task_planner import AdvancedTaskPlanner
from app.tools.base_tool import ToolContext

@pytest.mark.asyncio
async def test_flagship_workflow_1_execution():
    context = ToolContext(user_id="u1", device_id="desktop-1", platform="windows")
    plan = AdvancedTaskPlanner.create_flagship_workflow_1(user_id="u1")
    assert len(plan.steps) == 2
    assert plan.steps[0].tool_name == "internet.search_jobs"
    assert plan.steps[1].tool_name == "desktop.create_document"

    # Execute with explicit Tier 2 confirmation
    executed = await AdvancedTaskPlanner.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[0].status == "COMPLETED"
    assert executed.steps[1].status == "COMPLETED"
    assert "bytes_written" in executed.steps[1].result

@pytest.mark.asyncio
async def test_flagship_workflow_2_jobs():
    context = ToolContext(user_id="u1", device_id="desktop-1", platform="all")
    plan = AdvancedTaskPlanner.create_flagship_workflow_2(user_id="u1", query="python developer fresher")
    executed = await AdvancedTaskPlanner.execute_plan(plan, context, is_confirmed=False)
    assert executed.status == "COMPLETED"
    assert len(executed.steps[0].result["jobs"]) > 0

