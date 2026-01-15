from pydantic import BaseModel


class MineralInProduct(BaseModel):
    id: int
    content: float


class NewProduct(BaseModel):
    id: str
    name: str
    description: str
    minerals: list[MineralInProduct]
    calories: int
    energy: int


class SearchProduct(BaseModel):
    id_or_name: str


class ProductName(BaseModel):
    id: str
    name: str
    search_index: float


class ProductsNames(BaseModel):
    names: list[ProductName]


class MineralInProductResponse(MineralInProduct):
    name: str
    compact_name: str
    type_id: int


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    minerals: list[MineralInProductResponse]
    calories: int
    energy: int
    added_by_id: int
    added_by_name: str


class MultipleProductsResponse(BaseModel):
    products: list[ProductResponse]
