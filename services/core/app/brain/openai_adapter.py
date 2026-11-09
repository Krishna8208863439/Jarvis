import os
import json
import httpx
import logging
from typing import AsyncGenerator
from app.brain.llm_interface import BaseLLMAdapter, LLMMessage, LLMResponse, ToolDefinition

logger = logging.getLogger("nova.brain.openai")

class OpenAIAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    async def chat(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> LLMResponse:
        # Fallback response if no external API key is provided
        if not self.api_key:
            last_msg = messages[-1].content.lower()
            if "hello" in last_msg or "hey" in last_msg:
                return LLMResponse(content="Hello! I'm here. What can I do for you?")
            if "python" in last_msg and "job" in last_msg:
                return LLMResponse(
                    content="Sure! I'll search for suitable fresher opportunities.",
                    tool_calls=[{"name": "internet.search_jobs", "arguments": {"query": "python developer fresher"}}]
                )
            return LLMResponse(content=f"NOVA received your command: {messages[-1].content}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
        }
        if tools:
            payload["tools"] = [{"type": "function", "function": t.model_dump()} for t in tools]

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]["message"]
            return LLMResponse(
                content=choice.get("content") or "",
                tool_calls=choice.get("tool_calls", [])
            )

    async def chat_stream(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> AsyncGenerator[str, None]:
        res = await self.chat(messages, tools)
        for token in res.content.split(" "):
            yield token + " "

