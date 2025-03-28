from sqlalchemy import Column, Integer, String, ForeignKey, Float
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
