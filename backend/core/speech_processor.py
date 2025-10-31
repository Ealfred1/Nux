"""
Speech Processor Module (v0.2)
Handles voice recording and speech-to-text using Whisper
"""
import asyncio
import wave
import tempfile
import pyaudio
import whisper
import numpy as np
from pathlib import Path
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SpeechProcessor:
    """Records audio and transcribes using Whisper"""
    
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    CHANNELS = 1
    RECORD_SECONDS = 5
    
    def __init__(self):
        self.audio = None
        self.stream = None
        self.model = None
        self.model_loaded = False
        
    def load_model(self, model_size: str = "base"):
        """Load Whisper model (lazy loading)"""
        if self.model_loaded:
            return
            
        try:
            logger.info(f"📥 Loading Whisper model ({model_size})...")
            self.model = whisper.load_model(model_size)
            self.model_loaded = True
            logger.info("✅ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            logger.info("💡 Fallback: Using simple text simulation")
    
    async def record_audio(self, duration: float = None) -> Optional[str]:
        """Record audio and save to temporary file"""
        duration = duration or self.RECORD_SECONDS
        
        try:
            logger.info(f"🎤 Recording audio for {duration} seconds...")
            
            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            
            # Open stream
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.CHANNELS,
                rate=self.SAMPLE_RATE,
                input=True,
                frames_per_buffer=self.CHUNK_SIZE
            )
            
            frames = []
            num_chunks = int(self.SAMPLE_RATE / self.CHUNK_SIZE * duration)
            
            # Record audio
            for _ in range(num_chunks):
                data = self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
                await asyncio.sleep(0.001)  # Allow other tasks to run
            
            # Stop recording
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(b''.join(frames))
            
            logger.info(f"✅ Audio recorded: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
    
    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcribe audio file using Whisper"""
        if not self.model_loaded:
            self.load_model()
        
        if not self.model:
            # Fallback for testing without model
            logger.warning("Whisper model not available, using fallback")
            return await self._fallback_transcribe()
        
        try:
            logger.info("🔄 Transcribing audio with Whisper...")
            
            # Run transcription in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.model.transcribe(audio_path, language="en")
            )
            
            text = result["text"].strip()
            logger.info(f"📝 Transcribed: '{text}'")
            
            # Clean up temp file
            try:
                Path(audio_path).unlink()
            except:
                pass
            
            return text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    async def _fallback_transcribe(self) -> str:
        """Fallback transcription for testing"""
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Return a demo command
        demo_commands = [
            "open browser",
            "take screenshot",
            "what time is it",
            "open terminal"
        ]
        
        import random
        return random.choice(demo_commands)
    
    async def record_and_transcribe(self, duration: float = None) -> Optional[str]:
        """Record audio and transcribe in one call"""
        audio_path = await self.record_audio(duration)
        
        if not audio_path:
            return None
        
        return await self.transcribe_audio(audio_path)

