import pytest
from typing import AsyncGenerator

from fastapi import Request, Response
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.__main__ import app
from app.database import Base, DataBase
from app.database.init_db import create_tables
from app.depends.db import get_db
from app.depends.auth import verify_access_token
from app.handlers.auth import User
from core.redis_client import get_redis


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


async def verify_mock_token():
    #session = Mock(spec=get_test_session)
    #with patch('app.depends.auth.verify_token') as verify_test_mock_token:
    #    verify_test_mock_token.return_value = await verify_test_token()
    #    verify_test_mock_token.side_effect = await verify_test_token()
    #    return verify_test_mock_token
    return User(id=1, name='TestUser')


@pytest.fixture(scope='module')
async def test_client() -> AsyncGenerator[AsyncClient]:
    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_redis] = test_redis_client
    app.dependency_overrides[verify_access_token] = verify_mock_token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await create_tables()
