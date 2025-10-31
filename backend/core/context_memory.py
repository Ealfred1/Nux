"""
Context Memory (v0.5)
Manages conversation history and context for intelligent responses
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import deque
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContextMemory:
    """Manages conversation context and history"""
    
    def __init__(self, max_history: int = 50, context_window_minutes: int = 30):
        self.max_history = max_history
        self.context_window = timedelta(minutes=context_window_minutes)
        self.history = deque(maxlen=max_history)
        self.session_start = datetime.now()
        
    def add_interaction(self, command: str, result: Dict[str, Any], response: str = None):
        """Add a command-response interaction to history"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result": result,
            "response": response
        }
        self.history.append(interaction)
        logger.debug(f"Added to context: {command}")
    
    def get_recent_context(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get recent context within time window"""
        cutoff_time = datetime.now() - self.context_window
        recent = []
        
        for interaction in reversed(self.history):
            timestamp = datetime.fromisoformat(interaction["timestamp"])
            if timestamp < cutoff_time:
                break
            recent.append(interaction)
            if len(recent) >= count:
                break
        
        return list(reversed(recent))
    
    def get_last_command(self) -> str:
        """Get the last command"""
        if self.history:
            return self.history[-1]["command"]
        return None
    
    def get_last_result(self) -> Dict[str, Any]:
        """Get the last result"""
        if self.history:
            return self.history[-1]["result"]
        return None
    
    def search_history(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search history for interactions containing keyword"""
        results = []
        for interaction in reversed(self.history):
            if keyword.lower() in interaction["command"].lower():
                results.append(interaction)
                if len(results) >= limit:
                    break
        return results
    
    def get_context_summary(self) -> str:
        """Get a text summary of recent context"""
        recent = self.get_recent_context(5)
        if not recent:
            return "No recent context"
        
        summary = "Recent commands:\n"
        for i, interaction in enumerate(recent, 1):
            summary += f"{i}. {interaction['command']}\n"
        
        return summary
    
    def clear_context(self):
        """Clear all context"""
        self.history.clear()
        self.session_start = datetime.now()
        logger.info("Context cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_interactions": len(self.history),
            "session_duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
            "commands_in_window": len(self.get_recent_context(50))
        }

