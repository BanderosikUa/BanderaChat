import random
from datetime import datetime, timedelta
from pydantic import UUID4
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from src.schemas import PaginationParams

from src.auth import schemas
from src.auth.models import RefreshToken
from src.user.models import User
from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.security import check_password, hash_password, generate_random_alphanum

async def create_user(db: Session, user: schemas.UserRegister) -> User | None:
    hashed_pasword = hash_password(user.password)
    
    user.password = hashed_pasword
    
    if not user.photo:
        user.photo = random.choice(
            ["default.png", "default2.png", 
             "default3.png", "default4.png"]
            )
    
    user = user.dict()
    del user['passwordConfirm']
    
    db_user = User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


async def create_refresh_token(
    db: Session, *, user_id: int, refresh_token: str | None = None
    ) -> str:
    if not refresh_token:
        refresh_token = generate_random_alphanum(64)
        
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
