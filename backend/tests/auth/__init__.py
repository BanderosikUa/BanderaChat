import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fastapi import status

from src.config import LOGGER
from src.auth.crud import create_user
from src.auth.schemas import UserRegister

@pytest.mark.asyncio
class TestUsersRouters:
        
    async def test_get_me(self, client: TestClient, db: Session):
        user_1 = UserRegister(username='test1', email='test1@world.com',
                              password="@Test123", passwordConfirm="@Test123")
        await create_user(db, user_1)
        resp = await client.post(
            "/auth/login",
            json={
                "email": "test1@world.com",
                "password": "@Test123",
            }
        )
        access_token = resp.json()['access_token']
        resp = await client.get(
            "/users/me",
            headers={"Autorization": f"Bearer {access_token}"}
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_json['status'] == True
        assert resp_json['status']['user']['username'] == user_1.username
        assert resp_json['status']['user']['email'] == user_1.email
        
