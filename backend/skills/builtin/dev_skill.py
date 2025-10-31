"""
Developer Skill (v0.4)
Developer-focused commands: git, docker, code, etc.
"""
import subprocess
import os
from typing import Dict, Any
from pathlib import Path
from core.skill_base import Skill, SkillMetadata


class DeveloperSkill(Skill):
    """Developer tools and commands"""
    
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="developer",
            version="1.0.0",
            author="NuxAI Team",
            description="Developer tools: git, docker, IDE commands",
            triggers=["git", "docker", "code", "vs code", "commit", "push", "pull"]
        )
    
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute developer command"""
        command_lower = command.lower()
        
        # Git commands
        if "git status" in command_lower:
            return await self._git_status()
        elif "git" in command_lower and "commit" in command_lower:
            return await self._git_commit()
        elif "git" in command_lower and "push" in command_lower:
            return await self._git_push()
        
        # Docker commands
        elif "docker" in command_lower and "list" in command_lower:
            return await self._docker_list()
        elif "docker" in command_lower and "stop" in command_lower:
            return await self._docker_stop_all()
        
        # IDE commands
        elif "open" in command_lower and ("code" in command_lower or "vs code" in command_lower):
            project_path = self._extract_path(command) or "."
            return await self._open_vscode(project_path)
        
        return {
            "success": False,
            "error": "Unknown developer command"
        }
    
    async def _git_status(self) -> Dict[str, Any]:
        """Get git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                status = result.stdout.strip()
                if status:
                    files_changed = len(status.split('\n'))
                    return {
                        "success": True,
                        "result": status,
                        "speak": f"You have {files_changed} files with changes"
                    }
                else:
                    return {
                        "success": True,
                        "result": "Working tree clean",
                        "speak": "Your working tree is clean"
                    }
            else:
                return {
                    "success": False,
                    "error": "Not a git repository"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _git_commit(self) -> Dict[str, Any]:
        """Stage and commit changes"""
        try:
            # Stage all changes
            subprocess.run(["git", "add", "-A"], check=True, timeout=5)
            
            # Commit with auto-generated message
            timestamp = subprocess.run(
                ["date", "+%Y-%m-%d %H:%M"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            result = subprocess.run(
                ["git", "commit", "-m", f"Auto-commit: {timestamp}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "success": True,
                "result": "Changes committed",
                "speak": "I've committed your changes"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _git_push(self) -> Dict[str, Any]:
        """Push to remote"""
        try:
            result = subprocess.run(
                ["git", "push"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": True,
                "result": "Pushed to remote",
                "speak": "Changes pushed to remote repository"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _docker_list(self) -> Dict[str, Any]:
        """List running containers"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                containers = result.stdout.strip().split('\n')
                containers = [c for c in containers if c]
                
                if containers:
                    return {
                        "success": True,
                        "result": "\n".join(containers),
                        "speak": f"You have {len(containers)} running containers"
                    }
                else:
                    return {
                        "success": True,
                        "result": "No running containers",
                        "speak": "No containers are running"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _docker_stop_all(self) -> Dict[str, Any]:
        """Stop all containers"""
        try:
            subprocess.run(
                ["docker", "stop", "$(docker ps -q)"],
                shell=True,
                timeout=30
            )
            return {
                "success": True,
                "result": "All containers stopped",
                "speak": "I've stopped all Docker containers"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _open_vscode(self, path: str) -> Dict[str, Any]:
        """Open VS Code"""
        try:
            subprocess.Popen(["code", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {
                "success": True,
                "result": f"Opening VS Code: {path}",
                "speak": "Opening VS Code"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_path(self, command: str) -> str:
        """Extract file path from command"""
        # Simple extraction
        words = command.split()
        for word in words:
            if "/" in word or "." in word:
                return word
        return None

