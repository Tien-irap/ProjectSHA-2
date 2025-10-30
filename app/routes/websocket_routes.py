from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from ..core.websockets_connection import manager

router = APIRouter()

@router.websocket("/ws/feed")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for the live hashing feed."""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep the connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)