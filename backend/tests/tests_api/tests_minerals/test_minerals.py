import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_minerals_all(test_client: AsyncClient, test_db: DataBase):
    minerals = await test_db.minerals.all()
    ans = await test_client.get('/v1/universe/minerals')
    assert ans.status_code == 200
    assert len(ans.json().get('minerals')) == len(minerals)
    assert ans.json().get('minerals')[0].get('id') is not None
    assert ans.json().get('minerals')[0].get('name') is not None
    assert ans.json().get('minerals')[0].get('description') is not None
    assert ans.json().get('minerals')[0].get('intake') is not None
    assert ans.json().get('minerals')[0].get('type_id') is not None
    assert ans.json().get('minerals')[0].get('type_name') is not None


async def test_minerals_pagination_params(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/minerals', params={'skip': 1, 'limit': 3})

    assert ans.status_code == 200
    assert len(ans.json().get('minerals')) == 3
    assert ans.json().get('minerals')[0].get('id') is not None
    assert ans.json().get('minerals')[0].get('name') is not None
    assert ans.json().get('minerals')[0].get('description') is not None
    assert ans.json().get('minerals')[0].get('intake') is not None
    assert ans.json().get('minerals')[0].get('type_id') is not None
    assert ans.json().get('minerals')[0].get('type_name') is not None


async def test_minerals_pagination_params_adt_1(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/minerals', params={'skip': 0, 'limit': 1})

    assert ans.status_code == 200
    assert len(ans.json().get('minerals')) == 1


async def test_types_all(test_client: AsyncClient, test_db: DataBase):
    minerals = await test_db.mineral_types.all()
    ans = await test_client.get('/v1/universe/types')
    assert ans.status_code == 200
    assert len(ans.json().get('types')) == len(minerals)
    assert ans.json().get('types')[0].get('id') is not None
    assert ans.json().get('types')[0].get('name') is not None
    assert ans.json().get('types')[0].get('description') is not None
    assert ans.json().get('types')[0].get('minerals') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('id') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('name') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('compact_name') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('description') is not None


async def test_types_pagination_params(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/types', params={'skip': 1, 'limit': 3})

    assert ans.status_code == 200
    assert len(ans.json().get('types')) == 3
    assert ans.json().get('types')[0].get('id') is not None
    assert ans.json().get('types')[0].get('name') is not None
    assert ans.json().get('types')[0].get('description') is not None
    assert ans.json().get('types')[0].get('minerals') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('id') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('name') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('compact_name') is not None
    assert ans.json().get('types')[0]['minerals'][0].get('description') is not None



async def test_types_pagination_params_adt_1(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/types', params={'skip': 0, 'limit': 1})

    assert ans.status_code == 200
    assert len(ans.json().get('types')) == 1
