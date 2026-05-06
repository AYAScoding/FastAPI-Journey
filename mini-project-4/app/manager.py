from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, poll_id: str, websocket: WebSocket):
        # Establish the connection exactly once
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []
        self.active_connections[poll_id].append(websocket)

    def disconnect(self, poll_id: str, websocket: WebSocket):
        if poll_id in self.active_connections:
            if websocket in self.active_connections[poll_id]:
                self.active_connections[poll_id].remove(websocket)

    async def broadcast(self, poll_id: str, message: dict):
        if poll_id in self.active_connections:
            for connection in self.active_connections[poll_id]:
                await connection.send_json(message)

manager = ConnectionManager()