from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Numeric
from datetime import datetime
from db.base_class import Base
from typing import TYPE_CHECKING
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .address import BillingAddress
class OrderStatusEnum(str, PyEnum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return_order"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("billing_addresses.id"), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)