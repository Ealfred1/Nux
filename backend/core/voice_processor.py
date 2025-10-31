"""
Voice Processing Module
Handles voice command recognition and processing
"""
import asyncio
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from pathlib import Path
from utils.logger import setup_logger
from core.websocket_manager import ConnectionManager

logger = setup_logger(__name__)


class VoiceProcessor:
    """Processes voice commands"""
    
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 4096
    LISTEN_TIMEOUT = 5.0  # seconds
    
    def __init__(self, command_executor):
        self.command_executor = command_executor
        self.ws_manager = ConnectionManager()
        
    async def listen_for_command(self):
        """Listen for a voice command after wake word"""
        try:
            # Notify overlay to show listening state
            await self.ws_manager.broadcast({
                "type": "listening_started",
                "message": "Listening for command..."
            })
            
            # For v0.1, we'll use a simple demo command recognition
            # In production, this would use Vosk or other STT
            command_text = await self._capture_voice_command()
            
            if command_text:
                logger.info(f"📝 Command received: '{command_text}'")
                
                # Notify overlay
                await self.ws_manager.broadcast({
                    "type": "command_received",
                    "command": command_text
                })
                
                # Execute command
                result = await self.command_executor.execute(command_text)
                
                # Send result to overlay
                await self.ws_manager.broadcast({
                    "type": "command_result",
                    "result": result
                })
            else:
                logger.warning("No command captured")
                await self.ws_manager.broadcast({
                    "type": "listening_timeout",
                    "message": "No command heard"
                })
                
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            await self.ws_manager.broadcast({
                "type": "error",
                "message": str(e)
            })
    
    async def _capture_voice_command(self):
        """Capture voice command from microphone"""
        # For v0.1 demo, we'll use predefined test commands
        # In production, this would use actual STT
        
        demo_commands = [
            "open browser",
            "take screenshot",
            "what time is it",
            "open terminal"
        ]
        
        # Simulate voice capture delay
        await asyncio.sleep(2)
        
        # Return first demo command for testing
        # In real implementation, this would use Vosk/Whisper
        return demo_commands[0]

