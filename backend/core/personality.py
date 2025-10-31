"""
Personality Module (v0.3)
Manages AI personality, responses, and behavior
"""
from typing import Dict, List, Optional
import random
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Personality:
    """Manages NuxAI's personality and response generation"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.name = self.config.get("name", "Nux")
        self.personality_type = self.config.get("personality", "friendly")
        
        # Response templates
        self.response_templates = {
            "greeting": [
                f"Hello! {self.name} here.",
                f"Yes, I'm listening.",
                f"How can I help you?",
                "I'm ready!",
            ],
            "acknowledged": [
                "Got it!",
                "On it!",
                "Sure thing!",
                "Will do!",
                "Right away!",
            ],
            "success": [
                "Done!",
                "All set!",
                "Task completed!",
                "There you go!",
                "Finished!",
            ],
            "error": [
                "Sorry, I couldn't do that.",
                "Hmm, that didn't work.",
                "I ran into a problem.",
                "Something went wrong.",
            ],
            "unknown_command": [
                "I didn't understand that.",
                "Could you repeat that?",
                "I'm not sure what you mean.",
                "I don't know how to do that yet.",
            ],
            "timeout": [
                "I didn't hear anything.",
                "No command heard.",
                "Listening timeout.",
            ],
        }
        
        # Personality modifiers
        if self.personality_type == "professional":
            self._make_professional()
        elif self.personality_type == "casual":
            self._make_casual()
        elif self.personality_type == "excited":
            self._make_excited()
    
    def _make_professional(self):
        """Adjust responses for professional personality"""
        self.response_templates.update({
            "greeting": [
                f"{self.name} AI assistant ready.",
                "At your service.",
                "Standing by for commands.",
            ],
            "acknowledged": [
                "Understood.",
                "Executing.",
                "Processing request.",
            ],
            "success": [
                "Task completed successfully.",
                "Operation finished.",
                "Command executed.",
            ],
        })
    
    def _make_casual(self):
        """Adjust responses for casual personality"""
        self.response_templates.update({
            "greeting": [
                "Hey! What's up?",
                "Yo, I'm here!",
                "Sup?",
            ],
            "acknowledged": [
                "Cool, doing it!",
                "Alright!",
                "You got it!",
            ],
            "success": [
                "Done and done!",
                "Easy peasy!",
                "Nailed it!",
            ],
        })
    
    def _make_excited(self):
        """Adjust responses for excited personality"""
        self.response_templates.update({
            "greeting": [
                "Yes! I'm so ready!",
                "Let's do this!",
                "I'm pumped!",
            ],
            "acknowledged": [
                "Awesome! On it!",
                "Yes! Doing it now!",
                "Exciting! Let me handle that!",
            ],
            "success": [
                "Woohoo! Done!",
                "Success! That was great!",
                "Nailed it! Amazing!",
            ],
        })
    
    def get_response(self, response_type: str, context: Dict = None) -> str:
        """Get a response for the given type"""
        templates = self.response_templates.get(response_type, ["OK."])
        response = random.choice(templates)
        
        # Add context if provided
        if context:
            if "application" in context:
                response = f"{response} Opening {context['application']}."
            elif "action" in context:
                response = f"{response} {context['action'].title()}."
            elif "result" in context:
                response = context["result"]
        
        return response
    
    def format_command_response(self, intent: str, result: Dict) -> str:
        """Format a natural response based on command result"""
        if not result.get("success"):
            error_msg = result.get("error", "unknown error")
            return f"Sorry, I couldn't complete that. {error_msg}"
        
        # Get result message
        result_text = result.get("result", "")
        
        # Add personality flair
        if intent == "open_application":
            return f"Opening that for you now! {result_text}"
        elif intent == "screenshot":
            return f"Screenshot captured! {result_text}"
        elif intent == "time_query":
            return result_text
        elif intent == "system_control":
            return f"Executing system command. {result_text}"
        else:
            return f"Done! {result_text}"
    
    def get_wake_response(self) -> str:
        """Get response when wake word is detected"""
        return self.get_response("greeting")
    
    def get_listening_prompt(self) -> str:
        """Get prompt when listening for command"""
        prompts = [
            "I'm listening...",
            "Go ahead...",
            "What can I do for you?",
        ]
        return random.choice(prompts)

