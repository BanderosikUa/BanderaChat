import re
from datetime import datetime
from typing import Optional
from fastapi.responses import FileResponse
from fastapi import Request, Depends

from pydantic import EmailStr, Field, validator, constr, root_validator

from src.config import LOGGER, settings
from src.schemas import AllOptional, ORJSONModel

from src.auth.constants import ErrorCode


class UserBase(ORJSONModel):
    username: Optional[str]
    
# class UserUpdate(UserBase):
#     id: Optional[int]
#     email: Optional[EmailStr]

    
class User(UserBase):
    id: Optional[int]
    email: Optional[EmailStr]
    photo: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    verified: Optional[bool] = False
    
    class Config:
        orm_mode = True

class UserResponseSchema(User):
    id: int
    

class UserEmbedded(UserBase):
    id: int
    photo: str = ""
    
    class Config:
        orm_mode = True

class UserResponse(ORJSONModel):
    status: bool
    user: UserResponseSchema
    
    
class UserResponseList(ORJSONModel):
    status: bool
    users: list[UserEmbedded]
