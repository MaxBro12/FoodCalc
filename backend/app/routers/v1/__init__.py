from .auth import auth_router_v1
from .minerals import mineral_router_v1
from .products import products_router_v1

__all__ = (
    'auth_router_v1',
    'mineral_router_v1',
    'products_router_v1',
)