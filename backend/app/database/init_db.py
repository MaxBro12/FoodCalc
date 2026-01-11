import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .database import engine, Base, new_session
from .repo import DB
from .models import MineralType, Mineral


async def create_tables(session: AsyncSession):
    data = None
    try:
        with open(r'data/types.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    if data is not None:
        try:
            for type in data['data']:
                if DB.mineral_types.exists_by_id(int(type['id']), session=session):
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
