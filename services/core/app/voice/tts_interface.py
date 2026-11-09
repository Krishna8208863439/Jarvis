import abc
from typing import AsyncGenerator
from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    language: str = "en"       # "en", "hi", "mr"
    gender: str = "female"     # "female", "male"
    speed: float = 1.0         # 0.5 to 2.0
    volume: float = 1.0

class TTSAudioChunk(BaseModel):
    audio_bytes: bytes
    is_final: bool
    format: str = "mp3"

class BaseTTSProvider(abc.ABC):
    @abc.abstractmethod
    async def synthesize_stream(self, request: TTSRequest) -> AsyncGenerator[bytes, None]:
        """Synthesize speech into a stream of audio chunks."""
        pass

    @abc.abstractmethod
    async def synthesize(self, request: TTSRequest) -> bytes:
        """Synthesize speech into a complete audio buffer."""
        pass

