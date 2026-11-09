import pytest
from starlette.testclient import TestClient
from app.main import app

def test_tts_request_over_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({
            "type": "TTS_REQUEST",
            "payload": {
                "text": "Hello, I am NOVA.",
                "language": "en",
                "gender": "female",
                "speed": 1.0
            }
        })
        ack_data = websocket.receive_json()
        assert ack_data["type"] == "TTS_AUDIO_START"
        assert ack_data["payload"]["text"] == "Hello, I am NOVA."
        audio_chunk = websocket.receive_bytes()
        assert len(audio_chunk) > 0

def test_emergency_stop_over_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({
            "type": "EMERGENCY_STOP"
        })
        data = websocket.receive_json()
        assert data["type"] == "STATE_CHANGE"
        assert data["payload"]["state"] == "IDLE"

