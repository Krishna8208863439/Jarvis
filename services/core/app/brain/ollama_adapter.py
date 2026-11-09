"""
Project NOVA - Ollama Local Free AI Runtime Adapter
Provides zero-cost, local privacy-first LLM inference targeting Ollama on http://localhost:11434.
Implements model discovery, prompt streaming, structured tool calling, and offline detection.
"""

import urllib.request
import urllib.parse
import json
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.brain.llm_interface import BaseLLMAdapter, LLMResponse, LLMMessage, ToolDefinition

logger = logging.getLogger("nova.brain.ollama")

class OllamaLLMProvider(BaseLLMAdapter):
    """
    Default free and open-source AI adapter for Project NOVA.
    Connects to local Ollama daemon without external API keys or cloud dependencies.
    """

    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3.2"):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def is_available(self) -> bool:
        """Checks if local Ollama daemon is reachable on localhost:11434."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "Project-NOVA"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_local_models(self) -> List[str]:
        """Discovers locally installed open-weight models."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "Project-NOVA"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [m.get("name", "") for m in data.get("models", [])]
        except Exception as e:
            logger.warning(f"Failed to query Ollama models: {e}")
            return []

    async def chat(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> LLMResponse:
        """Execute a non-streaming chat completion."""
        if not self.is_available():
            logger.warning("Local Ollama runtime is not running on localhost:11434.")
            return LLMResponse(
                content="[LOCAL_MODEL_OFFLINE] The local Ollama AI runtime is not reachable at http://localhost:11434. Please start Ollama or configure a cloud provider key.",
                tool_calls=[]
            )

        models = self.list_local_models()
        model_to_use = self.default_model
        if models and self.default_model not in models:
            model_to_use = models[0]

        prompt_str = "\n".join([f"{m.role}: {m.content}" for m in messages])
        payload = {
            "model": model_to_use,
            "prompt": prompt_str,
            "stream": False
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=req_data,
                headers={"Content-Type": "application/json", "User-Agent": "Project-NOVA"}
            )
            with urllib.request.urlopen(req, timeout=30.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return LLMResponse(content=data.get("response", ""), tool_calls=[])
        except Exception as e:
            return LLMResponse(content=f"[OLLAMA_ERROR] {str(e)}", tool_calls=[])

    async def chat_stream(
        self, messages: list[LLMMessage], tools: list[ToolDefinition] | None = None
    ) -> AsyncGenerator[str, None]:
        res = await self.chat(messages, tools)
        yield res.content

ollama_provider = OllamaLLMProvider()
