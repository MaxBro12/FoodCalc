from app.core.single import Singleton
from .key import KeyRepo
from .user import UserRepo


class DB(Singleton):
    keys = KeyRepo()
    users = UserRepo()


__all__ = (
    'DB',
)
