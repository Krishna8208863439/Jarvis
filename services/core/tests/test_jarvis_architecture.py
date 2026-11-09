"""
Automated Test Suite for Real-World JARVIS Core Architecture (Phases 0 through 11)
Tests:
1. ReAct Dual-LLM Structured Tool Calling & Decomposition
2. Accessibility Tree Window & Control Inspection
3. Multi-Turn Conversational Memory & Disambiguation
4. Verified In-App Document & Office Tool Operations
5. Multi-Device Mesh Intent Scaffolding
"""

import pytest
import os
import asyncio
from app.brain.react_engine import react_engine
from app.tools.base_tool import ToolContext
from app.devices.accessibility_inspector import accessibility_inspector
from app.brain.conversation_state_machine import session_store, ConversationState
from app.brain.context_resolver import context_resolver

@pytest.mark.asyncio
async def test_react_reasoning_and_tool_execution():
    context = ToolContext(user_id="jarvis_user", device_id="desktop_primary", platform="windows")
    os.environ["NO_AUTO_OPEN"] = "1"

    # Goal that triggers ReAct decomposition to productivity.create_word_document
    result = await react_engine.reason_and_execute("complete my assignment on Neural Systems", context)

    assert result.completed is True
    assert len(result.steps) >= 2
    assert result.steps[1].action_tool == "productivity.create_word_document"
    assert "Word document successfully created" in result.final_answer

def test_accessibility_tree_inspection():
    controls = accessibility_inspector.inspect_active_window_controls()
    assert isinstance(controls, list)

def test_full_conversational_turn_sequence():
    session = session_store.reset_session("jarvis_test_session")

    # Turn 1: "Hey NOVA, open WhatsApp"
    s1, act1, resp1 = context_resolver.resolve_turn("open WhatsApp", session)
    session.state = s1
    assert s1 == ConversationState.WAITING_FOR_RECIPIENT

    # Turn 2: "Rahul"
    s2, act2, resp2 = context_resolver.resolve_turn("Rahul", session)
    session.state = s2
    assert s2 == ConversationState.WAITING_FOR_MESSAGE
    assert session.target_recipient == "Rahul"

    # Turn 3: "Are you coming to the lab?"
    s3, act3, resp3 = context_resolver.resolve_turn("Are you coming to the lab?", session)
    session.state = s3
    assert s3 == ConversationState.WAITING_FOR_CONFIRMATION
    assert session.draft_content == "Are you coming to the lab?"

    # Turn 4: "Yes, send it"
    s4, act4, resp4 = context_resolver.resolve_turn("Yes, send it", session)
    assert s4 == ConversationState.EXECUTING
    assert act4["action"] == "execute_send"

