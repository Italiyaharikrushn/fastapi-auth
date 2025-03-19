from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock: int
    image: Optional[str] = None 

class ProductCreate(ProductBase):
    seller_id: int

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True
