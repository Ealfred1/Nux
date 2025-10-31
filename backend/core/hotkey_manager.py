"""
Hotkey Manager (v0.6)
Global hotkey support for activating NuxAI
"""
import asyncio
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HotkeyManager:
    """Manages global hotkeys"""
    
    def __init__(self, hotkey: str = "ctrl+shift+space"):
        self.hotkey = hotkey
        self.callback = None
        self.enabled = False
        self.keyboard_module = None
        
    def initialize(self):
        """Initialize hotkey system"""
        try:
            import keyboard
            self.keyboard_module = keyboard
            self.enabled = True
            logger.info(f"⌨️  Hotkey system initialized: {self.hotkey}")
        except ImportError:
            logger.warning("keyboard module not available, hotkeys disabled")
            self.enabled = False
        except Exception as e:
            logger.error(f"Hotkey initialization error: {e}")
            self.enabled = False
    
    def register_hotkey(self, callback):
        """Register a hotkey callback"""
        if not self.enabled:
            logger.warning("Hotkey system not available")
            return False
        
        try:
            self.callback = callback
            self.keyboard_module.add_hotkey(self.hotkey, self._hotkey_pressed)
            logger.info(f"✅ Hotkey registered: {self.hotkey}")
            return True
        except Exception as e:
            logger.error(f"Failed to register hotkey: {e}")
            return False
    
    def _hotkey_pressed(self):
        """Handle hotkey press"""
        if self.callback:
            logger.info(f"🔥 Hotkey activated: {self.hotkey}")
            # Run callback in async context if needed
            try:
                if asyncio.iscoroutinefunction(self.callback):
                    asyncio.create_task(self.callback())
                else:
                    self.callback()
            except Exception as e:
                logger.error(f"Hotkey callback error: {e}")
    
    def unregister(self):
        """Unregister hotkey"""
        if self.enabled and self.keyboard_module:
            try:
                self.keyboard_module.remove_hotkey(self.hotkey)
                logger.info("Hotkey unregistered")
            except:
                pass

