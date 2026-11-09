"""
Project NOVA - Universal Email & Gmail Voice Automation Connector
Handles compose window focus, recipient and subject filling,
message drafting, review preview, and verified sending.
"""

import webbrowser
import urllib.parse
import time
import logging
from typing import Dict, Any, Optional
from app.devices.ui_operator import ui_operator

logger = logging.getLogger("nova.connectors.email")

class EmailConnector:
    """
    Connects NOVA voice commands to Gmail and Desktop Mail applications,
    orchestrating recipient, subject, and body draft composition.
    """

    @staticmethod
    def open_gmail_compose(recipient: str = "", subject: str = "", body: str = "") -> Dict[str, Any]:
        """Opens Gmail with recipient, subject, and body prefilled."""
        logger.info(f"Composing Gmail to '{recipient}' with subject '{subject}'")
        encoded_sub = urllib.parse.quote_plus(subject)
        encoded_body = urllib.parse.quote_plus(body)
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={encoded_sub}&body={encoded_body}"
        webbrowser.open(url)
        return {
            "status": "COMPOSE_OPENED",
            "provider": "Gmail",
            "recipient": recipient,
            "subject": subject,
            "body": body
        }

    @staticmethod
    def send_system_mail(recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """Dispatches via system mailto: protocol handler."""
        encoded_sub = urllib.parse.quote_plus(subject)
        encoded_body = urllib.parse.quote_plus(body)
        url = f"mailto:{recipient}?subject={encoded_sub}&body={encoded_body}"
        webbrowser.open(url)
        return {
            "status": "MAILTO_DISPATCHED",
            "recipient": recipient,
            "subject": subject
        }

email_connector = EmailConnector()

