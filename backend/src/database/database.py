from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DB_PATH,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)
