from fastapi import Depends

from sqlalchemy.orm import Session

from src.database import get_db

from src.chat.schemas import MessageCreate
from src.chat.models import Chat, Message

def get_chat_by_id(chat_id: int, db: Session = Depends(get_db), ) -> Chat | None:
    select_query = db.query(Chat).filter(Chat.id == chat_id)

    return select_query.one_or_none()

def create_message(message: MessageCreate, db: Session = Depends(get_db), ) -> None:
    message = message.dict()
    db_message = Message(**message)
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # return db_message
