import pytest
import json

from os import environ
from typing import AsyncGenerator

from unittest.mock import patch
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.__main__ import app
from app.database import Base, User, DB, MineralType, Mineral, Key
from app.database.init_db import create_tables
from app.core.auth import get_hash, TokenData
from app.depends.session import get_session
from app.depends.auth import verify_token


db_path = "sqlite+aiosqlite:///foodapp_test.sqlite3"


environ['DB_PATH'] = db_path


engine = create_async_engine(
    url=db_path,
    echo=True,
    pool_pre_ping=True,
)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession]:
    async with test_session() as session:
        yield session


async def verify_test_token() -> TokenData:
    async with test_session() as session:
        user = await DB.users.by_id(1, session=session)
        return TokenData(
            user=user,
            exp=10
        )


async def verify_mock_token():
    #session = Mock(spec=get_test_session)
    with patch('app.depends.auth.verify_token') as verify_test_mock_token:
        verify_test_mock_token.return_value = await verify_test_token()
        verify_test_mock_token.side_effect = await verify_test_token()
        return verify_test_mock_token


@pytest.fixture(scope='module')
async def test_client() -> AsyncGenerator[AsyncClient]:
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[verify_token] = verify_mock_token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(scope='function')
async def test_db() -> AsyncGenerator[AsyncSession]:
    async with test_session() as session:
        yield session


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with test_session() as session:
            key = Key(id=1, hash='12345', is_admin=True)
            session.add(key)
            await session.flush()
            user = User(id=1, name='test12345', password=get_hash('123456'), is_admin=True, key=key)
            session.add(user)
            await session.flush()
            await create_tables(session)
            await session.commit()


@pytest.fixture(autouse=True)
def mock_settings():
    with patch('app.settings.settings') as mock_settings:
        mock_settings.AUTH_SECRET_KEY = "test-secret-key"
        mock_settings.AUTH_ALGORITHM = "HS256"
        mock_settings.AUTH_TOKEN_LIFETIME_IN_MIN = 30
        mock_settings.DB_PATH = db_path
        yield mock_settings
