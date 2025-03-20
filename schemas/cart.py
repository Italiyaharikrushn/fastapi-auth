from pydantic import BaseModel
from typing import List, Optional

class CartCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    price: float

class CartResponseSchema(BaseModel):
    cart_id: int
    customer_id: int
    items: List[dict]
