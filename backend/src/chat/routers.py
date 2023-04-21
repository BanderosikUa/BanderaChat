
from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect,
    Depends)

from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import PaginationParams

from src.auth.dependencies import required_user, websocket_required_user
from src.auth.schemas import User
from src.config import LOGGER

from src.chat.manager import manager
# from src.chat. import Chat
from src.chat import crud, schemas
from src.chat.dependencies import valid_chat

router = APIRouter()


@router.get("/chats/{chat_id}/access")
async def websocket_access(chat: schemas.Chat = Depends(valid_chat),
                           user: User = Depends(required_user)):
    return {'status': True, "chat": chat.id, "user": user.id}

@router.websocket("/chats/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket,
                            #  chat: schemas.Chat = Depends(valid_chat),
                             user: User = Depends(websocket_required_user),
                             db: Session = Depends(get_db)):
    # await manager.connect(websocket)
    chat = schemas.Chat(id=1, title='test')
    try:
        while True:
            data = await websocket.receive_text()
            # todo: make message read by user
            LOGGER.debug(data)
            message = schemas.MessageCreate(
                user.id, chat.id, f"Client #{user.id} says: {data}"
                )
            crud.create_message(db, message)
            # await manager.send_personal_message(message, websocket)
            
            await manager.broadcast(message, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = schemas.MessageCreate(
            user.id, chat.id, f"Client #{user.id} says: {data}"
            )
        await manager.broadcast(message, websocket, add_to_db=False)

@router.post("/chats")
async def create_chat(chat_data: schemas.ChatCreate,
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> schemas.ChatResponse:
    chat = await crud.create_chat(db, chat_data, user)
    return {'status': True, 'chat': chat}
    
@router.get("/chats")
async def get_users_chats(pagination: PaginationParams = Depends(),
                          user: User = Depends(required_user),
                          db: Session = Depends(get_db)) -> schemas.ChatListResponse:
    chats = await crud.get_chats(db, pagination, user)
    LOGGER.info(chats)
    return {"status": True, "chats": chats}
