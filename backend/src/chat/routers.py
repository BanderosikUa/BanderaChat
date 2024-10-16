from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect,
    Depends, UploadFile, File, Request)

from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import PaginationParams
from src.config import LOGGER, MEDIA_DIR

from src.chat import crud, schemas, services, exceptions
from src.chat.dependencies import (
    valid_chat, websocket_valid_chat
)
from src.chat.manager import manager

from src.auth.dependencies import required_user, websocket_required_user
from src.user.schemas import User


router = APIRouter()


@router.websocket("/chats/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket,
                             chat: schemas.Chat = Depends(websocket_valid_chat),
                             user: User = Depends(websocket_required_user),
                             db: Session = Depends(get_db)):
    """
    WebSocket endpoint that accepts a WebSocket connection.

    This endpoint will accept incoming WebSocket connections and will send
    a message to the client every second.
    
    Connection accept inside websocket_required_user dependencies
    """
    data = {"user": user}
    
    await manager.on_online(ws=websocket, db=db, data=data)
    try:
        
        while True:
            data = await websocket.receive_json()
            data["user"] = user
            data["chat"] = chat
            
            LOGGER.info(data)
            
            await manager.on_receive(ws=websocket, data=data, db=db)
    except WebSocketDisconnect as e:
        LOGGER.opt(exception=True).error(e)
        LOGGER.info(f"{user.id} disconnected in {chat.id} chat")
        await manager.disconnect(websocket)
    except Exception as e:
        LOGGER.opt(exception=True).error(e)
        data["error"] = str(e)[:50]
        await manager.on_error(ws=websocket, data=data, db=db)
        

@router.post("/chats")
async def create_chat(request: Request,
                      chat_data: schemas.ChatCreate,
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> schemas.ChatResponse:
    chat = await crud.create_chat(db, chat_data, user)
    
    return {'status': True, 'chat': chat}


@router.post("/chats/{chat_id}/upload")
async def upload_photo_to_chat(request: Request,
                               chat: schemas.Chat = Depends(valid_chat),
                               photo: UploadFile = File(...),
                               user: User = Depends(required_user),
                               db: Session = Depends(get_db)) -> schemas.ChatResponse:
    chat = schemas.ChatUpdate.from_orm(chat)
    extension = photo.filename.split(".")[-1]
    
    if extension not in ["jpg", "jpeg", "png"]:
        raise exceptions.PhotoExtensionNotAlllow()
    
    filename = services.save_photo_locally(photo)
    chat.photo = filename
    
    chat = await crud.update_chat(db, chat)
    
    return {"status": True, "chat": chat}
    

@router.get("/chats")
async def get_users_chats(request: Request,
                          pagination: PaginationParams = Depends(),
                          user: User = Depends(required_user),
                          db: Session = Depends(get_db)) -> schemas.ChatListResponse:
    chats = await crud.get_chats(db, pagination, user)
    chats = services.setup_default_chat_photo_and_title(user, chats)
    
    return {"status": True, "chats": chats}


@router.get("/chats/{chat_id}")
async def get_chat_detail(request: Request,
                          chat = Depends(valid_chat),
                          user: User = Depends(required_user),
                          db: Session = Depends(get_db)) -> schemas.ChatDetailResponse:
    messages = await crud.get_messages_by_chat_id(db, chat_id=chat.id)
    messages = services.setup_message_type(user, messages)
    chat = services.setup_default_chat_photo_and_title(user, [chat])[0]
    
    return {"status": True, "chat": chat, "messages": messages}
