import pytest
from httpx import AsyncClient
from app.database.repo import DataBase


async def test_all_users(test_client: AsyncClient, test_db: DataBase):
    users = await test_client.get('/v1/users')
    assert users.status_code == 200
    assert len(users.json()['users']) == await test_db.users.count()


async def test_user_pagination_small(test_client: AsyncClient):
    users = await test_client.get('/v1/users', params={'skip': 0, 'limit': 1})
    assert users.status_code == 200
    assert len(users.json()['users']) == 1


async def test_user_pagination_large(test_client: AsyncClient):
    users = await test_client.get('/v1/users', params={'skip': 0, 'limit': 10})
    assert users.status_code == 200
    assert len(users.json()['users']) == 2
