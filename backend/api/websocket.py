"""
WebSocket API Router
Handles WebSocket connections from the overlay
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.websocket_manager import ConnectionManager
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()
manager = ConnectionManager()


@router.websocket("/overlay")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for overlay communication"""
    await manager.connect(websocket)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connected",
            "message": "Connected to NuxAI backend"
        }, websocket)
        
        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_json()
            logger.debug(f"Received from overlay: {data}")
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": data.get("timestamp")
                }, websocket)
            
            elif message_type == "overlay_ready":
                logger.info("Overlay is ready")
                await manager.send_personal_message({
                    "type": "backend_ready",
                    "message": "Backend is ready"
                }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

