"""
Text-to-Speech Engine (v0.3)
Provides voice responses using pyttsx3
"""
import pyttsx3
import asyncio
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TTSEngine:
    """Text-to-speech engine for voice responses"""
    
    def __init__(self):
        self.engine = None
        self.initialized = False
        self.enabled = True
        
        # Voice settings
        self.rate = 175  # Words per minute
        self.volume = 0.9  # 0.0 to 1.0
        self.voice_id = None  # None = default
        
    def initialize(self):
        """Initialize the TTS engine"""
        if self.initialized:
            return
        
        try:
            logger.info("🔊 Initializing TTS engine...")
            self.engine = pyttsx3.init()
            
            # Configure engine
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # List available voices
            voices = self.engine.getProperty('voices')
            logger.info(f"📢 Available voices: {len(voices)}")
            
            for idx, voice in enumerate(voices):
                logger.debug(f"  {idx}: {voice.name} ({voice.gender})")
            
            # Set voice if specified
            if self.voice_id is not None and self.voice_id < len(voices):
                self.engine.setProperty('voice', voices[self.voice_id].id)
            
            self.initialized = True
            logger.info("✅ TTS engine initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.enabled = False
    
    async def speak(self, text: str, wait: bool = True):
        """Speak the given text"""
        if not self.enabled:
            logger.debug(f"TTS disabled, would say: '{text}'")
            return
        
        if not self.initialized:
            self.initialize()
        
        if not self.initialized:
            return
        
        try:
            logger.info(f"🗣️ Speaking: '{text}'")
            
            if wait:
                # Run in executor to avoid blocking
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._speak_sync, text)
            else:
                # Fire and forget
                asyncio.create_task(self._speak_async(text))
                
        except Exception as e:
            logger.error(f"Error speaking: {e}")
    
    def _speak_sync(self, text: str):
        """Synchronous speak method"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    async def _speak_async(self, text: str):
        """Asynchronous speak method"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._speak_sync, text)
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.rate = rate
        if self.initialized:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self.initialized:
            self.engine.setProperty('volume', self.volume)
    
    def set_voice(self, voice_index: int):
        """Set voice by index"""
        self.voice_id = voice_index
        if self.initialized:
            voices = self.engine.getProperty('voices')
            if voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
    
    def list_voices(self) -> list:
        """List available voices"""
        if not self.initialized:
            self.initialize()
        
        if not self.initialized:
            return []
        
        voices = self.engine.getProperty('voices')
        return [
            {
                "id": idx,
                "name": voice.name,
                "languages": voice.languages,
                "gender": voice.gender
            }
            for idx, voice in enumerate(voices)
        ]
    
    def stop(self):
        """Stop current speech"""
        if self.initialized and self.engine:
            try:
                self.engine.stop()
            except:
                pass
    
    def shutdown(self):
        """Shutdown the TTS engine"""
        if self.initialized and self.engine:
            try:
                self.engine.stop()
                del self.engine
            except:
                pass
        self.initialized = False

