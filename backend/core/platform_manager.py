"""
Platform Manager (v0.6)
Cross-platform abstraction layer for Windows, macOS, and Linux
"""
import platform
import subprocess
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PlatformManager:
    """Manages platform-specific operations"""
    
    def __init__(self):
        self.system = platform.system()
        logger.info(f"🖥️  Platform detected: {self.system}")
    
    def is_linux(self) -> bool:
        return self.system == "Linux"
    
    def is_windows(self) -> bool:
        return self.system == "Windows"
    
    def is_macos(self) -> bool:
        return self.system == "Darwin"
    
    def open_application(self, app_name: str) -> bool:
        """Open an application across platforms"""
        try:
            if self.is_linux():
                return self._open_linux(app_name)
            elif self.is_windows():
                return self._open_windows(app_name)
            elif self.is_macos():
                return self._open_macos(app_name)
            return False
        except Exception as e:
            logger.error(f"Error opening {app_name}: {e}")
            return False
    
    def _open_linux(self, app_name: str) -> bool:
        """Open application on Linux"""
        app_map = {
            "browser": "firefox",
            "chrome": "google-chrome",
            "firefox": "firefox",
            "terminal": "gnome-terminal",
            "files": "nautilus",
            "calculator": "gnome-calculator"
        }
        
        command = app_map.get(app_name.lower(), app_name)
        subprocess.Popen([command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    
    def _open_windows(self, app_name: str) -> bool:
        """Open application on Windows"""
        app_map = {
            "browser": "start microsoft-edge:",
            "chrome": "start chrome",
            "firefox": "start firefox",
            "terminal": "start cmd",
            "files": "start explorer",
            "calculator": "start calc",
            "notepad": "start notepad"
        }
        
        command = app_map.get(app_name.lower(), f"start {app_name}")
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    
    def _open_macos(self, app_name: str) -> bool:
        """Open application on macOS"""
        app_map = {
            "browser": "Safari",
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "terminal": "Terminal",
            "files": "Finder",
            "calculator": "Calculator"
        }
        
        app = app_map.get(app_name.lower(), app_name)
        subprocess.Popen(["open", "-a", app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    
    def take_screenshot(self, filename: str) -> Optional[str]:
        """Take screenshot across platforms"""
        try:
            if self.is_linux():
                return self._screenshot_linux(filename)
            elif self.is_windows():
                return self._screenshot_windows(filename)
            elif self.is_macos():
                return self._screenshot_macos(filename)
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return None
    
    def _screenshot_linux(self, filename: str) -> str:
        """Screenshot on Linux"""
        subprocess.run(["gnome-screenshot", "-f", filename], check=True)
        return filename
    
    def _screenshot_windows(self, filename: str) -> str:
        """Screenshot on Windows"""
        # Use PowerShell to take screenshot
        ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save('{filename}')
        """
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        return filename
    
    def _screenshot_macos(self, filename: str) -> str:
        """Screenshot on macOS"""
        subprocess.run(["screencapture", filename], check=True)
        return filename
    
    def set_volume(self, level: int) -> bool:
        """Set system volume across platforms"""
        try:
            if self.is_linux():
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
            elif self.is_windows():
                # Uses nircmd (if installed) or powershell
                subprocess.run(["powershell", f"(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], shell=True)
            elif self.is_macos():
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"], check=True)
            return True
        except Exception as e:
            logger.error(f"Volume control error: {e}")
            return False
    
    def get_clipboard(self) -> Optional[str]:
        """Get clipboard content"""
        try:
            import pyperclip
            return pyperclip.paste()
        except:
            return None
    
    def set_clipboard(self, text: str) -> bool:
        """Set clipboard content"""
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except:
            return False

