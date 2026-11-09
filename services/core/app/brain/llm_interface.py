import abc
from typing import AsyncGenerator
from pydantic import BaseModel, Field

class LLMMessage(BaseModel):
    role: str # "system", "user", "assistant"
    content: str

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict

class LLMResponse(BaseModel):
    content: str
    tool_calls: list[dict] = Field(default_factory=list)

class BaseLLMAdapter(abc.ABC):
    @abc.abstractmethod
    async def chat(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> LLMResponse:
        """Execute a non-streaming chat completion."""
        pass

    @abc.abstractmethod
    async def chat_stream(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> AsyncGenerator[str, None]:
        """Execute a streaming chat completion."""
        pass

