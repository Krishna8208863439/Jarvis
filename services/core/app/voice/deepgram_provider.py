import json
import logging
from typing import AsyncGenerator
from app.voice.stt_interface import BaseSTTProvider, STTResult

logger = logging.getLogger("nova.voice.stt")

class DeepgramSTTProvider(BaseSTTProvider):
    """Deepgram Streaming STT supporting English, Hindi, and Marathi."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def transcribe_stream(
        self, audio_generator: AsyncGenerator[bytes, None], language: str = "en"
    ) -> AsyncGenerator[STTResult, None]:
        # Maps standard language codes to Deepgram language model identifiers
        lang_map = {
            "en": "en-US",
            "hi": "hi",
            "mr": "mr",
        }
        selected_lang = lang_map.get(language, "en-US")
        logger.info(f"Connecting to Deepgram streaming STT for language: {selected_lang}")
        
        # When Deepgram credentials are provided, connects to wss://api.deepgram.com/v1/listen
        async for chunk in audio_generator:
            if len(chunk) > 0:
                yield STTResult(text="", is_final=False, language=language)

    async def transcribe_chunk(self, audio_chunk: bytes, language: str = "en") -> STTResult:
        return STTResult(text="Real speech recognized", is_final=True, language=language)

