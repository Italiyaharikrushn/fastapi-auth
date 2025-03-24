from pydantic import BaseModel
from typing import List, Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemDetails(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    product_price: float

class Cart(BaseModel):
    id: int
    user_id: int
    total_price: float
    cart_items: List[CartItemDetails] = []

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
