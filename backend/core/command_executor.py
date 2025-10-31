"""
Command Execution Module (v0.2 Enhanced)
Executes system commands based on voice input with intent support
"""
import subprocess
import shlex
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CommandExecutor:
    """Executes voice commands as system operations"""
    
    def __init__(self):
        # Legacy command map for backward compatibility
        self.command_map = {
            "open browser": self._open_browser,
            "open firefox": self._open_browser,
            "open chrome": lambda: self._open_browser("google-chrome"),
            "take screenshot": self._take_screenshot,
            "screenshot": self._take_screenshot,
            "what time is it": self._get_time,
            "time": self._get_time,
            "open terminal": self._open_terminal,
            "open file manager": self._open_file_manager,
            "open calculator": self._open_calculator,
        }
        
        # Intent-based handlers (v0.2)
        self.intent_handlers = {
            "open_application": self._handle_open_application,
            "screenshot": self._handle_screenshot,
            "time_query": self._handle_time_query,
            "system_control": self._handle_system_control,
            "volume_control": self._handle_volume_control,
            "search": self._handle_search,
        }
    
    async def execute_with_intent(self, command_text: str, intent_result: Dict[str, Any]) -> dict:
        """Execute command using intent-based routing (v0.2)"""
        intent = intent_result.get("intent")
        parameters = intent_result.get("parameters", {})
        
        logger.info(f"⚡ Executing intent: {intent} with params: {parameters}")
        
        # Get handler for intent
        handler = self.intent_handlers.get(intent)
        
        if handler:
            try:
                result = handler(parameters) if not asyncio.iscoroutinefunction(handler) else await handler(parameters)
                return {
                    "success": True,
                    "intent": intent,
                    "command": command_text,
                    "result": result
                }
            except Exception as e:
                logger.error(f"Error executing intent {intent}: {e}")
                return {
                    "success": False,
                    "intent": intent,
                    "command": command_text,
                    "error": str(e)
                }
        else:
            # Fallback to legacy execution
            return await self.execute(command_text)
    
    async def execute(self, command_text: str) -> dict:
        """Execute a command based on voice input"""
        command_text = command_text.lower().strip()
        
        logger.info(f"⚡ Executing command: '{command_text}'")
        
        # Find matching command
        for key, handler in self.command_map.items():
            if key in command_text:
                try:
                    result = handler() if not asyncio.iscoroutinefunction(handler) else await handler()
                    return {
                        "success": True,
                        "command": command_text,
                        "result": result
                    }
                except Exception as e:
                    logger.error(f"Error executing command: {e}")
                    return {
                        "success": False,
                        "command": command_text,
                        "error": str(e)
                    }
        
        # Command not recognized
        logger.warning(f"Command not recognized: '{command_text}'")
        return {
            "success": False,
            "command": command_text,
            "error": "Command not recognized"
        }
    
    def _open_browser(self, browser="firefox"):
        """Open web browser"""
        try:
            subprocess.Popen([browser], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Opening {browser}"
        except FileNotFoundError:
            # Try alternative browsers
            for alt_browser in ["firefox", "google-chrome", "chromium", "brave"]:
                try:
                    subprocess.Popen([alt_browser], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return f"Opening {alt_browser}"
                except FileNotFoundError:
                    continue
            return "No browser found"
    
    def _take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = Path.home() / "Pictures" / "Screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            filename = screenshot_dir / f"nuxai_screenshot_{timestamp}.png"
            
            # Try different screenshot tools
            tools = [
                f"gnome-screenshot -f {filename}",
                f"scrot {filename}",
                f"import -window root {filename}",  # ImageMagick
            ]
            
            for tool in tools:
                try:
                    subprocess.run(shlex.split(tool), check=True, timeout=5)
                    logger.info(f"Screenshot saved: {filename}")
                    return f"Screenshot saved to {filename}"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            return "Screenshot tool not available"
            
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return f"Screenshot failed: {str(e)}"
    
    def _get_time(self):
        """Get current time"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    
    def _open_terminal(self):
        """Open terminal"""
        terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "xterm"]
        for terminal in terminals:
            try:
                subprocess.Popen([terminal], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Opening {terminal}"
            except FileNotFoundError:
                continue
        return "No terminal found"
    
    def _open_file_manager(self):
        """Open file manager"""
        file_managers = ["nautilus", "dolphin", "thunar", "nemo", "pcmanfm"]
        for fm in file_managers:
            try:
                subprocess.Popen([fm], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Opening {fm}"
            except FileNotFoundError:
                continue
        return "No file manager found"
    
    def _open_calculator(self):
        """Open calculator"""
        calculators = ["gnome-calculator", "kcalc", "galculator", "qalculate"]
        for calc in calculators:
            try:
                subprocess.Popen([calc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Opening {calc}"
            except FileNotFoundError:
                continue
        return "No calculator found"
    
    # ===== Intent-based handlers (v0.2) =====
    
    def _handle_open_application(self, params: Dict[str, Any]) -> str:
        """Handle open_application intent"""
        app_name = params.get("application", "").lower()
        
        # Map common application names
        app_map = {
            "browser": self._open_browser,
            "firefox": self._open_browser,
            "chrome": lambda: self._open_browser("google-chrome"),
            "terminal": self._open_terminal,
            "file manager": self._open_file_manager,
            "files": self._open_file_manager,
            "calculator": self._open_calculator,
            "calc": self._open_calculator,
        }
        
        handler = app_map.get(app_name)
        if handler:
            return handler()
        
        # Try to open by name directly
        try:
            subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Opening {app_name}"
        except FileNotFoundError:
            return f"Application '{app_name}' not found"
    
    def _handle_screenshot(self, params: Dict[str, Any]) -> str:
        """Handle screenshot intent"""
        return self._take_screenshot()
    
    def _handle_time_query(self, params: Dict[str, Any]) -> str:
        """Handle time query intent"""
        return self._get_time()
    
    def _handle_system_control(self, params: Dict[str, Any]) -> str:
        """Handle system control intent"""
        action = params.get("action", "").lower()
        
        commands = {
            "shutdown": "systemctl poweroff",
            "restart": "systemctl reboot",
            "reboot": "systemctl reboot",
            "sleep": "systemctl suspend",
            "suspend": "systemctl suspend",
        }
        
        command = commands.get(action)
        if command:
            logger.warning(f"System control command requested: {action}")
            return f"System {action} command requires elevated privileges"
        
        return f"Unknown system control action: {action}"
    
    def _handle_volume_control(self, params: Dict[str, Any]) -> str:
        """Handle volume control intent"""
        try:
            if "level" in params:
                level = params["level"]
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
                return f"Volume set to {level}%"
            
            action = params.get("action", "").lower()
            if action in ["increase", "raise"]:
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"], check=True)
                return "Volume increased"
            elif action in ["decrease", "lower"]:
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"], check=True)
                return "Volume decreased"
            elif action == "mute":
                subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"], check=True)
                return "Audio muted"
            elif action == "unmute":
                subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"], check=True)
                return "Audio unmuted"
        except Exception as e:
            logger.error(f"Volume control error: {e}")
            return "Volume control not available"
    
    def _handle_search(self, params: Dict[str, Any]) -> str:
        """Handle search intent"""
        query = params.get("query", "")
        if query:
            # Open browser with search
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            try:
                for browser in ["firefox", "google-chrome", "chromium"]:
                    try:
                        subprocess.Popen([browser, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return f"Searching for: {query}"
                    except FileNotFoundError:
                        continue
            except Exception as e:
                logger.error(f"Search error: {e}")
        return "Search failed"

