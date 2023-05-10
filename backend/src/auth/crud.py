import uuid
import random
from datetime import datetime, timedelta
from pydantic import UUID4

from sqlalchemy.orm import Session

from src import utils
from src.config import LOGGER, bucket

from src.auth.models import User, RefreshToken
from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import UserRegister, UserLogin
from src.auth.security import check_password, hash_password

async def create_user(db: Session, user: UserRegister) -> User | None:
    hashed_pasword = hash_password(user.password)
    
    user.password = hashed_pasword
    
    if not user.photo:
        user.photo = random.choice(
            ["default.png", "default1.png", 
             "default2.png", "default3.png"]
            )
    
    user = user.dict()
    del user['passwordConfirm']
    
    db_user = User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


async def get_user_by_id(db: Session, user_id: int) -> User | None:
    select_query = db.query(User).filter(User.id == user_id)

    return select_query.one_or_none()


async def get_users_list_by_ids(db: Session, user_ids: list[int]) -> list[User]:
    select_query = db.query(User).filter(User.id.in_(user_ids))

    return select_query.all()

async def get_user_by_email(db: Session, email: str) -> User | None:
    select_query = db.query(User).filter(User.email == email)

    return select_query.one_or_none()

async def get_user_by_username(db: Session, username: str) -> User | None:
    select_query = db.query(User).filter(User.username == username)

    return select_query.one_or_none()


async def create_refresh_token(
    db: Session, *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)
        
    db_refresh_token = RefreshToken(
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)

    return refresh_token


async def get_refresh_token(db: Session, refresh_token: str) -> RefreshToken | None:
    select_query = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token)

    return select_query.one_or_none()


async def expire_refresh_token(db: Session, refresh_token_uuid: UUID4) -> None:
    db_refresh_token = db.query(RefreshToken).filter(RefreshToken.uuid == refresh_token_uuid).\
                          update({"expires_at": datetime.utcnow() - timedelta(days=1)})

    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)


async def authenticate_user(db: Session, auth_data: UserLogin) -> User:
    user = await get_user_by_username(auth_data.username)
    if auth_data.email:
        user = await get_user_by_email(db, auth_data.email)
    else:
        user = await get_user_by_username(db, auth_data.username)
    
    
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user
