"""
Project NOVA - Universal Context & Multi-Turn Anaphora Resolver
Resolves references like 'him', 'send it', 'open Rahul', 'type this'
against the active ConversationState and session TaskContext.
"""

import re
import logging
from typing import Tuple, Optional, Dict, Any
from app.brain.conversation_state_machine import ConversationState, TaskContext

logger = logging.getLogger("nova.brain.context_resolver")

class ConversationalContextResolver:
    """
    Evaluates spoken voice inputs in the context of the current task state.
    Translates colloquial follow-ups into structured state transitions.
    """

    @staticmethod
    def resolve_turn(prompt: str, ctx: TaskContext) -> Tuple[ConversationState, Dict[str, Any], str]:
        """
        Returns:
            Tuple of (Next ConversationState, Action Data Dictionary, Spoken Voice Response)
        """
        p = prompt.strip()
        lower = p.lower()

        # Global Emergency / Cancellation check
        if lower in ["cancel", "cancel it", "cancel this task", "stop", "never mind", "abort"]:
            ctx.state = ConversationState.CANCELLED
            return ConversationState.IDLE, {"action": "cancel"}, "Task cancelled. What else can I do for you?"

        # -------------------------------------------------------------
        # STATE: WAITING_FOR_RECIPIENT (e.g. WhatsApp, Email)
        # -------------------------------------------------------------
        if ctx.state == ConversationState.WAITING_FOR_RECIPIENT:
            recipient = p
            # Strip verbal filler
            for prefix in ["open ", "contact ", "to ", "message ", "send to "]:
                if recipient.lower().startswith(prefix):
                    recipient = recipient[len(prefix):].strip()

            recipient = recipient.rstrip(".?")
            ctx.target_recipient = recipient
            ctx.state = ConversationState.WAITING_FOR_MESSAGE
            return (
                ConversationState.WAITING_FOR_MESSAGE,
                {"action": "set_recipient", "recipient": recipient},
                f"I found {recipient}. What message would you like to send?"
            )

        # -------------------------------------------------------------
        # STATE: WAITING_FOR_MESSAGE
        # -------------------------------------------------------------
        if ctx.state == ConversationState.WAITING_FOR_MESSAGE:
            message = p
            for prefix in ["send him a message saying ", "send her a message saying ", "send message saying ", "type ", "saying "]:
                if message.lower().startswith(prefix):
                    message = message[len(prefix):].strip()

            message = message.strip('"\'')
            ctx.draft_content = message
            ctx.state = ConversationState.WAITING_FOR_CONFIRMATION
            return (
                ConversationState.WAITING_FOR_CONFIRMATION,
                {"action": "draft_message", "recipient": ctx.target_recipient, "message": message},
                f"Your message to {ctx.target_recipient} is: '{message}'. Would you like me to send it?"
            )

        # -------------------------------------------------------------
        # STATE: WAITING_FOR_CONFIRMATION
        # -------------------------------------------------------------
        if ctx.state == ConversationState.WAITING_FOR_CONFIRMATION:
            clean_cmd = re.sub(r"[^a-zA-Z0-9\s]", "", lower).strip()
            confirm_phrases = ["yes", "send it", "yes send it", "send", "confirm", "send now", "haan bhej do", "pathva", "do it", "sure", "proceed"]
            if clean_cmd in confirm_phrases or any(phrase in clean_cmd for phrase in ["send it", "yes send", "confirm"]):
                ctx.state = ConversationState.EXECUTING
                return (
                    ConversationState.EXECUTING,
                    {"action": "execute_send", "recipient": ctx.target_recipient, "message": ctx.draft_content},
                    "Sending your message now."
                )
            elif clean_cmd in ["no", "dont send", "change it", "edit it", "cancel"]:
                ctx.state = ConversationState.WAITING_FOR_MESSAGE
                return (
                    ConversationState.WAITING_FOR_MESSAGE,
                    {"action": "edit_message"},
                    "Understood. What would you like the message to say instead?"
                )

        # -------------------------------------------------------------
        # DEFAULT / INITIAL INTENT IDENTIFICATION (STATE == IDLE)
        # -------------------------------------------------------------
        # WhatsApp Interactive Flow (e.g. "open whatsapp", "send whatsapp message")
        if "whatsapp" in lower:
            ctx.active_application = "WhatsApp"
            ctx.state = ConversationState.WAITING_FOR_RECIPIENT
            return (
                ConversationState.WAITING_FOR_RECIPIENT,
                {"action": "open_app", "app": "WhatsApp"},
                "WhatsApp is open. Whom would you like to contact?"
            )

        # Gmail / Email Interactive Flow (e.g. "open gmail", "send email")
        if lower.startswith("open gmail") or lower.startswith("send email") or lower.startswith("write email") or lower == "gmail" or lower == "email":
            ctx.active_application = "Gmail"
            ctx.state = ConversationState.WAITING_FOR_RECIPIENT
            return (
                ConversationState.WAITING_FOR_RECIPIENT,
                {"action": "open_app", "app": "Gmail"},
                "Gmail is open. Whom would you like to email?"
            )

        # Word Document App Opening (Only when specifically asking to open Word application)
        if lower in ["open word", "open ms word", "launch word", "open microsoft word", "word"]:
            ctx.active_application = "Word"
            ctx.state = ConversationState.WAITING_FOR_CONTENT
            return (
                ConversationState.WAITING_FOR_CONTENT,
                {"action": "open_app", "app": "Word"},
                "Word is open. What document would you like me to create?"
            )

        # Excel Spreadsheet App Opening (Only when specifically asking to open Excel)
        if lower in ["open excel", "open ms excel", "launch excel", "open microsoft excel", "excel"]:
            ctx.active_application = "Excel"
            ctx.state = ConversationState.WAITING_FOR_CONTENT
            return (
                ConversationState.WAITING_FOR_CONTENT,
                {"action": "open_app", "app": "Excel"},
                "Excel is open. What spreadsheet should I prepare?"
            )

        # VS Code Developer Flow
        if lower in ["open vs code", "open vscode", "launch vscode", "launch vs code", "vscode", "vs code"]:
            ctx.active_application = "VS Code"
            ctx.state = ConversationState.WAITING_FOR_CONTENT
            return (
                ConversationState.WAITING_FOR_CONTENT,
                {"action": "open_app", "app": "VS Code"},
                "VS Code is open. Which project would you like to work on?"
            )

        # Not in a multi-turn slot: return None to allow standard UniversalOperatorEngine
        return ConversationState.IDLE, {}, ""

context_resolver = ConversationalContextResolver()
