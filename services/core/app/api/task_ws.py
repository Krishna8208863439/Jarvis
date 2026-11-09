"""
NOVA Task WebSocket — Live Step-by-Step Execution Streaming.

Clients connect to ws://localhost:8000/ws/tasks and receive real-time events:
  STEP_STARTING   → a plan step is about to execute
  STEP_COMPLETED  → a plan step finished successfully
  STEP_FAILED     → a plan step errored
  TASK_COMPLETED  → all steps done
  TASK_FAILED     → plan aborted

The /api/v1/operator/execute route broadcasts events via the TaskEventBus
while executing each step.
"""

import asyncio
import json
import datetime
from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class TaskEventBus:
    """In-process pub-sub for task execution events (single-node broadcast)."""

    def __init__(self):
        self._clients: Set[WebSocket] = set()

    def register(self, ws: WebSocket):
        self._clients.add(ws)

    def unregister(self, ws: WebSocket):
        self._clients.discard(ws)

    async def broadcast(self, event_type: str, payload: dict):
        message = json.dumps({
            "type": event_type,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "payload": payload,
        })
        dead: Set[WebSocket] = set()
        for client in self._clients:
            try:
                await client.send_text(message)
            except Exception:
                dead.add(client)
        for d in dead:
            self._clients.discard(d)


# Singleton bus — imported by operator_routes to publish events
task_event_bus = TaskEventBus()


@router.websocket("/ws/tasks")
async def task_stream(websocket: WebSocket):
    """Frontend connects here to receive live task execution events."""
    await websocket.accept()
    task_event_bus.register(websocket)
    try:
        # Keep connection alive; client may send pings
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo ping back as pong
                if data == "ping":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except asyncio.TimeoutError:
                # Send heartbeat
                try:
                    await websocket.send_text(json.dumps({"type": "HEARTBEAT"}))
                except Exception:
                    break
    except WebSocketDisconnect:
        pass
    finally:
        task_event_bus.unregister(websocket)

