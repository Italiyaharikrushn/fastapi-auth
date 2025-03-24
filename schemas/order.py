from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Enum for order status
class OrderStatusEnum(str, Enum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return"

# Schema for creating an order
class OrderCreate(BaseModel):
    billing_address_id: int
    items: List[int]  # You can replace this with the actual order item schema

# Schema for updating an order
class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    billing_address_id: Optional[int] = None

# Schema for order response
class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_price: float
    order_items: List[int]  # You can replace this with the actual order item response

    class Config:
        orm_mode = True
