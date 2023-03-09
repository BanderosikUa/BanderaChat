import asyncio
import pytest
import pytest_asyncio

from typing import Any, Generator, AsyncGenerator

from async_asgi_testclient import TestClient

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from src.config import settings
from src.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin@mysql:3306/test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True,
)
# Use connect_args parameter only with sqlite
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True, scope="session")
def run_migrations() -> None:
    import os

    print("running migrations..")
    os.system("alembic upgrade head")

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    try:
        yield TestingSessionLocal()
    finally:
        TestingSessionLocal().close_all()
        Base.metadata.drop_all(bind=engine)
        
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    from src.main import app
    host, port = "127.0.0.1", "9000"
    scope = {"client": (host, port)}
    
    app.dependency_overrides[get_db] = override_get_db
    async with TestClient(app, scope=scope) as c:
        yield c
    del app.dependency_overrides[get_db]
