from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    cancelled = "cancelled"

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreateSchema(BaseModel):
    customer_id: int
    shipping_address_id: int
    billing_address_id: int
    items: List[OrderItemSchema]

class OrderResponseSchema(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    total_price: float
    items: List[OrderItemSchema]

    class Config:
        orm_mode = True
