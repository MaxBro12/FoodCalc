import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_names(test_client: AsyncClient, test_db: DataBase):
    limit = 1000
    names = await test_db.products.names(limit=limit)
    ans = await test_client.get('/v1/products/names', params={'limit': limit})
    assert ans.status_code == 200
    assert len(ans.json().get('names')) <= limit
    assert len(ans.json().get('names')) == len(names)


async def test_names_low_limit(test_client: AsyncClient, test_db: DataBase):
    limit = 2
    names = await test_db.products.names(limit=limit)
    ans = await test_client.get('/v1/products/names', params={'limit': limit})
    assert ans.status_code == 200
    assert len(ans.json().get('names')) == limit
    assert len(ans.json().get('names')) == len(names)


async def test_search_correct(test_client: AsyncClient, test_db: DataBase):
    names = await test_db.products.names(limit=10)
    ans = await test_client.post('/v1/products/search', json={'id_or_name': names[0][0]})
    assert ans.status_code == 200
    assert len(ans.json().get('names')) == 1
    assert ans.json().get('names')[0]['id'] == names[0][0]
    assert ans.json().get('names')[0]['name'] == names[0][1]
    assert ans.json().get('names')[0]['search_index'] == names[0][2]


async def test_search_not_exists(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post('/v1/products/search', json={'id_or_name': '321'})
    assert ans.status_code == 200
    assert len(ans.json().get('names')) == 0
