from typing import Annotated

from fastapi import Depends

from app.core.auth import verify_access_token, TokenData


TokenDep = Annotated[TokenData, Depends(verify_access_token)]
