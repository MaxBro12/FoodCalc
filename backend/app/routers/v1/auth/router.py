import logging
from random import randint

from fastapi import APIRouter, HTTPException, status, Response

from app.settings import settings

from .models import Token, UserLogin, UserRegister
from app.routers.misc_models import Ok
from app.depends import SessionDep
from app.database import DB
from app.core.auth import verify_hashed, create_access_token, get_hash
from app.core.trash import generate_trash_string


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Ok)
async def login(response: Response, user_data: UserLogin, session: SessionDep):
    user = await DB.users.by_name(user_data.username, session)
    if not user or not verify_hashed(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Некорректное имя пользователя или пароль",
        )

    response.set_cookie(
        key='access_token',
        value=create_access_token(data={
            "sub": user.name,
            generate_trash_string(randint(3, 6)): generate_trash_string(randint(5, 10))
        }),
        httponly=True,
        secure=False if settings.DEBUG else True,
        samesite='strict',
        max_age=settings.AUTH_TOKEN_LIFETIME_IN_MIN * 60
    )
    return {'ok': True}
    #return {
    #    "access_token": create_access_token(data={
    #        "sub": user.name,
    #        generate_trash_string(randint(3, 6)): generate_trash_string(randint(5, 10))
    #    }),
    #    "token_type": "Bearer"
    #}


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserRegister, session: SessionDep):
    logging.info(f'register > {user_data.username} - {user_data.key}')
    if len(user_data.username) < 6 or len(user_data.password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Логин или пароль должны быть больше 6")
    if await DB.users.exists(user_data.username, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя уже существует")
    if not await DB.keys.exists(user_data.key, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ввели неправильный ключ")

    key = await DB.keys.by_hash(user_data.key, session)
    if key is None or not await DB.users.new(
        username=user_data.username,
        password=get_hash(user_data.password),
        is_admin=key.is_admin,
        key_id=key.id,
        session=session
    ):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка приложения, свяжитесь с администрацией")
    return {'ok': True}
