"""
Command Execution Module
Executes system commands based on voice input
"""
import subprocess
import shlex
from datetime import datetime
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CommandExecutor:
    """Executes voice commands as system operations"""
    
    def __init__(self):
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


import asyncio

