"""
Configuration Management
Loads configuration from environment variables or defaults
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "NuxAI"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    
    # Voice
    sample_rate: int = 16000
    chunk_size: int = 4096
    wake_words: list = ["computer", "hey computer", "nux", "hey nux"]
    
    # Paths
    model_path: Path = Path("models/vosk-model-small-en-us-0.15")
    log_dir: Path = Path("logs")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

