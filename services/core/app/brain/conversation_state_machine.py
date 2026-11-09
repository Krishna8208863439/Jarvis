"""
Project NOVA - Universal Conversational Task State Machine
Maintains state across multiple voice turns for interactive application control,
including WhatsApp, Email, Word, Excel, VS Code, and general operating tasks.
"""

import time
import logging
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

logger = logging.getLogger("nova.brain.state_machine")

class ConversationState(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    UNDERSTANDING = "UNDERSTANDING"
    ASKING_CLARIFICATION = "ASKING_CLARIFICATION"
    WAITING_FOR_APPLICATION = "WAITING_FOR_APPLICATION"
    WAITING_FOR_RECIPIENT = "WAITING_FOR_RECIPIENT"
    WAITING_FOR_MESSAGE = "WAITING_FOR_MESSAGE"
    WAITING_FOR_CONTENT = "WAITING_FOR_CONTENT"
    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"

class TaskContext(BaseModel):
    task_id: str
    active_application: Optional[str] = None
    target_recipient: Optional[str] = None
    draft_content: Optional[str] = None
    subject: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    state: ConversationState = ConversationState.IDLE
    last_turn_timestamp: float = Field(default_factory=time.time)
    turn_count: int = 0
    history: List[Dict[str, str]] = Field(default_factory=list)

class ConversationalSessionStore:
    """In-memory persistent store for active user multi-turn voice sessions."""
    def __init__(self, ttl_seconds: int = 300):
        self._sessions: Dict[str, TaskContext] = {}
        self.ttl = ttl_seconds

    def get_session(self, session_id: str = "default-user") -> TaskContext:
        now = time.time()
        if session_id in self._sessions:
            ctx = self._sessions[session_id]
            # Reset if expired
            if now - ctx.last_turn_timestamp > self.ttl:
                logger.info(f"Session {session_id} expired. Resetting to IDLE.")
                return self.reset_session(session_id)
            return ctx

        # Create new context
        ctx = TaskContext(task_id=f"task-{int(now)}", state=ConversationState.IDLE)
        self._sessions[session_id] = ctx
        return ctx

    def update_session(self, session_id: str, ctx: TaskContext):
        ctx.last_turn_timestamp = time.time()
        ctx.turn_count += 1
        self._sessions[session_id] = ctx

    def reset_session(self, session_id: str = "default-user") -> TaskContext:
        ctx = TaskContext(task_id=f"task-{int(time.time())}", state=ConversationState.IDLE)
        self._sessions[session_id] = ctx
        return ctx

session_store = ConversationalSessionStore()

