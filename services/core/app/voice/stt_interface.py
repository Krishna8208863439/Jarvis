import abc
from typing import AsyncGenerator
from pydantic import BaseModel

class STTResult(BaseModel):
    text: str
    is_final: bool
    language: str
    confidence: float = 1.0

class BaseSTTProvider(abc.ABC):
    @abc.abstractmethod
    async def transcribe_stream(
        self, audio_generator: AsyncGenerator[bytes, None], language: str
    ) -> AsyncGenerator[STTResult, None]:
        """Stream transcription of PCM/Opus audio chunks."""
        pass

    @abc.abstractmethod
    async def transcribe_chunk(self, audio_chunk: bytes, language: str) -> STTResult:
        """Transcribe a single audio frame."""
        pass

