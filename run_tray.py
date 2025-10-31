#!/usr/bin/env python3
"""
NuxAI System Tray Launcher
Runs NuxAI backend with system tray icon
"""
import sys
import subprocess
import threading
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from core.system_tray import SystemTray
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


def start_backend():
    """Start the backend server in a subprocess"""
    logger.info("Starting NuxAI backend...")
    
    backend_path = Path(__file__).parent / "backend" / "main.py"
    
    process = subprocess.Popen(
        [sys.executable, str(backend_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(backend_path.parent)
    )
    
    logger.info(f"Backend started with PID: {process.pid}")
    return process


def main():
    """Main entry point"""
    print("🚀 Starting NuxAI with System Tray...")
    
    # Start backend in background
    backend_process = start_backend()
    
    # Give backend time to start
    time.sleep(2)
    
    # Initialize and run system tray
    print("🎨 Initializing system tray...")
    tray = SystemTray(config.config)
    tray.initialize()
    
    if tray.enabled:
        print("✅ System tray ready!")
        print("   • NuxAI is now running in the background")
        print("   • Right-click the tray icon for options")
        print("   • Press Ctrl+C to quit")
        
        try:
            # Run tray (blocking)
            tray.run()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
        finally:
            # Cleanup
            tray.stop()
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("✅ Shutdown complete")
    else:
        print("⚠️  System tray not available")
        print("   Backend is still running...")
        print("   Press Ctrl+C to quit")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            backend_process.terminate()
            backend_process.wait(timeout=5)


if __name__ == "__main__":
    main()

