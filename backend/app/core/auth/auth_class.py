from time import time
from datetime import datetime, timedelta

from fastapi import Request, Response, HTTPException, status
from jose import JWTError, jwt

from app.database.repo import DataBase
from app.database.models import User
from app.core.debug import logger
from app.core.spec_time import get_current_time

from .data_classes import TokenData

from app.settings import settings


class AuthService:
    def __init__(self, db: DataBase) -> None:
        self.__db = db

    def __encode_token(self, data: dict) -> str:
        return jwt.encode(
            claims=data,
            key=settings.AUTH_SECRET_KEY,
            algorithm=settings.AUTH_ALGORITHM
        )

    def __decode_token(self, token: str) -> dict:
        return jwt.decode(
            token=token,
            key=settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )

    def __hash_token(self, token: str) -> str:
        # Кажется что тут ничего нет, но не продакшене
        return token

    def __unhash_token(self, token: str) -> str:
        # Кажется что тут ничего нет, но не продакшене
        return token

    async def __base_token_checks(self, request: Request, cookie_key: str) -> tuple[User, dict, str]:
        try:
            if request.cookies.get(cookie_key) is None:
                logger.log(f'verify_{cookie_key} > no token', 'info')
                raise JWTError

            token = self.__unhash_token(request.cookies[cookie_key])
            data = self.__decode_token(token)
            if data['exp'] < time():
                logger.log(f'verify_{cookie_key} > expired for {data['sub']}', 'info')
                raise JWTError

            user = await self.__db.users.by_name(data['sub'])
            if user is None or not user.is_active:
                logger.log(
                    f'verify_{cookie_key} > user not found or inactive for {data['sub']}',
                    'info'
                )
                raise JWTError
            return user, data, token
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def verify_access_token(self, request: Request) -> TokenData:
        user, data, token = await self.__base_token_checks(request, 'access_token')
        user.last_active = datetime.now()
        return TokenData(user=user, exp=data['exp'])

    async def verify_refresh_token(self, request: Request) -> TokenData:
        user, data, token = await self.__base_token_checks(request, 'refresh_token')

        if not await self.__db.users.verify_token(
            user_id=user.id,
            refresh_token=token
        ):
            logger.log(f'verify_refresh_token > {data['sub']} token not verified', 'info')
            raise JWTError

        return TokenData(user=user, exp=data['exp'])

    async def create_tokens(self, user: User, response: Response, adt_data: dict | None = None) -> Response:
        data = {
            'sub': user.name,
            'exp': time() + settings.AUTH_TOKEN_LIFETIME_IN_MIN * 60#(get_current_time() + timedelta(minutes=settings.AUTH_TOKEN_LIFETIME_IN_MIN)).isoformat()
        }
        response.set_cookie(
            key='access_token',
            value=self.__hash_token(self.__encode_token(data)),
            httponly=False if settings.DEBUG else True,
            secure=False if settings.DEBUG else True,
            samesite='lax',
            #max_age=settings.AUTH_TOKEN_LIFETIME_IN_MIN * 60
        )

        data['exp'] = time() + settings.AUTH_REFRESH_LIFETIME_IN_DAYS * 24 * 60 * 60#(get_current_time() + timedelta(days=settings.AUTH_REFRESH_LIFETIME_IN_DAYS)).isoformat()
        refresh_token = self.__encode_token(data)
        response.set_cookie(
            key='refresh_token',
            value=self.__hash_token(refresh_token),
            httponly=False if settings.DEBUG else True,
            secure=False if settings.DEBUG else True,
            samesite='lax',
            #max_age=settings.AUTH_REFRESH_LIFETIME_IN_DAYS * 24 * 60 * 60
        )
        return response

    async def refresh(self, request: Request, response: Response) -> Response:
        old_token_data = await self.verify_refresh_token(request)
        await self.create_tokens(user=old_token_data.user, response=response)
        return response

    async def logout(self, user_id: int,response: Response) -> Response:
        await self.__db.users.clear_token(user_id)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
