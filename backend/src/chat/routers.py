
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
from src.chat import crud, schemas, services
from src.chat.dependencies import valid_chat, websocket_valid_chat

router = APIRouter()


@router.get("/chats/{chat_id}/access")
async def websocket_access(chat: schemas.Chat = Depends(valid_chat),
                           user: User = Depends(required_user)):
    return {'status': True, "chat": chat.id, "user": user.id}

@router.websocket("/chats/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket,
                             chat: schemas.Chat = Depends(websocket_valid_chat),
                             user: User = Depends(websocket_required_user),
                             db: Session = Depends(get_db)):
    try:
        while True:
            data = await websocket.receive_json()
            data['user'] = User
            
            message = schemas.MessageCreate(
                user=user, chat=chat, message=data['message'],
                )
            message = await crud.create_message(db, message)
            message = schemas.Message.from_orm(message)
            
            data['message'] = message
            
            data = schemas.WsData(action=data['action'],
                                  user=user,
                                  message=message)
            LOGGER.info(data)
            # todo: make message read by user
            # LOGGER.debug(data)
            # await manager.send_personal_message(message, websocket)
            
            await manager.on_receive(websocket, data)
    except WebSocketDisconnect as err:
        LOGGER.info(err)
        LOGGER.info(f"{user.id} disconnected in {chat.id} chat")
        await manager.disconnect(websocket)
        # message = schemas.MessageCreate(
        #     user.id, chat.id, f"Client #{user.id}"
        #     )
        # await manager.broadcast(message, websocket, add_to_db=False)

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
    chats = services.setup_default_chat_photo_and_title(user, chats)
    return {"status": True, "chats": chats}

# @router.get("/chats/{chat_id}")
# async def get_chat(chat = Depends(valid_chat)) -> schemas.ChatResponse:
#     return {"status": True, "chat": chat}

@router.get("/chats/{chat_id}")
async def get_chat_detail(chat = Depends(valid_chat),
                          db: Session = Depends(get_db)) -> schemas.ChatDetailResponse:
    messages = await crud.get_messages_by_chat_id(db, chat_id=chat.id)
    return {"status": True, "chat": chat, "messages": messages}
