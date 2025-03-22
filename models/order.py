from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base_class import Base
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .address import BillingAddress  # Prevents circular import

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("billing_addresses.id"), nullable=False)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.pending)
    total_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    billing_address = relationship("BillingAddress", back_populates="orders", foreign_keys=[billing_address_id])

    def calculate_total_price(self):
        self.total_price = sum(item.total_price() for item in self.order_items)
