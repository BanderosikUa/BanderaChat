
from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect,
    Depends)

from sqlalchemy.orm import Session

from src.database import get_db

from src.auth.dependencies import required_user
from src.auth.models import User

from src.chat.manager import manager
from src.chat.models import Chat
from src.chat.schemas import MessageCreate
from src.chat.dependencies import valid_chat
from src.chat.crud import create_message

router = APIRouter()

@router.websocket("/chat/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket,
                             user: User = Depends(required_user),
                             chat: Chat = Depends(valid_chat),
                             db: Session = Depends(get_db)):
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # todo: make message read by user
            
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            
            create_message(MessageCreate(user.id, chat.id, data))
            
            await manager.broadcast(f"Client #{user.id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user.id} left the chat")
