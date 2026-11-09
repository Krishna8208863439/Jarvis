import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.voice.stt_interface import STTResult
from app.voice.tts_interface import TTSRequest
from app.voice.elevenlabs_provider import ElevenLabsTTSProvider

logger = logging.getLogger("nova.voice.ws")
router = APIRouter()
tts_provider = ElevenLabsTTSProvider(api_key="demo_key")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Active: {len(self.active_connections)}")

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_voice_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive either binary audio frames (PCM/Opus) or JSON control messages
            message = await websocket.receive()
            if "bytes" in message and message["bytes"]:
                audio_bytes = message["bytes"]
                # In real streaming, audio_bytes is forwarded to the active STT provider
                # Send back real-time transcript acknowledgment
                response = {
                    "type": "TRANSCRIPT_PARTIAL",
                    "payload": {
                        "text": "",
                        "is_final": False,
                        "bytes_received": len(audio_bytes)
                    }
                }
                await websocket.send_text(json.dumps(response))

            elif "text" in message and message["text"]:
                data = json.loads(message["text"])
                msg_type = data.get("type")

                if msg_type == "SPEECH_TRANSCRIPT":
                    # Spoken transcript received from client VAD/WebSpeech or native STT
                    transcript_text = data.get("payload", {}).get("text", "")
                    language = data.get("payload", {}).get("language", "en")
                    is_final = data.get("payload", {}).get("is_final", True)

                    # Broadcast back confirmation and prepare AI brain execution
                    await websocket.send_text(json.dumps({
                        "type": "TRANSCRIPT_FINAL" if is_final else "TRANSCRIPT_PARTIAL",
                        "payload": {
                            "text": transcript_text,
                            "language": language,
                            "is_final": is_final
                        }
                    }))

                elif msg_type == "TTS_REQUEST":
                    # Generate speech audio response
                    text_to_speak = data.get("payload", {}).get("text", "")
                    lang = data.get("payload", {}).get("language", "en")
                    gender = data.get("payload", {}).get("gender", "female")
                    speed = data.get("payload", {}).get("speed", 1.0)

                    tts_req = TTSRequest(text=text_to_speak, language=lang, gender=gender, speed=speed)
                    audio_data = await tts_provider.synthesize(tts_req)

                    await websocket.send_text(json.dumps({
                        "type": "TTS_AUDIO_START",
                        "payload": {"text": text_to_speak, "bytes_length": len(audio_data)}
                    }))
                    await websocket.send_bytes(audio_data)

                elif msg_type == "EMERGENCY_STOP":
                    logger.warning("EMERGENCY STOP (NOVA STOP) received over WebSocket")
                    await websocket.send_text(json.dumps({
                        "type": "STATE_CHANGE",
                        "payload": {"state": "IDLE"}
                    }))

            elif "type" in message and message["type"] == "websocket.disconnect":
                break
                    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.debug(f"WebSocket session ended: {e}")
    finally:
        manager.disconnect(websocket)

