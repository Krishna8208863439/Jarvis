import pytest
from app.devices.app_discovery import app_registry
from app.brain.operator_engine import UniversalOperatorEngine
from app.tools.base_tool import ToolContext

def test_dynamic_app_discovery_registry():
    apps = app_registry.list_apps()
    assert len(apps) > 5
    # Verify core apps are present
    notepad = app_registry.search_app("notepad")
    assert notepad is not None
    assert notepad.app_id == "notepad"
    assert "LAUNCH" in notepad.capabilities

    # Fuzzy alias search test
    calc = app_registry.search_app("calculator")
    assert calc is not None
    assert calc.app_id == "calc"

def test_manual_app_registration():
    custom = app_registry.register_manual_app("mytool", "My Custom Tool", "mytool.exe", "Custom")
    assert custom.app_id == "mytool"
    found = app_registry.search_app("mytool")
    assert found is not None
    assert found.name == "My Custom Tool"

@pytest.mark.asyncio
async def test_universal_operator_word_document_generation():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("complete my assignment on Quantum Computing")
    assert plan.primary_intent == "COMPLETE_ASSIGNMENT"
    assert len(plan.steps) == 2
    assert plan.steps[1].action_type == "create_document"

    # Execute with confirmation
    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[1].status == "COMPLETED"
    assert "bytes" in executed.steps[1].result

@pytest.mark.asyncio
async def test_universal_operator_powerpoint_presentation():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("prepare my presentation on Autonomous AI Agents")
    assert plan.primary_intent == "CREATE_PRESENTATION"
    assert len(plan.steps) == 1
    assert plan.steps[0].action_type == "create_presentation"

    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[0].status == "COMPLETED"
    assert executed.steps[0].result["slides_count"] >= 4

@pytest.mark.asyncio
async def test_universal_operator_excel_spreadsheet():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("create a budget spreadsheet for Q1")
    assert plan.primary_intent == "CREATE_SPREADSHEET"

    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[0].result["rows_count"] > 0

