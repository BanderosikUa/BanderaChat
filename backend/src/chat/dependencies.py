from fastapi import Depends

from sqlalchemy.orm import Session

from src.database import get_db
from src.config import LOGGER

from src.chat.crud import get_chat_by_id
from src.chat.models import Chat
from src.chat.exceptions import ChatPermissionRequired, ChatNotFound

from src.auth.dependencies import websocket_required_user, required_user

from src.user.schemas import User


async def websocket_valid_chat(chat_id: int, 
                               user: User = Depends(websocket_required_user),
                               db: Session = Depends(get_db)) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    # chat = Chat.from_orm(chat)
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    return chat

async def valid_chat(chat_id: int, 
                     user: User = Depends(required_user),
                     db: Session = Depends(get_db)) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    # chat = Chat.from_orm(chat)
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    return chat
