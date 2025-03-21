from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base_class import Base

class BillingAddress(Base):
    __tablename__ = "billing_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, unique=True)

    billing_fullname = Column(String(255), nullable=False)
    billing_address = Column(Text, nullable=False)
    billing_city = Column(String(100), nullable=False)
    billing_state = Column(String(100), nullable=True)
    billing_pincode = Column(String(6), nullable=False)
    billing_country = Column(String(100), nullable=False)
    billing_contact_number = Column(String(14), nullable=False)

    shipping_fullname = Column(String(255), nullable=False)
    shipping_address = Column(Text, nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100), nullable=True)
    shipping_pincode = Column(String(6), nullable=False)
    shipping_country = Column(String(100), nullable=False)
    shipping_contact_number = Column(String(14), nullable=False)

    # Relationships
    user = relationship("User", back_populates="billing_address", uselist=False)
    order = relationship("Order", back_populates="billing_address", uselist=False)

    def __str__(self):
        return f"Billing Address for {self.billing_fullname}"
