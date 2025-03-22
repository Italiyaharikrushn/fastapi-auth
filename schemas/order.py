from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class OrderStatusEnum(str, Enum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return"

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    billing_address_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatusEnum

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: OrderStatusEnum

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_price: float
    order_items: List[OrderItemResponse]

    class Config:
        orm_mode = True
