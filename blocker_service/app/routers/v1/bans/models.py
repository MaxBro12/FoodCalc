from typing import Tuple, List
from datetime import datetime
from pydantic import BaseModel


class Ok(BaseModel):
    ok: bool = False


class Ban(BaseModel):
    ip: str
    reason: str
    date: datetime


class Bans(BaseModel):
    bans: Tuple[Ban] | List[Ban]


class NewBan(BaseModel):
    ip: str
    reason: str = 'no reason'
