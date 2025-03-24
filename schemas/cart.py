from pydantic import BaseModel
from typing import List, Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class CartItemUpdate(BaseModel):
    quantity: int

    class Config:
        orm_mode = True

class CartItemDetails(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    product_price: float

    class Config:
        orm_mode = True

class Cart(BaseModel):
    id: int
    user_id: int
    total_price: float
    cart_items: List[CartItemDetails] = []

    class Config:
        orm_mode = True

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[CartItemResponse]

    class Config:
        orm_mode = True
