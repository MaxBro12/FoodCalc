from fastapi import APIRouter

from app.depends import SessionDep, PaginationParams
from app.routers.misc_models import Ok
from app.database.repo import DB
from app.depends import Token
from app.routers.v1.products.models import NewProduct
from app.routers.decorators import admin_access


products_router_v1 = APIRouter(prefix='/v1/products', tags=['products'])


@products_router_v1.get('/')
async def products_pagination(session: SessionDep, pagination: PaginationParams):
    return {'products': await DB.products.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        order_by_field='id',
        session=session,
        load_relations=True
    )}


@products_router_v1.get('/{mineral_id}')
async def product_by_id(mineral_id: int, session: SessionDep):
    return {'mineral': await DB.products.by_id(
        type_id=mineral_id,
        session=session,
        load_relations=True
    )}


@products_router_v1.post('/new', response_model=Ok)
async def save_new_product(new: NewProduct, session: SessionDep, token: Token):
    await DB.products.new(
        id=new.id,
        name=new.name,
        description=new.description,
        added_by_id=token.user.id,
        session=session,
        commit=False,
    )
    await session.flush()
    for i in new.minerals:
        await DB.products_minerals.new(new.id, i.id, content=i.content, session=session, commit=False)
    await session.commit()
    return {'ok': True}


@admin_access
@products_router_v1.delete('/{product_id}', response_model=Ok)
async def del_product(product_id: int, session: SessionDep, token: Token):
    return {'ok': await DB.products.del_by_id(product_id=product_id, session=session)}
