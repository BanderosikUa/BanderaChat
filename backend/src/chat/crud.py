from sqlalchemy.orm import Session

from src.chat.models import Chat, Message

def get_chat_by_id(db: Session, chat_id: int) -> Chat | None:
    select_query = db.query(Chat).filter(Chat.id == chat_id)

    return select_query.one_or_none()
