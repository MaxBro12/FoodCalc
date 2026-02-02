import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists, select, text

from app.database.database import engine, Base, new_session
from app.database.models import Product, MineralType, Mineral
from app.database.repo import DataBase
from .models import MineralType, Mineral

from app.settings import settings


async def create_tables(session: AsyncSession):
    data = None
    products = None
    try:
        with open(r'data/types.json') as f:
            data = json.load(f)
        with open(r'data/products.json') as f:
            products = json.load(f)
    except FileNotFoundError:
        pass

    if data is not None and products is not None:
        try:
            for m_type in data['data']:
                if bool(await session.scalar(select(exists().select_from(MineralType).where(text(f"id={m_type['id']}"))))):
                    continue
                mineral_type = MineralType(
                    id=m_type['id'],
                    name=m_type['name'],
                    description=m_type['description'],
                )
                session.add(mineral_type)
                await session.flush()
                for mineral in m_type['minerals']:
                    mineral_to_save = Mineral(
                        id=mineral['id'],
                        name=mineral['name'],
                        compact_name=mineral['compact_name'],
                        description=mineral['description'],
                        intake=mineral['intake'],
                        type_id=m_type['id'],
                    )
                    session.add(mineral_to_save)
                    await session.flush()
            if settings.DEBUG:
                db = DataBase(session)
                await session.flush()
                for product in products['products']:
                    session.add(Product(
                        id=product['id'],
                        name=product['name'],
                        description=product['description'],
                        calories=product['calories'],
                        energy=product['energy'],
                        added_by=product['added_by'],
                    ))
                    await session.flush()

                    for mineral in product['minerals']:
                        await db.products_minerals.new(
                            product_id=product['id'],
                            mineral_id=mineral['id'],
                            content=mineral['content']
                        )
                await session.commit()

        except IntegrityError:
            return


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with new_session() as session:
        await create_tables(session)
        await session.commit()
