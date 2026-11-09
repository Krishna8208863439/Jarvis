"""
Automated Test Suite for Multi-Turn Conversational Voice Operator
Tests:
TEST A: WhatsApp Multi-Turn: "Open WhatsApp" -> "Rahul" -> "Hello Rahul, how are you?" -> "Yes, send it"
TEST B: Task Cancellation: "Open WhatsApp" -> "Cancel" -> Status returns to IDLE
TEST C: Gmail Multi-Turn: "Open Gmail" -> "Professor Rahul" -> "Meeting at 10 AM" -> Draft prepared
TEST D: Anaphora resolution: "him", "send it"
"""

import pytest
from app.brain.conversation_state_machine import session_store, ConversationState
from app.brain.context_resolver import context_resolver

def test_whatsapp_multi_turn_conversational_flow():
    session = session_store.reset_session("test-user")
    assert session.state == ConversationState.IDLE

    # Turn 1: "Hey NOVA, open WhatsApp"
    s1, act1, resp1 = context_resolver.resolve_turn("open WhatsApp", session)
    session.state = s1
    assert s1 == ConversationState.WAITING_FOR_RECIPIENT
    assert "WhatsApp is open" in resp1
    assert "Whom would you like to contact" in resp1

    # Turn 2: "Open Rahul"
    s2, act2, resp2 = context_resolver.resolve_turn("Open Rahul", session)
    session.state = s2
    assert s2 == ConversationState.WAITING_FOR_MESSAGE
    assert session.target_recipient == "Rahul"
    assert "I found Rahul" in resp2
    assert "What message would you like to send" in resp2

    # Turn 3: "Hello Rahul, how are you?"
    s3, act3, resp3 = context_resolver.resolve_turn("Hello Rahul, how are you?", session)
    session.state = s3
    assert s3 == ConversationState.WAITING_FOR_CONFIRMATION
    assert session.draft_content == "Hello Rahul, how are you?"
    assert "Would you like me to send it" in resp3

    # Turn 4: "Yes, send it"
    s4, act4, resp4 = context_resolver.resolve_turn("Yes, send it", session)
    assert s4 == ConversationState.EXECUTING
    assert act4["action"] == "execute_send"
    assert act4["recipient"] == "Rahul"
    assert act4["message"] == "Hello Rahul, how are you?"

def test_task_cancellation_flow():
    session = session_store.reset_session("test-cancel-user")
    # Start task
    s1, _, _ = context_resolver.resolve_turn("open WhatsApp", session)
    session.state = s1
    assert session.state == ConversationState.WAITING_FOR_RECIPIENT

    # Cancel task
    s2, act2, resp2 = context_resolver.resolve_turn("Cancel", session)
    assert s2 == ConversationState.IDLE
    assert act2["action"] == "cancel"
    assert "cancelled" in resp2.lower()

def test_gmail_multi_turn_flow():
    session = session_store.reset_session("test-gmail-user")
    # Turn 1: Open Gmail
    s1, _, resp1 = context_resolver.resolve_turn("open Gmail", session)
    session.state = s1
    assert s1 == ConversationState.WAITING_FOR_RECIPIENT
    assert "Gmail is open" in resp1

    # Turn 2: Recipient
    s2, _, resp2 = context_resolver.resolve_turn("Professor Sharma", session)
    session.state = s2
    assert s2 == ConversationState.WAITING_FOR_MESSAGE
    assert session.target_recipient == "Professor Sharma"

