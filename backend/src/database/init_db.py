import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists, select, text

from src.database.database import engine, Base, new_session
from src.database.models import Product, MineralType, Mineral
from src.database.repo import DataBase
from .models import MineralType, Mineral

from src.settings import settings


async def create_tables(session: AsyncSession):
    minerals = None
    products = None
    try:
        with open(r'data/types.json') as f:
            minerals = json.load(f)
        with open(r'data/new_products.json') as f:
            products = json.load(f)
    except FileNotFoundError:
        pass

    if minerals is not None:
        try:
            for m_type in minerals['data']:
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
                        daily_value=mineral['intake'],
                        type_id=m_type['id'],
                    )
                    session.add(mineral_to_save)
                    await session.flush()
        except IntegrityError:
            return
    await session.flush()
    if products is not None:
        try:
            for product in products['products']:
                if bool(await session.scalar(select(exists().select_from(Product).where(text(f"id={product['id']}"))))):
                    continue
                product_to_save = Product(
                    id=product['id'],
                    name=product['name'],
                    description=product['description'],
                    calories_per_100g=product['calories_per_100g'],
                    proteins_per_100g=product['proteins_per_100g'],
                    fats_per_100g=product['fats_per_100g'],
                    carbs_per_100g=product['carbs_per_100g'],
                    fiber_per_100g=product['fiber_per_100g'],
                    sugar_per_100g=product['sugar_per_100g'],
                    added_by=1,
                    is_verified=True,
                )
                session.add(product_to_save)
                await session.flush()
        except IntegrityError:
            return
    await session.commit()


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with new_session() as session:
        await create_tables(session)
