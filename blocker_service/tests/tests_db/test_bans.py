import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo import DataBase


@pytest.mark.asyncio
async def test_add(test_db: DataBase):
    await test_db.bans.clear_table()
    await test_db.bans.new('123.4.5.6', 'test', True)
    assert await test_db.bans.exists('123.4.5.6') == True
    res = await test_db.bans.by_ip('123.4.5.6')
    assert res is not None
    assert res.reason == 'test'


@pytest.mark.asyncio
async def test_add_wrong_ip(test_db: DataBase):
    await test_db.bans.new('123.4.5', 'test', False)
    await test_db.flush()
    assert await test_db.bans.exists('123.4.5') == False
    await test_db.rollback()


@pytest.mark.asyncio
async def test_auto_reason(test_db: DataBase):
    await test_db.bans.clear_table()
    await test_db.bans.new('123.4.5.6', commit=False)
    await test_db.flush()
    assert await test_db.bans.exists('123.4.5.6') == True
    res = await test_db.bans.by_ip('123.4.5.6')
    assert res is not None
    assert res.reason == 'no reason'
    await test_db.rollback()


@pytest.mark.asyncio
async def test_delete(test_db: DataBase):
    await test_db.bans.clear_table()
    await test_db.bans.new('123.4.5.6', 'test', False)
    await test_db.flush()
    assert await test_db.bans.exists('123.4.5.6') == True

    assert await test_db.bans.delete_by_ip('123.4.5.6', False) == True
    await test_db.flush()
    assert await test_db.bans.exists('123.4.5.6') == False
