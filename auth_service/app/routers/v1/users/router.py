from fastapi import APIRouter, HTTPException, status
from app.depends import DBDep
from core.pydantic_misc_models import Ok
from core.redis_client import RedisDep
from core.fast_decorators import cache, rate_limiter
from core.fast_depends import PaginationParams
from .models import UserResponse, UsersMultipleResponse


users_router_v1 = APIRouter(prefix='/v1/users', tags=['users'])


@users_router_v1.get('', response_model=UsersMultipleResponse)
@rate_limiter(max_requests=10, time_delta=30)
@cache(key='get_users')
async def get_users(db: DBDep, redis: RedisDep, pagination_params: PaginationParams):
    """Получение списка пользователей, если есть параметры пагинации тогда ответ с пагинацией"""
    if pagination_params.skip is not None and pagination_params.limit is not None:
        return {'users': await db.users.pagination(skip=pagination_params.skip, limit=pagination_params.limit)}
    return {'users': await db.users.all()}


@users_router_v1.get('/{user_id}', response_model=UserResponse)
@rate_limiter(max_requests=10, time_delta=30)
@cache(key='get_user')
async def get_user(user_id: int, db: DBDep, redis: RedisDep):
    """Получение пользователя по id"""
    user = await db.users.by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


@users_router_v1.post('/deactive/{user_id}')
async def deactive_user(user_id: int, db: DBDep):
    """Деактивация пользователя он не сможет авторизоваться"""
    return {'ok': await db.users.deactivate(user_id)}


@users_router_v1.post('/active/{user_id}')
async def active_user(user_id: int, db: DBDep):
    """Активация пользователя он сможет авторизоваться"""
    return {'ok': await db.users.activate(user_id)}
