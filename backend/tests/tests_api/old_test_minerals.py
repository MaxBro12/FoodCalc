import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_minerals_pagination(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.get('/v1/universe/minerals')
    assert ans.status_code == 200
    assert len(ans.json().get('minerals')) >= 0
    assert ans.json().get('minerals')[0].get('id') is not None
    assert ans.json().get('minerals')[0].get('name') is not None
    assert ans.json().get('minerals')[0].get('description') is not None
    assert ans.json().get('minerals')[0].get('intake') is not None
    assert ans.json().get('minerals')[0].get('type_id') is not None
    assert ans.json().get('minerals')[0].get('type_name') is not None


async def test_minerals_pagination_params(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.get('/v1/universe/minerals/', params={'skip': 1, 'limit': 10})

    assert ans.status_code == 200
    assert len(ans.json().get('minerals')) == 10
    assert ans.json().get('minerals')[0].get('id') is not None
    assert ans.json().get('minerals')[0].get('name') is not None
    assert ans.json().get('minerals')[0].get('description') is not None
    assert ans.json().get('minerals')[0].get('intake') is not None
    assert ans.json().get('minerals')[0].get('type_id') is not None
    assert ans.json().get('minerals')[0].get('type_name') is not None


async def test_minerals_by_id(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/minerals/1')

    assert ans.status_code == 200
    assert ans.json().get('name') == 'Белки'
    assert ans.json().get('description') == 'Строительный материал для клеток, тканей (мышцы, кожа, волосы), ферментов, гормонов, антител. Вторичный источник энергии.'
    assert ans.json().get('intake') == 4
    assert ans.json().get('type_id') == 1
    assert ans.json().get('type_name') == 'Макронутриенты'


async def test_minerals_by_id_wrong(test_client: AsyncClient):
    ans = await test_client.get(f'/v1/universe/minerals/100')

    assert ans.status_code == 404
    assert ans.json().get('detail') == 'Минерал не найден'


async def test_minerals_del_by_id(test_client: AsyncClient, test_db: DataBase):
    await test_db.minerals.new(
        name='test_name',
        compact_name='tn',
        description='test_description',
        intake=10,
        type_id=1,
        commit=True
    )
    test_id = await test_db.minerals.by_name('test_name')
    assert test_id is not None

    ans = await test_client.delete(f'/v1/universe/minerals/{test_id.id}')
    assert ans.status_code == 200
    assert ans.json().get('ok') == True


async def test_minerals_del_by_id_wrong(test_client: AsyncClient):
    ans = await test_client.delete(f'/v1/universe/minerals/1000')
    assert ans.status_code == 200
    assert ans.json().get('ok') == False


async def test_minerals_new(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post('/v1/universe/minerals/new', json={
        'name': 'test_name',
        'description': 'test_description',
        'intake': 10,
        'type_id': 1
    })
    assert ans.status_code == 200
    assert ans.json().get('ok') == True

    test_min = await test_db.minerals.by_name('test_name')
    assert test_min is not None

    assert await test_db.minerals.del_by_id(test_min.id)



async def test_types_pagination(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.get('/v1/universe/types/')

    assert ans.status_code == 200
    assert len(ans.json().get('types')) >= 0
    assert ans.json().get('types')[0].get('id') is not None
    assert ans.json().get('types')[0].get('name') is not None
    assert ans.json().get('types')[0].get('description') is not None
    assert ans.json().get('types')[0].get('minerals') is not None


async def test_types_pagination_params(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/types/', params={'skip': 1, 'limit': 2})

    assert ans.status_code == 200
    assert len(ans.json().get('types')) == 2
    assert ans.json().get('types')[0].get('id') is not None
    assert ans.json().get('types')[0].get('name') is not None
    assert ans.json().get('types')[0].get('description') is not None
    assert ans.json().get('types')[0].get('minerals') is not None


async def test_types_by_id(test_client: AsyncClient):
    ans = await test_client.get('/v1/universe/types/1')

    assert ans.status_code == 200
    assert ans.json().get('name') == 'Макронутриенты'
    assert ans.json().get('description') == 'Это основа питания. К ним относятся белки, жиры, углеводы, а также вода и клетчатка.'
    assert len(ans.json().get('minerals')) >= 3


async def test_types_by_id_wrong(test_client: AsyncClient):
    ans = await test_client.get(f'/v1/universe/types/100')

    assert ans.status_code == 404
    assert ans.json().get('detail') == 'Тип минералов не найден'


async def test_types_del_by_id(test_client: AsyncClient, test_db: DataBase):
    await test_db.mineral_types.new(
        name='test_name',
        description='test_description',
        commit=True
    )
    test_id = await test_db.mineral_types.by_name('test_name')
    assert test_id is not None

    ans = await test_client.delete(f'/v1/universe/types/{test_id.id}')
    assert ans.status_code == 200
    assert ans.json().get('ok') == True


async def test_types_del_by_id_wrong(test_client: AsyncClient):
    ans = await test_client.delete(f'/v1/universe/types/1000')
    assert ans.status_code == 200
    assert ans.json().get('ok') == False


async def test_types_new(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post('/v1/universe/types/new', json={
        'name': 'test_name',
        'description': 'test_description',
    })
    assert ans.status_code == 200
    assert ans.json().get('ok') == True

    test_min = await test_db.mineral_types.by_name('test_name')
    assert test_min is not None

    assert await test_db.minerals.del_by_id(test_min.id)
