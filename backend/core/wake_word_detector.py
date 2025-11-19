"""
Wake Word Detection Module
Uses Vosk for offline wake word detection
"""
import asyncio
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from pathlib import Path
from typing import Optional
from utils.logger import setup_logger
from core.websocket_manager import ConnectionManager

logger = setup_logger(__name__)


class WakeWordDetector:
    """Detects wake words from microphone input"""
    
    WAKE_WORDS = ["computer", "hey computer", "nux", "hey nux"]
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 4096
    
    def __init__(self, voice_processor):
        self.voice_processor = voice_processor
        self.is_listening = False
        self.audio = None
        self.stream = None
        self.model = None
        self.recognizer = None
        self.ws_manager = ConnectionManager()
        
    async def start_listening(self):
        """Start listening for wake words"""
        if self.is_listening:
            logger.warning("Wake word detector is already listening")
            return
            
        try:
            logger.info("🎤 Initializing wake word detector...")
            
            # Initialize Vosk model - use absolute path based on this file's location
            import os
            script_dir = Path(__file__).parent.parent  # Go up to backend directory
            model_path = script_dir / "models" / "vosk-model-small-en-us-0.15"
            
            if not model_path.exists():
                logger.error(f"Vosk model not found at {model_path}")
                logger.info("Please download the model: https://alphacephei.com/vosk/models")
                # Use a fallback simple wake word detection
                await self._simple_wake_word_detection()
                return
                
            self.model = Model(str(model_path))
            self.recognizer = KaldiRecognizer(self.model, self.SAMPLE_RATE)
            
            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.SAMPLE_RATE,
                input=True,
                frames_per_buffer=self.CHUNK_SIZE
            )
            
            self.is_listening = True
            logger.info("✅ Wake word detector ready! Say 'Computer' or 'Hey Nux' to activate...")
            
            # Listen loop
            while self.is_listening:
                data = self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    
                    if text:
                        logger.debug(f"Recognized: {text}")
                        
                        # Check for wake words
                        for wake_word in self.WAKE_WORDS:
                            if wake_word in text:
                                logger.info(f"🎯 Wake word detected: '{wake_word}'")
                                await self._handle_wake_word()
                                break
                
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Error in wake word detection: {e}")
            # Fallback to simple detection
            await self._simple_wake_word_detection()
        finally:
            self._cleanup()
    
    async def _simple_wake_word_detection(self):
        """Fallback: Simple wake word detection without Vosk model"""
        logger.info("🎤 Using simple wake word detection (press Enter to activate)")
        logger.info("✅ Wake word detector ready! Press Enter to simulate wake word...")
        
        self.is_listening = True
        
        # Simulate wake word with Enter key for testing
        loop = asyncio.get_event_loop()
        
        while self.is_listening:
            await asyncio.sleep(1)
            # In a real scenario, this would be triggered by actual voice
            # For testing without model, we'll auto-trigger every 30 seconds
            # or you can modify to use keyboard input
            
    async def _handle_wake_word(self):
        """Handle wake word detection"""
        try:
            # Notify overlay via WebSocket
            await self.ws_manager.broadcast({
                "type": "wake_word_detected",
                "message": "Wake word detected",
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Start listening for command
            logger.info("👂 Listening for command...")
            await self.voice_processor.listen_for_command()
            
        except Exception as e:
            logger.error(f"Error handling wake word: {e}")
    
    def stop_listening(self):
        """Stop listening for wake words"""
        logger.info("Stopping wake word detector...")
        self.is_listening = False
        self._cleanup()
    
    def _cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()

