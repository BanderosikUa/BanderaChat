from secrets import token_hex

from fastapi import UploadFile

from src.config import LOGGER, bucket

from src.chat import schemas as chat_schemas
from src.auth import schemas as auth_schemas

from src.chat.models import Chat, Message


def setup_default_chat_photo_and_title(user: auth_schemas.User, 
                                       chats: list[Chat]) -> list[chat_schemas.Chat]:
    chats = [chat_schemas.Chat.from_orm(chat_db) for chat_db in chats]
    for chat in chats:
        if chat.is_direct and not chat.photo:
            interlocutor = None
            for participant in chat.participants:
                if user.id != participant.id:
                    interlocutor = participant
            chat.photo = interlocutor.photo if interlocutor else chat.photo
            chat.title = interlocutor.username if interlocutor else chat.name
    return chats

def setup_message_type(user: auth_schemas.User,
                       messages: list[Message]) -> list[chat_schemas.MessageResponse]:
    messages = [chat_schemas.MessageResponse.from_orm(message_db) for message_db in messages]
    for message in messages:
        if message.user.id == user.id:
            message.type = "own"
        else:
            message.type = "other"
    return messages

def save_photo(photo: UploadFile) -> str:
    filename = f"{token_hex(10)}.jpg"
    photo.filename = filename
    
    blob = bucket.blob(filename)
    blob.upload_from_file(photo.file)
    return filename
    
