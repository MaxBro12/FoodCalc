import pytest
from typing import AsyncGenerator

from app.database.repo import DataBase
from app.database.models import User, Key
from app.database import Base

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(
    url='sqlite+aiosqlite:///:memory:',
    pool_pre_ping=True,
    echo=True
)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession]:
    async with test_session() as session:
        yield session


@pytest.fixture(scope='function')
async def test_db() -> AsyncGenerator[DataBase]:
    async with test_session() as session:
        yield DataBase(session=session)



@pytest.fixture(scope='session', autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with test_session() as session:
            session.add_all([
                Key(id=1, hash='123'),
                Key(id=2, hash='456'),
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
                key_id=1
            )
            await session.commit()
