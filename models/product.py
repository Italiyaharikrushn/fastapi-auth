from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base_class import Base
 

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image = Column(String, nullable=True)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    seller = relationship("User", back_populates="products")
    documents = relationship("Document", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")