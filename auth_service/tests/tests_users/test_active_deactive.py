import pytest
from httpx import AsyncClient
from app.database.repo import DataBase


async def test_deactive(test_client: AsyncClient, test_db: DataBase):
    user = await test_db.users.by_name('test_user')
    ans = await test_client.post(f'/v1/users/deactive/{user.id}')
    assert ans.status_code == 200
    assert ans.json()['ok'] == True


async def test_active(test_client: AsyncClient, test_db: DataBase):
    user = await test_db.users.by_name('test_user')
    ans = await test_client.post(f'/v1/users/active/{user.id}')
    assert ans.status_code == 200
    assert ans.json()['ok'] == True
