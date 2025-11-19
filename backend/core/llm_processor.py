"""
LLM Processor (v0.5)
Local LLM integration for intelligent command understanding
"""
from typing import Optional, Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMProcessor:
    """Process commands using local LLM"""
    
    def __init__(self, model_name: str = "orca-mini-3b-gguf2-q4_0.gguf"):
        self.model_name = model_name
        self.model = None
        self.enabled = False
        
    def initialize(self):
        """Initialize the LLM model"""
        try:
            logger.info(f"🧠 Loading LLM model: {self.model_name}...")
            
            # Try to import gpt4all
            try:
                from gpt4all import GPT4All
                self.model = GPT4All(self.model_name)
                self.enabled = True
                logger.info("✅ LLM model loaded successfully")
            except ImportError:
                logger.warning("gpt4all not installed, LLM features disabled")
                self.enabled = False
            except Exception as e:
                logger.warning(f"Could not load LLM model: {e}")
                logger.info("💡 LLM features will be disabled")
                self.enabled = False
                
        except Exception as e:
            logger.error(f"LLM initialization error: {e}")
            self.enabled = False
    
    async def process_command(self, command: str, context: str = "") -> Optional[Dict[str, Any]]:
        """
        Process command with LLM for better understanding
        
        Args:
            command: The voice command
            context: Recent conversation context
        
        Returns:
            Processed command understanding or None
        """
        if not self.enabled:
            return None
        
        try:
            prompt = self._build_prompt(command, context)
            response = self.model.generate(prompt, max_tokens=100)
            
            return {
                "understood": True,
                "llm_response": response.strip(),
                "confidence": 0.8
            }
            
        except Exception as e:
            logger.error(f"LLM processing error: {e}")
            return None
    
    def _build_prompt(self, command: str, context: str) -> str:
        """Build prompt for LLM"""
        prompt = """You are NuxAI, a helpful voice assistant. 
Understand the following voice command and determine what action to take.

"""
        
        if context:
            prompt += f"Recent context:\n{context}\n\n"
        
        prompt += f"User command: {command}\n\n"
        prompt += "What is the user asking for? Respond briefly:"
        
        return prompt
    
    async def parse_compound_command(self, command: str) -> Optional[List[str]]:
        """
        Parse compound commands (e.g., "open chrome and search for python")
        
        Returns:
            List of individual commands or None
        """
        if not self.enabled:
            # Fallback: simple splitting
            return self._simple_compound_parse(command)
        
        try:
            prompt = f"""Break this compound command into individual actions:
"{command}"

List each action on a new line:"""
            
            response = self.model.generate(prompt, max_tokens=100)
            
            # Parse response into list
            actions = [line.strip() for line in response.split('\n') if line.strip()]
            actions = [a.lstrip('1234567890.- ') for a in actions]
            
            return actions if actions else [command]
            
        except Exception as e:
            logger.error(f"Compound parsing error: {e}")
            return [command]
    
    def _simple_compound_parse(self, command: str) -> List[str]:
        """Simple fallback for compound command parsing"""
        # Split on "and", "then", "after that"
        separators = [" and ", " then ", " after that ", " followed by "]
        
        parts = [command]
        for sep in separators:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(sep))
            parts = new_parts
        
        return [p.strip() for p in parts if p.strip()]

