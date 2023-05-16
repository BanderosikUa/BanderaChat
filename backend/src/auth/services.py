import random
import string

from sqlalchemy.orm import Session

from src.config import LOGGER, bucket

from src.auth.models import User
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import UserLogin, UserRegister
from src.auth.security import check_password
from src.auth.crud import get_user_by_username, get_user_by_email


async def authenticate_user(db: Session, auth_data: UserLogin) -> User:
    user = await get_user_by_username(db, auth_data.username)
    if auth_data.email:
        user = await get_user_by_email(db, auth_data.email)
    else:
        user = await get_user_by_username(db, auth_data.username)
    
    
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user

# async def appoint_user_default_photo(user: UserRegister):
#     try:
#         default_name = random.choice(
#             ["default.png", "default1.png", 
#              "default2.png", "default3.png"])
#         photo_url = bucket.blob(default_name).public_url
#         user.photo = photo_url
#         return user
#     except Exception as e:
#         LOGGER.error(e)
#         user.photo = ""
#     return user 
