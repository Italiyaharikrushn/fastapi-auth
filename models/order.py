from sqlalchemy import Column, Integer, ForeignKey, String, Float, Enum
from sqlalchemy.orm import relationship
from db.base_class import Base
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    READY_TO_SHIP = "ready_to_ship"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("shipping_addresses.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("billing_addresses.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_price = Column(Float, nullable=False)

    customer = relationship("User", back_populates="orders")
    shipping_address = relationship("ShippingAddress")
    billing_address = relationship("BillingAddress")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
