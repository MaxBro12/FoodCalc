from typing import Annotated

from fastapi import Depends

from app.database.session import get_session, AsyncSession


SessionDep = Annotated[AsyncSession, Depends(get_session)]
