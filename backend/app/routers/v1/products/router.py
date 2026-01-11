from fastapi import APIRouter, HTTPException, status, Body

from app.depends import SessionDep, PaginationParams, TokenDep
from app.routers.misc_models import Ok
from app.database.repo import DB
from app.routers.v1.products.models import NewProduct
from app.routers.decorators import admin_access
from .models import SearchProduct, MultipleProductsResponse, ProductResponse


products_router_v1 = APIRouter(prefix='/v1/products', tags=['products'])


@products_router_v1.get('/', response_model=MultipleProductsResponse)
async def products_pagination(session: SessionDep, pagination: PaginationParams):
    products = await DB.products.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        order_by_field='id',
        session=session,
        load_relations=True
    )
    return {'products': [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'minerals': [{
            'id': mineral.mineral.id,
            'name': mineral.mineral.name,
            'type_id': mineral.mineral.type_id,
            'content': mineral.content,
        } for mineral in product.minerals],
        'calories': product.calories,
        'energy': product.energy,
        'added_by_id': product.added_by_id,
        'added_by_name': product.added_by.name
    } for product in products]}


@products_router_v1.get('/{product_id}', response_model=ProductResponse)
async def product_by_id(product_id: int, session: SessionDep):
    product = await DB.products.by_id(
        type_id=product_id,
        session=session,
        load_relations=True
    )
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Продукт с данным кодом не найден')
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'minerals': [{
            'id': mineral.mineral.id,
            'name': mineral.mineral.name,
            'type_id': mineral.mineral.type_id,
            'content': mineral.content,
        } for mineral in product.minerals],
        'calories': product.calories,
        'energy': product.energy,
        'added_by_id': product.added_by_id,
        'added_by_name': product.added_by.name
    }


@products_router_v1.post('/search', response_model=ProductResponse)
async def search_products(query: SearchProduct, session: SessionDep):
    try:
        product = await DB.products.by_id(
            type_id=int(query.id_or_name),
            session=session,
            load_relations=True
        )
    except ValueError:
        product = await DB.products.by_name(
            name=query.id_or_name,
            session=session,
            load_relations=True
        )
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Продукт по запросу {query.id_or_name} не найден')
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'minerals': [{
            'id': mineral.mineral.id,
            'name': mineral.mineral.name,
            'type_id': mineral.mineral.type_id,
            'content': mineral.content,
        } for mineral in product.minerals],
        'calories': product.calories,
        'energy': product.energy,
        'added_by_id': product.added_by_id,
        'added_by_name': product.added_by.name
    }

@products_router_v1.post('/names', response_model=Ok)
async def names(session: SessionDep, limit: int = Body(embed=True, default=500)):
    return {'names': await DB.products.names(limit=limit, session=session)}


@products_router_v1.post('/new', response_model=Ok)
async def save_new_product(new: NewProduct, session: SessionDep, token: TokenDep):
    await DB.products.new(
        pid=new.id,
        name=new.name,
        description=new.description,
        calories=new.calories,
        energy=new.energy,
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
async def del_product(product_id: int, session: SessionDep, token: TokenDep):
    return {'ok': await DB.products.del_by_id(product_id=product_id, session=session)}
