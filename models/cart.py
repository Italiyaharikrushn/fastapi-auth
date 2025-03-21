from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base_class import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="carts")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def total_items(self):
        return sum(item.quantity for item in self.cart_items)

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items)
