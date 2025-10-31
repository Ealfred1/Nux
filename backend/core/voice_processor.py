"""
Voice Processing Module (v0.2 Enhanced)
Handles voice command recognition and processing with Whisper
"""
import asyncio
import json
from pathlib import Path
from utils.logger import setup_logger
from core.websocket_manager import ConnectionManager
from core.speech_processor import SpeechProcessor
from core.intent_parser import IntentParser
from core.tts_engine import TTSEngine
from core.personality import Personality

logger = setup_logger(__name__)


class VoiceProcessor:
    """Processes voice commands with advanced STT and TTS"""
    
    def __init__(self, command_executor, config: dict = None):
        self.command_executor = command_executor
        self.ws_manager = ConnectionManager()
        self.config = config or {}
        
        # Initialize v0.2 components
        self.speech_processor = SpeechProcessor()
        self.intent_parser = IntentParser()
        
        # Initialize v0.3 components
        self.tts_engine = TTSEngine()
        self.personality = Personality(self.config.get("personality", {}))
        
        # Settings
        self.recording_duration = self.config.get("voice", {}).get("recording_duration", 5)
        self.voice_enabled = self.config.get("personality", {}).get("voice_enabled", True)
        
    async def listen_for_command(self):
        """Listen for a voice command after wake word (v0.2 Enhanced)"""
        try:
            # Speak wake response (v0.3)
            if self.voice_enabled:
                wake_response = self.personality.get_wake_response()
                await self.tts_engine.speak(wake_response, wait=False)
            
            # Notify overlay to show listening state
            await self.ws_manager.broadcast({
                "type": "listening_started",
                "message": "Listening for command..."
            })
            
            # Record and transcribe voice command (v0.2)
            command_text = await self._capture_voice_command()
            
            if command_text:
                logger.info(f"📝 Command received: '{command_text}'")
                
                # Notify overlay
                await self.ws_manager.broadcast({
                    "type": "command_received",
                    "command": command_text
                })
                
                # Parse intent (v0.2)
                intent_result = self.intent_parser.parse(command_text)
                
                # Execute command with intent
                result = await self.command_executor.execute_with_intent(
                    command_text, 
                    intent_result
                )
                
                # Generate personality response (v0.3)
                response_text = self.personality.format_command_response(
                    intent_result["intent"],
                    result
                )
                
                # Speak response (v0.3)
                if self.voice_enabled:
                    await self.tts_engine.speak(response_text, wait=False)
                
                # Send result to overlay
                await self.ws_manager.broadcast({
                    "type": "command_result",
                    "result": result,
                    "response": response_text
                })
            else:
                logger.warning("No command captured")
                timeout_msg = self.personality.get_response("timeout")
                
                if self.voice_enabled:
                    await self.tts_engine.speak(timeout_msg, wait=False)
                
                await self.ws_manager.broadcast({
                    "type": "listening_timeout",
                    "message": timeout_msg
                })
                
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            error_msg = self.personality.get_response("error")
            
            if self.voice_enabled:
                await self.tts_engine.speak(error_msg, wait=False)
            
            await self.ws_manager.broadcast({
                "type": "error",
                "message": str(e)
            })
    
    async def _capture_voice_command(self):
        """Capture voice command from microphone using Whisper (v0.2)"""
        try:
            # Use speech processor to record and transcribe
            command_text = await self.speech_processor.record_and_transcribe(
                duration=self.recording_duration
            )
            return command_text
        except Exception as e:
            logger.error(f"Error capturing voice: {e}")
            return None

