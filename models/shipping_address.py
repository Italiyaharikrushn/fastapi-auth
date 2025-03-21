from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base_class import Base

class ShippingAddress(Base):
    __tablename__ = "shipping_addresses"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)  # Only for sellers
    business_name = Column(String(255), nullable=False)
    business_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    pincode = Column(String(6), nullable=False)
    country = Column(String(100), nullable=False)

    # Relationships
    seller = relationship("User", back_populates="shipping_addresses")

    def __repr__(self):
        return f"<ShippingAddress {self.business_name}, {self.city}>"
