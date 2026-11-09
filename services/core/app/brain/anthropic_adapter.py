import os
import json
import httpx
import logging
from typing import AsyncGenerator
from app.brain.llm_interface import BaseLLMAdapter, LLMMessage, LLMResponse, ToolDefinition

logger = logging.getLogger("nova.brain.anthropic")

class AnthropicAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str | None = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.model = model

    async def chat(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(content=f"NOVA (Anthropic Adapter): {messages[-1].content}")

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        system_prompt = next((m.content for m in messages if m.role == "system"), "")
        user_messages = [m.model_dump() for m in messages if m.role != "system"]

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": user_messages,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = "".join(b.get("text", "") for b in data.get("content", []))
            return LLMResponse(content=text)

    async def chat_stream(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> AsyncGenerator[str, None]:
        res = await self.chat(messages, tools)
        yield res.content

