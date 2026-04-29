from .auth import auth_router_v1
from .minerals import minerals_router_v1
from .products import products_router_v1
from .utils import utils_router_v1


__all__ = (
    'auth_router_v1',
    'minerals_router_v1',
    'products_router_v1',
    'utils_router_v1',
)
