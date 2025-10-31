"""
Health Check API Router (v0.3)
Provides health and status endpoints
"""
from fastapi import APIRouter
from datetime import datetime
from config import config

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": config.get("app.name", "NuxAI"),
        "version": config.get("app.version", "0.3.0"),
        "timestamp": datetime.now().isoformat()
    }


@router.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "status": "running",
        "service": config.get("app.name", "NuxAI"),
        "version": config.get("app.version", "0.3.0"),
        "personality": {
            "name": config.get("personality.name"),
            "type": config.get("personality.type"),
            "voice_enabled": config.get("personality.voice_enabled")
        },
        "features": config.get("features", {}),
        "timestamp": datetime.now().isoformat()
    }

