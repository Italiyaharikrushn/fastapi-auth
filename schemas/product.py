from pydantic import BaseModel

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    image: str

class ProductUpdate(BaseModel):
    title: str
    description: str
    price: float
    stock: int

class ProductResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    seller_id: int
