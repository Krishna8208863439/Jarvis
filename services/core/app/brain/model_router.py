"""
Project NOVA - Model Provider Router
Priority Hierarchy:
1. Local Ollama (if reachable on port 11434) - Free & Open Source Default
2. OpenAI (if OPENAI_API_KEY environment variable is configured)
3. Anthropic (if ANTHROPIC_API_KEY environment variable is configured)
4. Offline Diagnostic Handler - Never fabricates fake AI responses
"""

import os
import logging
from typing import Dict, Any, List, Optional
from app.brain.llm_interface import BaseLLMAdapter, LLMResponse, LLMMessage
from app.brain.ollama_adapter import ollama_provider
from app.brain.openai_adapter import OpenAIAdapter
from app.brain.anthropic_adapter import AnthropicAdapter

logger = logging.getLogger("nova.brain.router")

class ModelProviderRouter:
    """Dynamically routes requests to the best available free local or configured cloud AI model."""

    def __init__(self):
        self.ollama = ollama_provider
        self.openai = OpenAIAdapter(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.anthropic = AnthropicAdapter(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    def get_active_provider(self) -> BaseLLMAdapter:
        """Returns the active provider following the strict open-source priority rules."""
        # 1. Prefer local free Ollama runtime
        if self.ollama.is_available():
            logger.info("Using local Ollama AI runtime.")
            return self.ollama

        # 2. Check OpenAI cloud key
        if os.environ.get("OPENAI_API_KEY"):
            logger.info("Using OpenAI cloud provider.")
            return self.openai

        # 3. Check Anthropic cloud key
        if os.environ.get("ANTHROPIC_API_KEY"):
            logger.info("Using Anthropic cloud provider.")
            return self.anthropic

        # 4. Fallback: Ollama provider which will honestly return [LOCAL_MODEL_OFFLINE]
        return self.ollama

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> LLMResponse:
        provider = self.get_active_provider()
        return await provider.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            tools=tools
        )

model_router = ModelProviderRouter()
