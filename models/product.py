from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric
from db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(String, nullable=True)
    stock = Column(Integer, nullable=False, default=0)
