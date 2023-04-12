
from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect,
    Depends)

from sqlalchemy.orm import Session

from src.database import get_db

from src.auth.crud import get_user_by_id
from src.auth.oa2auth import required_user

from src.chat.manager import manager
from src.chat.exceptions import ChatPermissionRequired, ChatNotFound
from src.chat.crud import get_chat_by_id

router = APIRouter()

@router.websocket("/chat/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket, chat_id: int,
                             user_id: str = Depends(required_user),
                             db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # todo: make message read by user
            
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
