"""
Skill Manager (v0.4)
Manages loading, executing, and lifecycle of skills
"""
import os
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any
from core.skill_base import Skill, SkillMetadata
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SkillManager:
    """Manages all NuxAI skills"""
    
    def __init__(self, skills_dirs: List[str] = None):
        self.skills: Dict[str, Skill] = {}
        self.skills_dirs = skills_dirs or [
            "skills/builtin",
            "skills/user"
        ]
        
    async def load_all_skills(self):
        """Load all skills from configured directories"""
        logger.info("🔌 Loading skills...")
        
        for skills_dir in self.skills_dirs:
            if not os.path.exists(skills_dir):
                logger.warning(f"Skills directory not found: {skills_dir}")
                continue
            
            await self._load_skills_from_directory(skills_dir)
        
        logger.info(f"✅ Loaded {len(self.skills)} skills")
        
        # Initialize all skills
        for skill_name, skill in self.skills.items():
            try:
                await skill.initialize()
            except Exception as e:
                logger.error(f"Failed to initialize skill {skill_name}: {e}")
    
    async def _load_skills_from_directory(self, directory: str):
        """Load all skills from a directory"""
        path = Path(directory)
        
        for file_path in path.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            try:
                skill = await self._load_skill_from_file(file_path)
                if skill:
                    skill_name = skill.metadata.name
                    self.skills[skill_name] = skill
                    logger.info(f"  ✓ Loaded: {skill_name} v{skill.metadata.version}")
            except Exception as e:
                logger.error(f"Failed to load skill from {file_path}: {e}")
    
    async def _load_skill_from_file(self, file_path: Path) -> Optional[Skill]:
        """Load a skill from a Python file"""
        module_name = file_path.stem
        
        # Load module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            return None
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find Skill subclass
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Skill) and obj != Skill:
                return obj()
        
        return None
    
    async def execute_command(self, command: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a command using appropriate skill
        
        Returns:
            Result dict if skill handles command, None otherwise
        """
        context = context or {}
        
        # Find matching skill
        for skill_name, skill in self.skills.items():
            if not skill.metadata.enabled:
                continue
            
            if skill.can_handle(command):
                logger.info(f"🎯 Skill '{skill_name}' handling command")
                try:
                    result = await skill.execute(command, context)
                    result["skill"] = skill_name
                    return result
                except Exception as e:
                    logger.error(f"Skill {skill_name} execution failed: {e}")
                    return {
                        "success": False,
                        "error": str(e),
                        "skill": skill_name
                    }
        
        return None
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """List all loaded skills"""
        return [
            {
                "name": skill.metadata.name,
                "version": skill.metadata.version,
                "author": skill.metadata.author,
                "description": skill.metadata.description,
                "enabled": skill.metadata.enabled,
                "triggers": skill.metadata.triggers
            }
            for skill in self.skills.values()
        ]
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self.skills.get(name)
    
    def enable_skill(self, name: str):
        """Enable a skill"""
        skill = self.skills.get(name)
        if skill:
            skill.metadata.enabled = True
            logger.info(f"Enabled skill: {name}")
    
    def disable_skill(self, name: str):
        """Disable a skill"""
        skill = self.skills.get(name)
        if skill:
            skill.metadata.enabled = False
            logger.info(f"Disabled skill: {name}")
    
    async def shutdown_all(self):
        """Shutdown all skills"""
        logger.info("Shutting down all skills...")
        for skill in self.skills.values():
            try:
                await skill.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down skill: {e}")

