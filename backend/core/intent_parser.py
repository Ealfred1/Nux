"""
Intent Parser Module (v0.2)
Parses voice commands and extracts intent and parameters
"""
import re
from typing import Dict, Optional, List, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IntentParser:
    """Parses natural language commands into structured intents"""
    
    def __init__(self):
        self.intent_patterns = self._build_patterns()
    
    def _build_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build regex patterns for intent matching"""
        return {
            "open_application": [
                {
                    "pattern": r"(?:open|launch|start)\s+(?:the\s+)?(\w+(?:\s+\w+)?)",
                    "examples": ["open browser", "launch firefox", "start calculator"]
                },
            ],
            "screenshot": [
                {
                    "pattern": r"(?:take|capture|grab)\s+(?:a\s+)?screenshot",
                    "examples": ["take screenshot", "capture screen"]
                },
                {
                    "pattern": r"screenshot",
                    "examples": ["screenshot"]
                },
            ],
            "time_query": [
                {
                    "pattern": r"(?:what|tell me)\s+(?:is\s+)?(?:the\s+)?time(?:\s+is it)?",
                    "examples": ["what time is it", "tell me the time"]
                },
                {
                    "pattern": r"(?:what's|whats)\s+the\s+time",
                    "examples": ["what's the time"]
                },
                {
                    "pattern": r"^time$",
                    "examples": ["time"]
                },
            ],
            "system_control": [
                {
                    "pattern": r"(shutdown|restart|reboot|sleep|suspend)\s*(?:the\s+)?(?:computer|system|pc)?",
                    "examples": ["shutdown", "restart computer", "sleep"]
                },
            ],
            "volume_control": [
                {
                    "pattern": r"(?:set|change)\s+volume\s+to\s+(\d+)",
                    "examples": ["set volume to 50"]
                },
                {
                    "pattern": r"(increase|decrease|raise|lower)\s+(?:the\s+)?volume",
                    "examples": ["increase volume", "lower volume"]
                },
                {
                    "pattern": r"(mute|unmute)",
                    "examples": ["mute", "unmute"]
                },
            ],
            "search": [
                {
                    "pattern": r"(?:search|google|look up)\s+(?:for\s+)?(.+)",
                    "examples": ["search for python", "google linux commands"]
                },
            ],
            "file_operations": [
                {
                    "pattern": r"(?:create|make)\s+(?:a\s+)?(?:new\s+)?file\s+(?:called\s+)?(.+)",
                    "examples": ["create file test.txt", "make a new file"]
                },
                {
                    "pattern": r"(?:delete|remove)\s+(?:the\s+)?file\s+(.+)",
                    "examples": ["delete file test.txt"]
                },
            ],
        }
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse text into intent and parameters"""
        text = text.lower().strip()
        
        logger.info(f"🧠 Parsing intent from: '{text}'")
        
        # Try to match against patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                match = re.search(pattern, text, re.IGNORECASE)
                
                if match:
                    result = {
                        "intent": intent,
                        "original_text": text,
                        "confidence": 0.9,
                        "parameters": {}
                    }
                    
                    # Extract parameters from capture groups
                    if match.groups():
                        result["parameters"] = self._extract_parameters(
                            intent, 
                            match.groups()
                        )
                    
                    logger.info(f"✅ Intent matched: {intent}")
                    return result
        
        # No match found
        logger.warning(f"❓ No intent matched for: '{text}'")
        return {
            "intent": "unknown",
            "original_text": text,
            "confidence": 0.0,
            "parameters": {}
        }
    
    def _extract_parameters(self, intent: str, groups: tuple) -> Dict[str, Any]:
        """Extract and structure parameters based on intent"""
        params = {}
        
        if intent == "open_application":
            params["application"] = groups[0].strip()
        
        elif intent == "system_control":
            params["action"] = groups[0].strip()
        
        elif intent == "volume_control":
            if groups[0].isdigit():
                params["level"] = int(groups[0])
            else:
                params["action"] = groups[0].strip()
        
        elif intent == "search":
            params["query"] = groups[0].strip()
        
        elif intent == "file_operations":
            params["filename"] = groups[0].strip()
        
        return params
    
    def get_command_suggestions(self, partial_text: str) -> List[str]:
        """Get command suggestions based on partial input"""
        suggestions = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern_info in patterns:
                for example in pattern_info["examples"]:
                    if example.startswith(partial_text.lower()):
                        suggestions.append(example)
        
        return suggestions[:5]  # Return top 5 suggestions

