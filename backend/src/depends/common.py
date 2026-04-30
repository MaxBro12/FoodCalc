from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from .auth import UserDep
from .db import DBDep


@dataclass(frozen=True, slots=True)
class Common:
    user: UserDep
    db: DBDep


def get_common_dep(user: UserDep, db: DBDep) -> Common:
    return Common(user=user, db=db)


CommonDep = Annotated[Common, Depends(get_common_dep)]
