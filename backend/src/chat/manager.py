import json
import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from sqlalchemy.orm import Session

from src.config import LOGGER
from src.chat.schemas import MessageCreate, WsData, User, UserEmbedded
from src.chat.crud import create_message
from src.chat import crud, schemas, services

def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

class WebSocketManager:
    actions: list[str] = []
    encoding = 'json'
    
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        LOGGER.info(self.connections)
        await self.add_connection(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        if ws in self.connections:
            self.connections.remove(ws)

    async def add_connection(self, ws: WebSocket) -> None:
        self.connections.append(ws)

    async def send_personal_message(self, ws: WebSocket, message: dict) -> None:
        await ws.send_json(message)

    async def broadcast(self, message: dict) -> None:
        for connection in self.connections:
            await connection.send_json(message)

    async def broadcast_exclude(self, wss: list[WebSocket], message: dict) -> None:
        for connection in self.connections:
            if connection not in wss:
                await connection.send_json(message)
                
    async def actions_not_allowed(self, *, ws: WebSocket,
                                  data: dict, db: Session = None) -> None:
        await ws.send_json({'action': 'Not found'})
        
    async def on_receive(self, *, ws: WebSocket,
                         data: dict, db: Session = None) -> None:
        if data["action"] in self.actions:
            handler = getattr(self, data["action"], self.actions_not_allowed)
        else:
            handler = self.actions_not_allowed
        return await handler(ws=ws, db=db, data=data)
    
class ConnectionManager(WebSocketManager):
    actions = ['join', 'send_message', 'close', 'delete', 'edit', "ping"]

    async def ping(self, *, ws: WebSocket,
                   data: dict, db: Session = None) -> None:
        await ws.send_json({"action": "pong"})
        
    async def on_online(self, *, ws: WebSocket,
                        data: dict, db: Session = None) -> None:
        user = data['user']
        user = UserEmbedded.from_orm(user)
        await self.broadcast({'action': 'online', 
                              'user': user.dict()})
        
    async def on_error(self, *, ws: WebSocket,
                       data: dict, db: Session = None) -> None:
        response = {"action": "error", "message": data["error"]}
        await self.send_personal_message(ws, response)
        await self.disconnect(ws)

    async def join(self, *, ws: WebSocket,
                   data: dict, db: Session = None) -> None:
        user = data["user"]
        user = UserEmbedded.from_orm(user)
        
        await self.broadcast({'action': 'join',
                              "user": user.dict(),
                              'message': f"{user.username} join the chat"})

    async def close(self, *, ws: WebSocket,
                    data: dict, db: Session = None) -> None:
        user = data["user"]
        
        user = UserEmbedded.from_orm(user)
        
        await self.broadcast_exclude(
            [ws],
            {'action': 'disconnect', 
             "user": user.json(),
             'message': f"{user.username} has disconnected"}
        )
        await self.disconnect(ws)

    async def send_message(self, *, ws: WebSocket,
                           data: dict, db: Session = None) -> None:
        user = data["user"]
        chat = data["chat"]
        
        message = schemas.MessageCreate(
                user=user, chat=chat, message=data['message'],
                )
        message = await crud.create_message(db, message)
        message = schemas.MessageResponse.from_orm(message)
        message.type = "other"
        
        user = UserEmbedded.from_orm(user)
        
        await self.broadcast_exclude([ws], {
            'action': 'newMessage',
            'user': json.loads(user.json()),
            'message': json.loads(message.json()),
        })
                
manager = ConnectionManager()
