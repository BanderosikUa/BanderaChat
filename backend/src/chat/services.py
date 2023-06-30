from secrets import token_hex

from fastapi import UploadFile

from src.config import LOGGER, settings, MEDIA_DIR, bucket

from src.chat.schemas import Chat as ChatSchema, MessageResponse
from src.user.schemas import User as UserSchema

from src.chat.models import Chat, Message


def setup_default_chat_photo_and_title(user: UserSchema, 
                                       chats: list[Chat]) -> list[ChatSchema]:
    chats = [ChatSchema.from_orm(chat_db) for chat_db in chats]
    for chat in chats:
        if chat.is_direct and not chat.photo:
            interlocutor = None
            for participant in chat.participants:
                if user.id != participant.id:
                    interlocutor = participant
            chat.photo = interlocutor.photo if interlocutor else chat.photo
            chat.title = interlocutor.username if interlocutor else chat.name
    return chats


def setup_message_type(user: UserSchema,
                       messages: list[Message]) -> list[MessageResponse]:
    messages = [MessageResponse.from_orm(message_db) for message_db in messages]
    for message in messages:
        if message.user.id == user.id:
            message.type = "own"
        else:
            message.type = "other"
    return messages


def save_photo_to_google_bucket(photo: UploadFile) -> str:
    filename = f"{token_hex(10)}.jpg"
    photo.filename = filename
    
    blob = bucket.blob(filename)
    blob.upload_from_file(photo.file)
    return filename


def save_photo_locally(photo: UploadFile) -> str:
    contents = photo.read()
    filename = f"{token_hex(10)}.jpg"
    photo.filename = filename
    filepath = settings.MEDIA_DIR / filename
    filepath.write_bytes(contents)
    
    return filename
    
