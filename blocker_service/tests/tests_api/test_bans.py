import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repo import DataBase


@pytest.mark.asyncio
async def test_post(test_client: AsyncClient):
    res = await test_client.post('v1/bans', json={'ip': '123.4.5.6', 'reason': 'test'})
    assert res.json()['ok'] == True


@pytest.mark.asyncio
async def test_post_wrong(test_client: AsyncClient):
    res = await test_client.post('v1/bans', json={'ip': '123'})
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_in(test_client: AsyncClient, test_db: DataBase):
    await test_db.bans.new(ip_address='123.4.5.6', reason='test', commit=True)
    res = await test_client.get('v1/bans/123.4.5.6')
    assert res.json()['ok'] == True
    await test_db.bans.delete_by_ip('123.4.5.6', commit=True)


@pytest.mark.asyncio
async def test_in_wrong(test_client: AsyncClient):
    res = await test_client.get('v1/bans/123')
    assert res.status_code == 400
    assert res.json()['detail'] == 'Invalid IP address'


@pytest.mark.asyncio
async def test_delete(test_client: AsyncClient, test_db: DataBase):
    await test_db.bans.new(ip_address='123.4.5.6', reason='test', commit=True)
    res = await test_client.delete('v1/bans/123.4.5.6')
    assert res.json()['ok'] == True
