from datetime import datetime

from fastapi import Cookie, Depends

from sqlalchemy.orm import Session

from src.config import LOGGER
from src.database import SessionLocal

from src.auth import crud, exceptions

from src.auth.models import RefreshToken


def _is_valid_refresh_token(db_refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at
