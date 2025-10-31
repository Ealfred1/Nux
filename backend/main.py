"""
NuxAI Backend - Main Application Entry Point
FastAPI-based voice assistant backend with wake word detection
"""
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.websocket import router as websocket_router
from api.health import router as health_router
from core.wake_word_detector import WakeWordDetector
from core.voice_processor import VoiceProcessor
from core.command_executor import CommandExecutor
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Global instances
wake_word_detector = None
voice_processor = None
command_executor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global wake_word_detector, voice_processor, command_executor
    
    logger.info("🚀 Starting NuxAI Backend v0.1...")
    
    # Initialize components
    command_executor = CommandExecutor()
    voice_processor = VoiceProcessor(command_executor)
    wake_word_detector = WakeWordDetector(voice_processor)
    
    # Start wake word detection in background
    asyncio.create_task(wake_word_detector.start_listening())
    
    logger.info("✅ NuxAI Backend is ready!")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down NuxAI Backend...")
    if wake_word_detector:
        wake_word_detector.stop_listening()


# Create FastAPI app
app = FastAPI(
    title="NuxAI Backend",
    description="Intelligent offline voice assistant for Linux",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "NuxAI",
        "version": "0.1.0",
        "status": "running",
        "message": "Intelligent Voice Assistant Backend"
    }


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()

