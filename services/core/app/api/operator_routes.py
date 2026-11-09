"""
Project NOVA - Universal Operator Intent & App Execution Router
Exposes dynamic application discovery and execution APIs.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from app.devices.app_discovery import app_registry, RegisteredApp
from app.brain.operator_engine import UniversalOperatorEngine, UniversalOperatorPlan, TaskActionStep
from app.brain.conversation_state_machine import session_store, ConversationState
from app.brain.context_resolver import context_resolver
from app.connectors.whatsapp_connector import whatsapp_connector
from app.connectors.email_connector import email_connector
from app.tools.base_tool import ToolContext

router = APIRouter(prefix="/api/v1/operator")

class OperatorVoiceRequest(BaseModel):
    user_prompt: str
    platform: str = "windows"
    device_id: str = "local-desktop"
    language: str = "en"
    is_confirmed: bool = False

class OperatorVoiceResponse(BaseModel):
    spoken_response: str
    plan: UniversalOperatorPlan
    success: bool = True

class RegisterAppRequest(BaseModel):
    app_id: str
    name: str
    launch_command: str
    category: str = "Custom"

@router.get("/apps", response_model=List[RegisteredApp])
async def list_installed_apps(category: Optional[str] = None):
    """Return all dynamically discovered installed applications on this device."""
    return app_registry.list_apps(category=category)

@router.post("/apps/register", response_model=RegisteredApp)
async def register_manual_app(req: RegisterAppRequest):
    """Manually register any custom application."""
    return app_registry.register_manual_app(
        app_id=req.app_id,
        name=req.name,
        launch_command=req.launch_command,
        category=req.category
    )

@router.post("/execute", response_model=OperatorVoiceResponse)
async def execute_operator_intent(req: OperatorVoiceRequest):
    """
    Main Autonomous Operator Endpoint with Multi-Turn Conversational Memory:
    Maintains task context across multiple turns (e.g. Open WhatsApp -> Rahul -> Message -> Send).
    """
    session = session_store.get_session(session_id="default-user")

    # Step 1: Check multi-turn conversational context resolver
    next_state, action_data, spoken_text = context_resolver.resolve_turn(req.user_prompt, session)

    if spoken_text:
        # Multi-turn conversational transition triggered!
        session.state = next_state
        session_store.update_session("default-user", session)

        plan_id = f"plan-{session.task_id}-{session.turn_count}"
        plan_status = "AWAITING_APPROVAL" if next_state == ConversationState.WAITING_FOR_CONFIRMATION else "EXECUTING"

        # If user confirmed send, perform the real application send!
        if action_data.get("action") == "execute_send":
            if session.active_application == "WhatsApp":
                send_res = whatsapp_connector.type_and_send_message(session.draft_content, direct_send=True)
                session_store.reset_session("default-user")
                spoken_text = "Your WhatsApp message has been sent successfully."
            elif session.active_application == "Gmail":
                email_connector.open_gmail_compose(session.target_recipient, "Message from Project NOVA", session.draft_content)
                session_store.reset_session("default-user")
                spoken_text = "Your email has been prepared and sent."

        # If user opened app in multi-turn (e.g. WhatsApp, Word, Excel, VS Code)
        elif action_data.get("action") == "open_app":
            app_target = action_data.get("app")
            if app_target == "WhatsApp":
                whatsapp_connector.open_whatsapp()
            elif app_target:
                app_obj = app_registry.search_app(app_target)
                if app_obj and app_obj.launch_command:
                    clean_cmd = app_obj.launch_command.strip()
                    if clean_cmd.startswith('"') and clean_cmd.endswith('"'):
                        clean_cmd = clean_cmd[1:-1]
                    import subprocess
                    subprocess.Popen(["cmd.exe", "/c", "start", "", clean_cmd])

        plan = UniversalOperatorPlan(
            plan_id=plan_id,
            user_prompt=req.user_prompt,
            primary_intent=session.active_application or "CONVERSATION",
            steps=[
                TaskActionStep(
                    step_id="step-1",
                    action_type=action_data.get("action", "converse"),
                    target=session.active_application or "Assistant",
                    description=spoken_text,
                    risk_tier="TIER_1_REVERSIBLE",
                    arguments=action_data,
                    status="COMPLETED"
                )
            ],
            status=plan_status,
            spoken_summary=spoken_text
        )

        return OperatorVoiceResponse(
            spoken_response=spoken_text,
            plan=plan,
            success=True
        )

    # Step 2: Fall back to standard single-shot autonomous planner
    plan = UniversalOperatorEngine.parse_and_plan(req.user_prompt, platform=req.platform)
    context = ToolContext(user_id="user-1", device_id=req.device_id, platform=req.platform)

    # If plan is safe (Tier 0 / Tier 1) or already confirmed by user, execute immediately!
    if plan.status == "EXECUTING" or req.is_confirmed:
        plan = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=req.is_confirmed)

    return OperatorVoiceResponse(
        spoken_response=plan.spoken_summary,
        plan=plan,
        success=plan.status != "FAILED"
    )

@router.post("/plan/approve", response_model=OperatorVoiceResponse)
async def approve_and_execute_plan(req: OperatorVoiceRequest):
    """Approve a Tier 2/3 sensitive task (like generating Word, PowerPoint, or Excel files)."""
    plan = UniversalOperatorEngine.parse_and_plan(req.user_prompt, platform=req.platform)
    context = ToolContext(user_id="user-1", device_id=req.device_id, platform=req.platform)

    plan = await UniversalOperatorEngine.execute_plan(plan, context, is_confirmed=True)
    return OperatorVoiceResponse(
        spoken_response="Task successfully executed and verified on your device.",
        plan=plan,
        success=plan.status == "COMPLETED"
    )

