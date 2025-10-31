"""
Skill Base Class (v0.4)
Base class for all NuxAI skills/plugins
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class SkillMetadata:
    """Metadata for a skill"""
    name: str
    version: str
    author: str
    description: str
    triggers: List[str]  # Command patterns that trigger this skill
    requires: List[str] = None  # Required dependencies
    enabled: bool = True


class Skill(ABC):
    """Base class for all skills"""
    
    def __init__(self):
        self.metadata = self.get_metadata()
        self.logger = setup_logger(f"skill.{self.metadata.name}")
    
    @abstractmethod
    def get_metadata(self) -> SkillMetadata:
        """Return skill metadata"""
        pass
    
    @abstractmethod
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill
        
        Args:
            command: The voice command text
            context: Execution context (user data, history, etc.)
        
        Returns:
            Dict with 'success', 'result', and optional 'speak' key
        """
        pass
    
    def can_handle(self, command: str) -> bool:
        """Check if this skill can handle the command"""
        command_lower = command.lower()
        for trigger in self.metadata.triggers:
            if trigger.lower() in command_lower:
                return True
        return False
    
    async def initialize(self):
        """Initialize skill (called once on load)"""
        self.logger.info(f"Initializing skill: {self.metadata.name}")
    
    async def shutdown(self):
        """Cleanup skill (called on app shutdown)"""
        self.logger.info(f"Shutting down skill: {self.metadata.name}")
    
    def get_help(self) -> str:
        """Return help text for this skill"""
        return f"{self.metadata.description}\n\nTriggers: {', '.join(self.metadata.triggers)}"

