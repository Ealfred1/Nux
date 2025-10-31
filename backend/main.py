"""
NuxAI Backend - Main Application Entry Point (v0.3)
FastAPI-based voice assistant with Whisper STT and TTS
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
from config import config
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
    
    app_version = config.get("app.version", "0.3.0")
    logger.info(f"🚀 Starting NuxAI Backend v{app_version}...")
    
    # Initialize components with config
    command_executor = CommandExecutor()
    voice_processor = VoiceProcessor(command_executor, config.config)
    wake_word_detector = WakeWordDetector(voice_processor)
    
    # Start wake word detection in background
    asyncio.create_task(wake_word_detector.start_listening())
    
    logger.info("✅ NuxAI Backend is ready!")
    logger.info(f"   - Wake words: {config.get('voice.wake_words')}")
    logger.info(f"   - Personality: {config.get('personality.name')} ({config.get('personality.type')})")
    logger.info(f"   - TTS enabled: {config.get('personality.voice_enabled')}")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down NuxAI Backend...")
    if wake_word_detector:
        wake_word_detector.stop_listening()
    if voice_processor and voice_processor.tts_engine:
        voice_processor.tts_engine.shutdown()


# Create FastAPI app
app = FastAPI(
    title="NuxAI Backend",
    description="Intelligent offline voice assistant with Whisper and TTS",
    version=config.get("app.version", "0.3.0"),
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
        "name": config.get("app.name", "NuxAI"),
        "version": config.get("app.version", "0.3.0"),
        "status": "running",
        "message": "Intelligent Voice Assistant with Whisper and TTS",
        "personality": config.get("personality.name", "Nux"),
        "features": config.get("features", {})
    }


def main():
    """Main entry point"""
    host = config.get("server.host", "127.0.0.1")
    port = config.get("server.port", 8000)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()

