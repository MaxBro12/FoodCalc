from dataclasses import dataclass

from app.database.models import User


@dataclass(frozen=True, slots=True)
class TokenData:
    user: User
    exp: int
