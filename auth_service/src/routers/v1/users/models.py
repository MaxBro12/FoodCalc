from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    is_admin: bool
    last_active: datetime
    key_id: int


class UsersMultipleResponse(BaseModel):
    users: list[UserResponse]
