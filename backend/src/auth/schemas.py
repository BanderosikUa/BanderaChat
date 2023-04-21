import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, validator, constr, root_validator

from src.config import LOGGER
from src.models import ORJSONModel
from src.schemas import AllOptional

from src.auth.constants import ErrorCode

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")

class UserBase(ORJSONModel):
    username: Optional[str]
    email: Optional[EmailStr]
    photo: Optional[str] = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    verified: Optional[bool] = False

class UserRegister(UserBase):
    username: str = Field(max_length=128, min_length=3)
    email: EmailStr
    password: constr(min_length=8)
    passwordConfirm: str
    
    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password
    
    @validator("passwordConfirm")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("password")
        
        if password and password != v:
            raise ValueError(ErrorCode.PASSWORD_NOT_MATCH)
        return values
    
    
class UserLogin(ORJSONModel):
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
    id: int
    is_admin: bool
    
    class Config:
        orm_mode = True

class UserResponseSchema(UserBase):
    id: int

class UserResponse(ORJSONModel):
    status: str
    user: UserResponseSchema
    
        
class AccessTokenResponse(ORJSONModel):
    status: str
    access_token: str
