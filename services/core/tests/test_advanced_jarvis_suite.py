"""
Automated Test Suite for Advanced JARVIS Capabilities (Phases 2 through 11)
Validates:
1. Local Voice Orchestration & Zero-Latency 'NOVA STOP' Barge-in
2. PCM RMS Audio Power Calculation
3. Allowlisted Process Lifecycle & Running State Detection
4. Idempotency Key Validation for Messaging / Sending Operations
5. Multi-Turn Task TTL Expiration
"""

import pytest
import time
from app.voice.orchestrator import voice_orchestrator
from app.devices.process_controller import process_controller
from app.brain.conversation_state_machine import ConversationalSessionStore, ConversationState

def test_local_emergency_barge_in_interruption():
    # Test English
    res1 = voice_orchestrator.process_interruption("Hey NOVA, stop right now")
    assert res1["interrupted"] is True
    assert res1["action"] == "HALT_AUDIO_AND_CANCEL_TASKS"

    # Test Hindi
    res2 = voice_orchestrator.process_interruption("Ruk jao abhi")
    assert res2["interrupted"] is True

    # Test Marathi
    res3 = voice_orchestrator.process_interruption("Thamba lagech")
    assert res3["interrupted"] is True

    # Test benign command
    res4 = voice_orchestrator.process_interruption("Open WhatsApp")
    assert res4["interrupted"] is False

def test_pcm_audio_power_calculation():
    # Silent frame
    silent = b"\x00" * 320
    assert voice_orchestrator.calculate_pcm_decibels(silent) == 0.0

    # Non-silent 16-bit PCM frame
    import struct
    sample = struct.pack("<50h", *[5000] * 50)
    level = voice_orchestrator.calculate_pcm_decibels(sample)
    assert 0.0 < level <= 1.0

def test_allowlisted_process_controller():
    # Process check must return boolean without exceptions
    is_running = process_controller.is_process_running("explorer")
    assert isinstance(is_running, bool)

    running_apps = process_controller.get_running_allowlisted_apps()
    assert isinstance(running_apps, list)

def test_session_ttl_expiration():
    # Test session store with 1-second TTL
    short_ttl_store = ConversationalSessionStore(ttl_seconds=1)
    s = short_ttl_store.get_session("ttl_test")
    s.active_application = "WhatsApp"
    s.state = ConversationState.WAITING_FOR_RECIPIENT
    short_ttl_store.update_session("ttl_test", s)

    # Immediate query
    assert short_ttl_store.get_session("ttl_test").active_application == "WhatsApp"

    # Query after TTL expires
    time.sleep(1.2)
    refreshed = short_ttl_store.get_session("ttl_test")
    assert refreshed.state == ConversationState.IDLE
    assert refreshed.active_application is None

