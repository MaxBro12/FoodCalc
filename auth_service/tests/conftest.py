import pytest
from typing import AsyncGenerator

from fastapi import Request, Response
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database.repo import DataBase
from app.database.models import User, Key
from app.database import Base
from app.depends.db import get_db
from core.redis_client import get_redis
from app.__main__ import app



engine = create_async_engine(
    url="sqlite+aiosqlite:///:memory:",
    echo=True,
    pool_pre_ping=True,
)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_db() -> AsyncGenerator[DataBase]:
    async with test_session() as session:
        yield DataBase(session)
        await session.commit()


@pytest.fixture(scope='function')
async def test_db() -> AsyncGenerator[DataBase]:
    async with test_session() as session:
        yield DataBase(session)


async def test_redis_client(request: Request):
    class RedisClientMock:
        def __init__(self, *args, **kwargs):
            pass

        async def get(self, *args, **kwargs):
            return None

        async def set(self, *args, **kwargs):
            pass

        async def get_dict(self, *args, **kwargs):
            return {}

        async def set_dict(self, *args, **kwargs):
            pass

        async def delete(self, *args, **kwargs):
            pass

        async def set_json(self, *args, **kwargs):
            pass

        async def get_json(self, *args, **kwargs):
            pass
    yield RedisClientMock()


@pytest.fixture(scope='module')
async def test_client() -> AsyncGenerator[AsyncClient]:
    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_redis] = test_redis_client

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        app.dependency_overrides.clear()



@pytest.fixture(scope='session', autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with test_session() as session:
            session.add_all([
                Key(id=1, hash='123', app_name='test_app'),
                Key(id=2, hash='456', app_name='another_test_app'),
            ])
            await session.commit()

            db = DataBase(session=session)
            await db.users.new(
                username='test_user',
                password='test_password',
                is_admin=True,
                key_id=1
            )
            await db.users.new(
                username='test_deactive_user',
                password='test_deactive_password',
                is_admin=True,
                is_active=False,
                key_id=1
            )
            await session.commit()
