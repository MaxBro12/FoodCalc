from dataclasses import dataclass
from typing import Literal


Method = Literal['GET', 'POST', 'PUT', 'DELETE']


@dataclass(frozen=True, slots=True)
class ResponseData:
    status: int
    json: dict
