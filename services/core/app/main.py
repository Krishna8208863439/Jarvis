import datetime
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.voice_routes import router as voice_router
from app.api.intent_routes import router as intent_router
from app.api.operator_routes import router as operator_router
from app.api.task_ws import router as task_ws_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NOVA Universal AI Assistant Core Orchestration API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router)
app.include_router(intent_router)
app.include_router(operator_router)
app.include_router(task_ws_router)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": "0.1.0",
    }

@app.get("/api/v1/system/status")
async def system_status():
    return {
        "engine": "active",
        "registered_devices_count": 0,
        "active_sessions": 0,
        "database": "configured",
    }

