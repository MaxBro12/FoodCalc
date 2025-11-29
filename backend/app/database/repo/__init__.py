from app.core.single import Singleton
from .key import KeyRepo
from .user import UserRepo
from .mineral_type import MineralTypeRepo
from .mineral import MineralRepo
from .product import ProductRepo
from .product_mineral import ProductMineralRepo


class DB(Singleton):
    keys = KeyRepo()
    users = UserRepo()

    mineral_types = MineralTypeRepo()
    minerals = MineralRepo()

    products = ProductRepo()
    products_minerals = ProductMineralRepo()


__all__ = (
    'DB',
)
