from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return"

class OrderCreate(BaseModel):
    billing_address_id: int
    items: List[int]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    billing_address_id: Optional[int] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_price: float
    order_items: List[int]

    class Config:
        orm_mode = True
