import json

from datetime import datetime
from typing import List, Optional

from src.config import bucket
from src.schemas import AllOptional, ORJSONModel

from src.auth.schemas import User, UserEmbedded

from pydantic import BaseModel, validator

        
class ChatBase(ORJSONModel):
    title: Optional[str]
    is_direct: bool = False
    photo: str = ""
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class ChatCreate(ChatBase):
    participants: List[User]
    
    
class ChatUpdate(ChatBase):
    id: int
    is_direct: bool
    
class Chat(ChatBase, metaclass=AllOptional):
    id: int
    is_direct: bool
    participants: List[User] = []
    moderators: List[User] = []

    class Config:
        orm_mode = True
        
class ChatResponseItem(Chat):
    participants: List[UserEmbedded]
    moderators: List[UserEmbedded]
        
    @validator('photo', pre=True)
    def photo_formater(cls, v, values) -> str:
        if values.get("photo") and not "http" in values.get("photo", ""):
            photo = bucket.blob(values["photo"]).public_url
        elif v and not "http" in v:
            photo = bucket.blob(v).public_url
        else:
            photo = v
        return photo
    
        
class ChatResponse(BaseModel):
    status: bool
    chat: ChatResponseItem
    

class ChatListResponse(BaseModel):
    status: bool
    chats: List[ChatResponseItem]

class MessageBase(BaseModel):
    user: UserEmbedded
    message: str
    
class MessageCreate(MessageBase):
    chat: Chat

class Message(MessageBase):
    id: int
    chat: Chat
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
        
class MessageResponse(MessageBase):
    id: int
    user: UserEmbedded
    created_at: datetime
    updated_at: datetime
    type: Optional[str]  # own message or other
    
    class Config:
        orm_mode = True
        
class WsData(BaseModel):
    action: str = ""
    user: User
    message: MessageResponse | None
    
class ChatDetailResponse(BaseModel):
    status: bool
    chat: ChatResponseItem
    messages: List[MessageResponse]
