from typing import TypeVar
from app.database.database import Base
from app.database.session import new_session


T = TypeVar('T', bound=Base)
