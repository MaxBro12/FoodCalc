from core.simplejwt import SimpleJWT
from core.trash import generate_trash_string
from app.database.models import User
from app.routers.v1.auth.models import TokenFull

from app.settings import settings


class AuthHandler:
    jwt = SimpleJWT(settings.AUTH_SECRET_KEY, settings.AUTH_ALGORITHM)

    def create_tokens(self, user: User):
        uni = generate_trash_string(6)
        user.unique = uni
        return TokenFull(
            access_token=self.jwt.create_token({
                'uid': user.name,
                'usp': user.id,
            }, expire_delta=settings.AUTH_ACCESS_EXPIRE),
            refresh_token=self.jwt.create_token({
                'uid': user.name,
                'usp': user.id,
                'uni': user.unique
            }, expire_delta=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60)
        )

    def verify_refresh_token(self, token: str):
        return self.jwt.verify_token(
            token=token,
            valid_time=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60
        )

auth_handler = AuthHandler()
