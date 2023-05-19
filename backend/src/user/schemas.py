import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, validator, constr, root_validator

from src.config import LOGGER, bucket
from src.schemas import AllOptional, ORJSONModel

from src.auth.constants import ErrorCode


class UserBase(ORJSONModel):
    username: Optional[str]
    
# class UserUpdate(UserBase):
#     id: Optional[int]
#     email: Optional[EmailStr]
    email: Optional[EmailStr]
    username: Optional[str] = Field(max_length=128, min_length=3)
    password: constr(min_length=8)
    
    class Config:
        validate_assignment = True
        
    @root_validator(pre=True)
    def validate_is_email_or_username(cls, values): # better name needed ;) 
        if sum([bool(v) for v in values.values()]) != 2:
            raise ValueError('Either email or username must be set.')
        return values
    
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
    
    @validator('photo', pre=True)
    def photo_formater(cls, v, values) -> str:
        if values.get("photo") and not "http" in values.get("photo", ""):
            photo = bucket.blob(values["photo"]).public_url
        elif v and not "http" in v:
            photo = bucket.blob(v).public_url
        else:
            photo = v
        return photo
    
class UserEmbedded(UserBase):
    id: int
    photo: str = ""
    
    class Config:
        orm_mode = True
        
    @validator('photo', pre=True)
    def photo_formater(cls, v, values) -> str:
        if values.get("photo") and not "http" in values.get("photo", ""):
            photo = bucket.blob(values["photo"]).public_url
        elif v and not "http" in v:
            photo = bucket.blob(v).public_url
        else:
            photo = v
        return photo

class UserResponse(ORJSONModel):
    status: bool
    user: UserResponseSchema
    
    
class UserResponseList(ORJSONModel):
    status: bool
    users: list[UserEmbedded]
