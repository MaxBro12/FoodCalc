import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists, select, text

from app.core.security import get_hash
from app.settings import settings
from .database import engine, Base, new_session
from .models import MineralType, Mineral, Key, User


async def create_tables(session: AsyncSession):
    data = None
    try:
        with open(r'data/types.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    if data is not None:
        try:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print()
            if settings.DEBUG and await session.scalar(select(exists().where(Key.id == 1))):
                session.add(Key(id=1, hash='123', is_admin=True))
                await session.commit()
            if settings.DEBUG and await session.scalar(select(exists().where(User.id == 1))):
                session.add(User(name='123' , password=get_hash('123') , is_admin=True, key_id=1))
                await session.commit()

            for type in data['data']:
                if bool(await session.scalar(select(exists().select_from(MineralType).where(text(f"id={type['id']}"))))):
                    continue
                mineral_type = MineralType(
                    id=type['id'],
                    name=type['name'],
                    description=type['description'],
                )
                session.add(mineral_type)
                await session.flush()
                for mineral in type['minerals']:
                    mineral_to_save = Mineral(
                        id=mineral['id'],
                        name=mineral['name'],
                        compact_name=mineral['compact_name'],
                        description=mineral['description'],
                        intake=mineral['intake'],
                        type_id=type['id'],
                    )
                    session.add(mineral_to_save)
                    await session.flush()
        except IntegrityError:
            return


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with new_session() as session:
        await create_tables(session)
        await session.commit()
