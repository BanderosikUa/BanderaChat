import os
from pathlib import Path

from typing import Any
from pydantic import BaseSettings, root_validator
from pydantic.networks import MultiHostDsn
from loguru import logger as LOGGER

from src.constants import Environment

BASE_DIR = Path(__file__).resolve().parent

LOGGER.add(f'{BASE_DIR.parent}/logs/info.log', level='INFO', rotation="10 MB")

class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"
        
    DATABASE_URL: MultiHostDsn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(os.getenv('DATABASE_USERNAME'), 
                                                                                      os.getenv('DATABASE_PASSWORD'), 
                                                                                      os.getenv('DATABASE_HOST'), 
                                                                                      os.getenv('DATABASE_SOCKET'), 
                                                                                      os.getenv('DATABASE'),
                                                                                      )
    DATABASE_TEST_URL: MultiHostDsn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(os.getenv('DATABASE_USERNAME'), 
                                                                                      os.getenv('DATABASE_PASSWORD'), 
                                                                                      os.getenv('DATABASE_HOST'), 
                                                                                      os.getenv('DATABASE_SOCKET'), 
                                                                                      os.getenv('DATABASE_TEST', 'test'),
                                                                                      )
    
    # REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.LOCAL

    SENTRY_DSN: str | None

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str] = ["*"]
    
    # root_path: str = BASE_DIR.as_posix()

    APP_VERSION: str = "1"

    @root_validator(skip_on_failure=True)
    def validate_sentry_non_local(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data["ENVIRONMENT"].is_deployed and not data["SENTRY_DSN"]:
            raise ValueError("Sentry is not set")

        return data

settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
