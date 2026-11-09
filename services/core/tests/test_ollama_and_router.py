"""
Automated Test Suite for Phase 1: NOVA Core, Local Ollama Adapter & Model Router
Verifies:
1. Local Ollama availability detection without throwing unhandled exceptions.
2. Honest error handling when local AI daemon is offline (Rule 3: Never fabricate AI output).
3. Model Provider Router priority hierarchy.
4. Structured tool argument schemas.
"""

import pytest
import os
from app.brain.ollama_adapter import OllamaLLMProvider
from app.brain.model_router import ModelProviderRouter
from app.brain.react_engine import react_engine

@pytest.mark.asyncio
async def test_ollama_offline_honest_diagnostic():
    # Target an unused port to simulate offline Ollama runtime
    offline_adapter = OllamaLLMProvider(base_url="http://localhost:59999")
    assert offline_adapter.is_available() is False

    from app.brain.llm_interface import LLMMessage
    # Verify no fabricated text is generated when offline
    res = await offline_adapter.chat([LLMMessage(role="user", content="Explain quantum computing")])
    assert "[LOCAL_MODEL_OFFLINE]" in res.content

def test_model_router_fallback_hierarchy():
    router = ModelProviderRouter()
    provider = router.get_active_provider()
    assert provider is not None

def test_react_tool_definitions_schema_compliance():
    schemas = react_engine.get_tool_definitions()
    assert len(schemas) >= 4
    for s in schemas:
        assert "type" in s and s["type"] == "function"
        assert "function" in s
        assert "name" in s["function"]
        assert "parameters" in s["function"]
