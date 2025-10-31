"""
Health Check API Router
Provides health and status endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NuxAI Backend",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "status": "running",
        "service": "NuxAI Backend",
        "version": "0.1.0",
        "features": {
            "wake_word_detection": True,
            "voice_commands": True,
            "websocket": True,
            "offline_mode": True
        },
        "timestamp": datetime.now().isoformat()
    }

