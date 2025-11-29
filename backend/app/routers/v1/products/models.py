from pydantic import BaseModel


class MineralInProduct(BaseModel):
    id: int
    content: float


class NewProduct(BaseModel):
    id: int
    name: str
    description: str
    minerals: list[MineralInProduct]
