"""
Comprehensive End-to-End Test Suite for Project NOVA Universal Operator
Covers:
1. Dynamic Application Discovery & Registration
2. Natural Spoken Intent Parsing
3. Real Word Document Generation & Verification
4. Real PowerPoint Slide Generation & Verification
5. Real Excel Spreadsheet Generation & Verification
6. Web Research & Knowledge Extraction
7. Windows UI Operator Window & Focus Management
8. Mobile Mesh Intent Payload Synthesis
"""

import pytest
import os
import asyncio
from app.devices.app_discovery import app_registry
from app.brain.operator_engine import UniversalOperatorEngine
from app.tools.base_tool import ToolContext
from app.tools.browser_agent import browser_agent
from app.devices.ui_operator import ui_operator
from app.devices.mobile_mesh import mobile_connector

def test_dynamic_application_discovery():
    apps = app_registry.list_apps()
    assert len(apps) >= 5, "Expected at least 5 standard applications discovered"
    notepad = app_registry.search_app("notepad")
    assert notepad is not None
    assert notepad.name == "Notepad"

def test_intent_parsing_and_planning():
    # Test App Launch Intent
    p1 = UniversalOperatorEngine.parse_and_plan("open notepad")
    assert p1.primary_intent == "OPEN_APPLICATION"
    assert p1.steps[0].action_type == "launch_app"

    # Test Assignment Document Intent
    p2 = UniversalOperatorEngine.parse_and_plan("complete my assignment on Machine Learning")
    assert p2.primary_intent == "COMPLETE_ASSIGNMENT"
    assert p2.status == "AWAITING_APPROVAL"
    assert len(p2.steps) == 2

    # Test Presentation Intent
    p3 = UniversalOperatorEngine.parse_and_plan("prepare my presentation on Neural Networks")
    assert p3.primary_intent == "CREATE_PRESENTATION"
    assert p3.status == "AWAITING_APPROVAL"

    # Test Excel Intent
    p4 = UniversalOperatorEngine.parse_and_plan("create a budget spreadsheet for Q1")
    assert p4.primary_intent == "CREATE_SPREADSHEET"

    # Test Media Intent
    p5 = UniversalOperatorEngine.parse_and_plan("play a dj song on youtube")
    assert p5.primary_intent == "PLAY_MEDIA"

@pytest.mark.asyncio
async def test_real_word_document_creation():
    context = ToolContext(user_id="test", device_id="local", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("complete my assignment on Autonomous Robotics")
    # Verify execution without opening window in test environment
    os.environ["NO_AUTO_OPEN"] = "1"
    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[1].status == "COMPLETED"
    assert "bytes" in executed.steps[1].result
    assert executed.steps[1].result["bytes"] > 0

@pytest.mark.asyncio
async def test_real_powerpoint_presentation_creation():
    context = ToolContext(user_id="test", device_id="local", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("prepare my presentation on Cloud Architecture")
    os.environ["NO_AUTO_OPEN"] = "1"
    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[0].status == "COMPLETED"
    assert executed.steps[0].result["slides_count"] >= 4

@pytest.mark.asyncio
async def test_real_excel_spreadsheet_creation():
    context = ToolContext(user_id="test", device_id="local", platform="windows")
    plan = UniversalOperatorEngine.parse_and_plan("create an expense budget spreadsheet")
    os.environ["NO_AUTO_OPEN"] = "1"
    executed = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    assert executed.status == "COMPLETED"
    assert executed.steps[0].status == "COMPLETED"
    assert executed.steps[0].result["rows_count"] > 0

@pytest.mark.asyncio
async def test_web_research_agent():
    res = await browser_agent.search_and_summarize("Machine Learning")
    assert res["total_found"] >= 1
    assert "findings" in res

def test_ui_operator_bounds_inspection():
    title = ui_operator.get_active_window_title()
    assert isinstance(title, str)

def test_mobile_mesh_synthesis():
    android_intent = mobile_connector.create_android_intent(
        action="android.intent.action.VIEW",
        uri="https://www.youtube.com",
        package="com.google.android.youtube"
    )
    assert android_intent["platform"] == "android"
    assert android_intent["package"] == "com.google.android.youtube"

    ios_link = mobile_connector.create_ios_url_scheme("youtube://watch", {"v": "dQw4w9WgXcQ"})
    assert ios_link["platform"] == "ios"
    assert "youtube://watch?v=" in ios_link["url_scheme"]

