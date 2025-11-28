from app.core.single import Singleton
from .key import KeyRepo
from .user import UserRepo
from .mineral_type import MineralTypeRepo
from .mineral import MineralRepo


class DB(Singleton):
    keys = KeyRepo()
    users = UserRepo()

    mineral_types = MineralTypeRepo()
    minerals = MineralRepo()


__all__ = (
    'DB',
)
