from fastapi import Depends

from sqlalchemy.orm import Session

from src.database import get_db

from src.auth.dependencies import required_user
from src.auth.models import User
from src.auth.crud import get_user_by_id

from src.chat.crud import get_chat_by_id
from src.chat.models import Chat
from src.chat.exceptions import ChatPermissionRequired, ChatNotFound

def valid_chat(chat_id: str, user: User, db : Session = Depends(get_db)) -> Chat:
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    return chat
