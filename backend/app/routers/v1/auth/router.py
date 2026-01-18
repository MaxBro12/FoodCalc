import logging
from random import randint

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.requests import Request

from app.settings import settings

from .models import Token, UserLogin, UserRegister
from app.routers.misc_models import Ok
from app.depends import SessionDep, TokenDep
from app.database import DB
from app.core.auth import (
    verify_hashed,
    create_access_token,
    get_hash,
    create_refresh_token,
    verify_refresh_token
)
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

    # Передача обычного токена
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

    # Передача токена для обновления
    uni = generate_trash_string(6)
    token = create_refresh_token(data={
        "sub": user.name
    }).split('.')

    await DB.users.set_tokens(user.id, uni, '.'.join(token), session=session)

    response.set_cookie(
        key='refresh_token',
        value=token[0] + '.' + uni + token[1] + '.' + token[2],
        httponly=True,
        secure=False if settings.DEBUG else True,
        samesite='strict',
        max_age=settings.AUTH_REFRESH_LIFETIME_IN_DAYS * 24 * 60 * 60
    )
    return {'ok': True}


@auth_router_v1.post('/refresh', response_model=Ok)
async def refresh(request: Request, response: Response, session: SessionDep):
    if not request.cookies.get('refresh_token'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token not provided"
        )
    token_data = await verify_refresh_token(session, request.cookies['refresh_token'])
    uni = generate_trash_string(6)
    token = create_refresh_token(data={
        "sub": token_data.user.name
    }).split('.')
    await DB.users.set_tokens(token_data.user.id, uni, '.'.join(token), session=session)

    response.set_cookie(
        key='refresh_token',
        value=token[0] + '.' + uni + token[1] + '.' + token[2],
        httponly=True,
        secure=False if settings.DEBUG else True,
        samesite='strict',
        max_age=settings.AUTH_REFRESH_LIFETIME_IN_DAYS * 24 * 60 * 60
    )
    return {'ok': True}


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
