"""
NuxAI Minimal API Server for Testing
Runs the API without audio/voice components
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.health import router as health_router
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NuxAI Backend (Test Mode)",
    description="Intelligent offline voice assistant - API Testing Mode",
    version=config.get("app.version", "1.0.0"),
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health router
app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": config.get("app.name", "NuxAI"),
        "version": config.get("app.version", "1.0.0"),
        "status": "running",
        "mode": "test",
        "message": "Intelligent Voice Assistant - API Test Mode (Audio disabled)",
        "personality": config.get("personality.name", "Nux"),
        "features": config.get("features", {})
    }


@app.get("/settings", response_class=HTMLResponse)
async def settings():
    """Settings page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NuxAI Settings</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>🎤 NuxAI Settings</h1>
        <div class="info">
            <h2>Test Mode Active</h2>
            <p>This is a minimal API server for testing purposes.</p>
            <p>Audio/voice features are disabled.</p>
            <p><strong>Version:</strong> 1.0.0</p>
            <p><strong>Status:</strong> Running</p>
        </div>
        <h3>API Endpoints:</h3>
        <ul>
            <li><a href="/">/</a> - Root endpoint</li>
            <li><a href="/api/health">/api/health</a> - Health check</li>
            <li><a href="/api/status">/api/status</a> - Detailed status</li>
            <li><a href="/docs">/docs</a> - API documentation</li>
        </ul>
    </body>
    </html>
    """


def main():
    """Main entry point"""
    host = config.get("server.host", "127.0.0.1")
    port = config.get("server.port", 8000)
    
    logger.info("🚀 Starting NuxAI API Test Server...")
    logger.info(f"   🌐 Server: http://{host}:{port}")
    logger.info(f"   📚 API Docs: http://{host}:{port}/docs")
    logger.info(f"   ⚙️  Settings: http://{host}:{port}/settings")
    logger.info("   ⚠️  Test Mode: Audio features disabled")
    
    uvicorn.run(
        "test_server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
