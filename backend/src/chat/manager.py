import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.config import LOGGER
from src.chat.schemas import MessageCreate, WsData
from src.chat.crud import create_message


class WebSocketManager:
    actions: list[str] = []
    encoding = 'json'
    
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        await self.add_connection(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.connections.remove(websocket)

    async def add_connection(self, websocket: WebSocket) -> None:
        self.connections.append(websocket)

    async def send_message(self, websocket: WebSocket, message: dict) -> None:
        await websocket.send_json(message)

    async def broadcast(self, message: dict) -> None:
        for connection in self.connections:
            await connection.send_json(message)

    async def broadcast_exclude(self, websockets: list[WebSocket], message: dict) -> None:
        for connection in self.connections:
            if connection not in websockets:
                await connection.send_json(message)
                
    async def actions_not_allowed(self, websocket: WebSocket, data: dict | None) -> None:
        await websocket.send_json({'action': 'Not found'})
        
    async def on_receive(self, websocket: WebSocket, data: WsData) -> None:
        if data.action in self.actions:
            handler = getattr(self, data.action, self.actions_not_allowed)
        else:
            handler = self.actions_not_allowed
        LOGGER.info(handler.__name__)
        return await handler(websocket, data)

class ConnectionManager(WebSocketManager):
    actions = ['join', 'send_message', 'close']
    manager = WebSocketManager()

    async def join(self, websocket: WebSocket, data: WsData) -> None:
        await self.manager.broadcast({'action': 'join', 
                                      'message': f"{data.user.id} connected"})

    async def close(self, websocket: WebSocket, data: WsData) -> None:
        await self.manager.disconnect(websocket)
        await self.broadcast_exclude(
            [websocket],
            {'action': 'disconnect', 'message': f"{data.user.id} disconnected"}
        )

    async def send_message(self, websocket: WebSocket, data: WsData) -> None:
        await self.manager.broadcast({
            'action': 'newMessage',
            'username': data.user.username,
            'message': data.message.json()
        })
                
manager = ConnectionManager()
