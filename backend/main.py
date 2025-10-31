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
from core.context_memory import ContextMemory
from core.llm_processor import LLMProcessor
from core.platform_manager import PlatformManager
from core.hotkey_manager import HotkeyManager
from core.system_tray import SystemTray
from web_ui.app import router as webui_router
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Global instances
wake_word_detector = None
voice_processor = None
command_executor = None
context_memory = None
llm_processor = None
platform_manager = None
hotkey_manager = None
system_tray = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global wake_word_detector, voice_processor, command_executor
    global context_memory, llm_processor, platform_manager, hotkey_manager, system_tray
    
    app_version = config.get("app.version", "1.0.0")
    logger.info(f"🚀 Starting NuxAI Backend v{app_version}...")
    logger.info("=" * 60)
    
    # Initialize platform manager (v0.6)
    platform_manager = PlatformManager()
    
    # Initialize core components
    command_executor = CommandExecutor()
    context_memory = ContextMemory(
        max_history=config.get("context.max_history", 50),
        context_window_minutes=config.get("context.window_minutes", 30)
    )
    
    voice_processor = VoiceProcessor(command_executor, config.config)
    
    # Load skills (v0.4)
    if config.get("features.skills", True):
        logger.info("🔌 Loading skills...")
        await voice_processor.skill_manager.load_all_skills()
    
    # Initialize LLM (v0.5) if enabled
    if config.get("features.llm", False):
        llm_processor = LLMProcessor(config.get("llm.model"))
        llm_processor.initialize()
    
    # Initialize hotkeys (v0.6) if enabled  
    if config.get("features.hotkeys", True):
        hotkey_manager = HotkeyManager(config.get("hotkeys.activate", "ctrl+shift+space"))
        hotkey_manager.initialize()
    
    # Initialize wake word detector
    wake_word_detector = WakeWordDetector(voice_processor)
    
    # Start wake word detection in background
    asyncio.create_task(wake_word_detector.start_listening())
    
    logger.info("=" * 60)
    logger.info("✅ NuxAI v{} is ready!".format(app_version))
    logger.info(f"   🎤 Wake words: {', '.join(config.get('voice.wake_words', []))}")
    logger.info(f"   🎭 Personality: {config.get('personality.name')} ({config.get('personality.type')})")
    logger.info(f"   🗣️  TTS: {'Enabled' if config.get('personality.voice_enabled') else 'Disabled'}")
    logger.info(f"   🔌 Skills: {len(voice_processor.skill_manager.skills)} loaded")
    logger.info(f"   🧠 LLM: {'Enabled' if llm_processor and llm_processor.enabled else 'Disabled'}")
    logger.info(f"   ⌨️  Hotkeys: {'Enabled' if hotkey_manager and hotkey_manager.enabled else 'Disabled'}")
    logger.info(f"   🖥️  Platform: {platform_manager.system}")
    logger.info(f"   🌐 Web UI: http://{config.get('server.host')}:{config.get('server.port')}/settings")
    logger.info("=" * 60)
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down NuxAI Backend...")
    if wake_word_detector:
        wake_word_detector.stop_listening()
    if voice_processor:
        if voice_processor.tts_engine:
            voice_processor.tts_engine.shutdown()
        if voice_processor.skill_manager:
            await voice_processor.skill_manager.shutdown_all()
    if hotkey_manager:
        hotkey_manager.unregister()
    if system_tray:
        system_tray.stop()


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
app.include_router(webui_router, tags=["web-ui"])


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

