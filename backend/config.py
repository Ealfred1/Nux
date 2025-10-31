"""
Configuration Management (v0.3 Enhanced)
Loads configuration from JSON file and environment variables
"""
import json
from pathlib import Path
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Config:
    """Application configuration manager"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not self.config_file.exists():
            logger.warning(f"Config file not found: {self.config_file}, using defaults")
            return self._default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                logger.info(f"✅ Configuration loaded from {self.config_file}")
                return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "app": {
                "name": "NuxAI",
                "version": "0.3.0"
            },
            "personality": {
                "name": "Nux",
                "type": "friendly",
                "voice_enabled": True
            },
            "voice": {
                "wake_words": ["computer", "hey computer", "nux", "hey nux"],
                "whisper_model": "base",
                "recording_duration": 5,
                "tts_rate": 175,
                "tts_volume": 0.9,
                "tts_voice_index": None
            },
            "server": {
                "host": "127.0.0.1",
                "port": 8000
            },
            "features": {
                "wake_word_detection": True,
                "voice_recognition": True,
                "text_to_speech": True,
                "intent_parsing": True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")


# Global config instance
config = Config()

