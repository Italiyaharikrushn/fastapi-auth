from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base_class import Base
import enum

class OrderStatusEnum(str, enum.Enum):
    pending = "Pending"
    processing = "Processing"
    shipped = "Shipped"
    delivered = "Delivered"
    cancelled = "Cancelled"
    return_order = "Return"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.pending)
    total_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_total_price(self):
        self.total_price = sum(item.total_price() for item in self.order_items)
