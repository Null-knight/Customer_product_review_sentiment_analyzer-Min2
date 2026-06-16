from __future__ import annotations

from fastapi import WebSocket, WebSocketDisconnect

from src.api.server_state import processor


async def review_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            await websocket.send_json(processor.process_review(payload).__dict__)
    except WebSocketDisconnect:
        return

