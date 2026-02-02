import pytest
from httpx import AsyncClient
from app.database.repo import DataBase


async def test_correct(test_client: AsyncClient, test_db: DataBase):
    user = await test_db.users.by_name('test_user')
    ans = await test_client.get(f'/v1/users/{user.id}')
    assert ans.json()['id'] == user.id
    assert ans.json()['name'] == user.name
    assert ans.json()['is_active'] == user.is_active
    assert ans.json()['is_admin'] == user.is_admin
    assert ans.json()['key_id'] == user.key_id


async def test_incorrect_id(test_client: AsyncClient):
    ans = await test_client.get(f'/v1/users/12345')
    assert ans.status_code == 404
    assert ans.json()['detail'] == 'User not found'
