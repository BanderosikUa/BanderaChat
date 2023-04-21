import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.config import LOGGER
from src.chat.schemas import MessageCreate
from src.chat.crud import create_message

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    #  todo: mark read message here!! 

    # async def send_personal_message(self, message: MessageCreate, websocket: WebSocket):
    #     create_message(MessageCreate)
    #     await websocket.send_text(message.message) 
    
    # async def receive_text(self, websocket: WebSocket) -> str:
    #     data = await websocket.receive_text()
    #     return data

    async def broadcast(self, message: MessageCreate, sender: WebSocket, add_to_db: bool = True):
        LOGGER.debug(f"Broadcasting across {len(self.active_connections)} CONNECTIONS")
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(message.schema_json(indent=2))
                LOGGER.debug(f"Broadcasting: {message.dict()}")

manager = ConnectionManager()
