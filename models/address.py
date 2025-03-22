from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base_class import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order  # Prevents circular import

class BillingAddress(Base):
    __tablename__ = "billing_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, unique=True)

    billing_fullname = Column(String, nullable=False)
    billing_address = Column(String, nullable=False)
    billing_city = Column(String, nullable=False)
    billing_state = Column(String, nullable=False)
    billing_pincode = Column(String, nullable=False)
    billing_country = Column(String, nullable=False)
    billing_contact_number = Column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="billing_address", uselist=False)
    orders = relationship("Order", back_populates="billing_address", foreign_keys="[Order.billing_address_id]")

    def __str__(self):
        return f"Billing Address for {self.billing_fullname}"