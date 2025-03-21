from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base


class User(Base):
     __tablename__ = "user"
 
     id = Column(Integer, primary_key=True, index=True)
     first_name = Column(String(32), nullable=False)
     last_name = Column(String(32), nullable=False)
     password = Column(String, nullable=False)
     email = Column(String(256), unique=True, nullable=False)
     phone = Column(String(15), nullable=True)
     gender = Column(String(15), nullable=True)
     role = Column(String(32), nullable=False, default="seller")  # Default role seller
     expiry_date = Column(DateTime(timezone=True), nullable=False)
     is_super_admin = Column(Boolean, nullable=False, default=False)
 
     # Seller can have multiple products
     products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
