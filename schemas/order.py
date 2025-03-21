from pydantic import BaseModel
from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    user_id: int  # Required to link order to a user

class OrderUpdate(BaseModel):
    status: OrderStatusEnum  # Update order status

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models
