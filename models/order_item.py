from sqlalchemy import Column, Integer, ForeignKey, Enum, Date
from datetime import date
from db.base_class import Base
import enum

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"
    return_order = "return"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.pending)
    order_date = Column(Date, default=date.today)
    dispatch_date = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)

    def total_price(self):
        return self.quantity * self.product.price
