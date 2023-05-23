import re
from typing import Optional

from pydantic import EmailStr, Field, validator, constr, root_validator

from src.schemas import ORJSONModel

from src.auth.constants import ErrorCode
from src.user.schemas import User

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")

class UserRegister(User):
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
        return v
    
    
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

class AccessTokenResponse(ORJSONModel):
    status: bool
    access_token: str
