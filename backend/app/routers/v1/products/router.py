from fastapi import APIRouter, HTTPException, status, Body

from app.depends import DBDep, PaginationParams, TokenDep
from app.routers.misc_models import Ok
from app.routers.v1.products.models import NewProduct
from app.routers.decorators import admin_access
from .models import SearchProduct, MultipleProductsResponse, ProductResponse, ProductsNames


products_router_v1 = APIRouter(prefix='/v1/products', tags=['products'])


@products_router_v1.get('/', response_model=MultipleProductsResponse)
async def products_pagination(db: DBDep, pagination: PaginationParams):
    products = await db.products.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        order_by_field='id',
        load_relations=True
    )
    return {'products': [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'minerals': [{
            'id': mineral.mineral.id,
            'name': mineral.mineral.name,
            'compact_name': mineral.mineral.compact_name,
            'type_id': mineral.mineral.type_id,
            'content': mineral.content,
        } for mineral in product.minerals],
        'calories': product.calories,
        'energy': product.energy,
        'added_by_id': product.added_by_id,
        'added_by_name': product.added_by.name
    } for product in products]}


@products_router_v1.get('/details/{product_id}', response_model=ProductResponse)
async def product_by_id(product_id: str, db: DBDep):
    product = await db.products.by_id(
        type_id=product_id,
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
            'compact_name': mineral.mineral.compact_name,
            'type_id': mineral.mineral.type_id,
            'content': mineral.content,
        } for mineral in product.minerals],
        'calories': product.calories,
        'energy': product.energy,
        'added_by_id': product.added_by_id,
        'added_by_name': product.added_by.name
    }


@products_router_v1.post('/search', response_model=ProductsNames)
async def search_products(query: SearchProduct, db: DBDep):
    return {'names': [{
        'id': i[0],
        'name': i[1],
        'search_index': i[2]
    } for i in await db.products.search(query=query.id_or_name)]}


@products_router_v1.get('/names', response_model=ProductsNames)
async def names(db: DBDep, limit: int = 500):
    return {'names': [{
        'id': i[0],
        'name': i[1],
        'search_index': i[2]
    } for i in await db.products.names(limit=limit)]}


@products_router_v1.post('/new', response_model=Ok)
async def save_new_product(new: NewProduct, db: DBDep, token: TokenDep):
    await db.products.new(
        pid=new.id,
        name=new.name,
        description=new.description,
        calories=new.calories,
        energy=new.energy,
        added_by_id=token.user.id,
        commit=False,
    )
    await db.flush()
    for i in new.minerals:
        await db.products_minerals.new(new.id, i.id, content=i.content, commit=False)
    return {'ok': True}


@admin_access
@products_router_v1.delete('/{product_id}', response_model=Ok)
async def del_product(product_id: int, db: DBDep, token: TokenDep):
    return {'ok': await db.products.del_by_id(product_id=product_id)}
