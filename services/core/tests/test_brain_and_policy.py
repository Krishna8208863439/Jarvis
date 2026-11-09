import pytest
from app.brain.openai_adapter import OpenAIAdapter
from app.brain.anthropic_adapter import AnthropicAdapter
from app.brain.llm_interface import LLMMessage
from app.tools.registry import registry
from app.tools.standard_tools import InternetSearchJobsTool, DeleteFileTool
from app.tools.base_tool import ToolContext
from app.policy.engine import PolicyViolationError
from app.memory.store import memory_store

# Register tools
registry.register(InternetSearchJobsTool())
registry.register(DeleteFileTool())

@pytest.mark.asyncio
async def test_llm_adapters_fallback_chat():
    openai = OpenAIAdapter()
    resp = await openai.chat([LLMMessage(role="user", content="Hey NOVA")])
    assert "Hello! I'm here." in resp.content

    anthropic = AnthropicAdapter()
    resp2 = await anthropic.chat([LLMMessage(role="user", content="Test prompt")])
    assert "NOVA (Anthropic Adapter)" in resp2.content

@pytest.mark.asyncio
async def test_tier_0_safe_tool_execution():
    context = ToolContext(user_id="u1", device_id="d1", platform="all")
    res = await registry.execute_tool(
        "internet.search_jobs", {"query": "python developer"}, context
    )
    assert res.success is True
    assert len(res.data["jobs"]) > 0

@pytest.mark.asyncio
async def test_tier_3_voice_only_rejection_policy():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows", voice_only_auth=True)
    with pytest.raises(PolicyViolationError) as exc_info:
        await registry.execute_tool(
            "desktop.delete_file", {"path": "C:\\temp\\file.txt"}, context, is_confirmed=False
        )
    assert "Voice-only confirmation is strictly prohibited" in str(exc_info.value)

@pytest.mark.asyncio
async def test_tier_3_confirmed_execution():
    context = ToolContext(user_id="u1", device_id="d1", platform="windows", voice_only_auth=False)
    res = await registry.execute_tool(
        "desktop.delete_file", {"path": "C:\\temp\\file.txt"}, context, is_confirmed=True
    )
    assert res.success is True
    assert res.data["deleted_path"] == "C:\\temp\\file.txt"

def test_memory_store_user_approval_constraint():
    with pytest.raises(ValueError) as exc:
        memory_store.set_memory("fav_color", "blue", user_approved=False)
    assert "without explicit user approval" in str(exc.value)

    item = memory_store.set_memory("name", "Krishna", user_approved=True)
    assert item.value == "Krishna"
    assert memory_store.get_memory("name").value == "Krishna"
    assert memory_store.delete_memory("name") is True

