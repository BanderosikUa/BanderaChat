import re
from datetime import datetime

from pydantic import EmailStr, Field, validator, constr, root_validator

from src.config import LOGGER
from src.models import ORJSONModel

from src.auth.constants import ErrorCode

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")

class UserBase(ORJSONModel):
    username: str = Field(max_length=128, min_length=3)
    email: EmailStr
    photo: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None
    verified: bool = False

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserRegister(UserBase):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False
    
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
    
    # @validator("email")
    # def valid_email_duplicate(cls, email: EmailStr):
        
        
class UserLogin(ORJSONModel):
    email: EmailStr|None
    username: str|None = Field(max_length=128, min_length=3)
    password: constr(min_length=8)
    
    class Config:
        validate_assignment = True
        
    @root_validator(pre=True)
    def validate_is_email_or_username(cls, values): # better name needed ;) 
        if sum([bool(v) for v in values.values()]) != 2:
            raise ValueError('Either email or username must be set.')
        return values
    
class UserResponseSchema(UserBase):
    id: int
    pass

class UserResponse(ORJSONModel):
    status: str
    user: UserResponseSchema
    
        
# class UserCreate(UserBase):
#     @validator("password")
#     def valid_password(cls, password: str) -> str:
#         if not re.match(STRONG_PASSWORD_PATTERN, password):
#             raise ValueError(
#                 "Password must contain at least "
#                 "one lower character, "
#                 "one upper character, "
#                 "digit or "
#                 "special symbol"
#             )

#         return password
    
# class UserResponse(UserBase):
#     pass

# class JWTData(ORJSONModel):
#     user_id: int = Field(alias="sub")
#     is_admin: bool = False


class AccessTokenResponse(ORJSONModel):
    status: str
    access_token: str
