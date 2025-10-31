"""
System Tray (v1.0)
System tray icon and menu for NuxAI
"""
import asyncio
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SystemTray:
    """System tray integration"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.icon = None
        self.enabled = False
        
    def initialize(self):
        """Initialize system tray"""
        try:
            import pystray
            from PIL import Image, ImageDraw
            
            self.pystray = pystray
            
            # Create simple icon
            image = self._create_icon()
            
            # Create menu
            menu = pystray.Menu(
                pystray.MenuItem("NuxAI", self._on_clicked, default=True),
                pystray.MenuItem("Enable Voice", self._toggle_voice, checked=lambda item: self.config.get("voice_enabled", True)),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Settings", self._open_settings),
                pystray.MenuItem("Skills", self._open_skills),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self._quit)
            )
            
            self.icon = pystray.Icon("nuxai", image, "NuxAI Assistant", menu)
            self.enabled = True
            
            logger.info("🎨 System tray initialized")
            
        except ImportError:
            logger.warning("pystray not available, system tray disabled")
            self.enabled = False
        except Exception as e:
            logger.error(f"System tray initialization error: {e}")
            self.enabled = False
    
    def _create_icon(self):
        """Create tray icon"""
        from PIL import Image, ImageDraw
        
        # Create a simple circular icon
        size = 64
        image = Image.new('RGB', (size, size), color='black')
        draw = ImageDraw.Draw(image)
        
        # Draw blue circle
        draw.ellipse([8, 8, size-8, size-8], fill='#4A90E2', outline='white', width=2)
        
        # Draw "N" in center
        draw.text((size//2-8, size//2-12), "N", fill='white')
        
        return image
    
    def run(self):
        """Run the system tray (blocking)"""
        if self.enabled and self.icon:
            logger.info("Starting system tray...")
            self.icon.run()
    
    def stop(self):
        """Stop the system tray"""
        if self.enabled and self.icon:
            self.icon.stop()
    
    def _on_clicked(self, icon, item):
        """Handle tray icon click"""
        logger.info("Tray icon clicked")
        # Could show status window or trigger voice activation
    
    def _toggle_voice(self, icon, item):
        """Toggle voice recognition"""
        current = self.config.get("voice_enabled", True)
        self.config["voice_enabled"] = not current
        logger.info(f"Voice {'enabled' if not current else 'disabled'}")
    
    def _open_settings(self, icon, item):
        """Open settings"""
        logger.info("Opening settings...")
        # TODO: Launch settings UI
    
    def _open_skills(self, icon, item):
        """Open skills manager"""
        logger.info("Opening skills manager...")
        # TODO: Launch skills UI
    
    def _quit(self, icon, item):
        """Quit application"""
        logger.info("Quitting from system tray")
        icon.stop()

