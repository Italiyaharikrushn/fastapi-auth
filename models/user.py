from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, DateTime
from db.base_class import Base
from datetime import datetime, timedelta

from core.enums import RoleEnum

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    expiry_date = Column(DateTime, nullable=True, default=lambda: datetime.utcnow() + timedelta(days=365))  # ✅ Fix: Set default expiry date

# class RoleEnum(str, enum.Enum):  
#     SELLER = "SELLER"
#     ADMIN = "ADMIN"
#     CUSTOMER = "CUSTOMER"

# class User(Base):
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(32), nullable=False)
#     last_name = Column(String(32), nullable=False)
#     password = Column(String(), nullable=False)
#     email = Column(String(256), unique=True, nullable=False)
#     phone = Column(String(15), nullable=True)
#     gender = Column(String(15), nullable=True)
#     created_by = Column(Integer, nullable=True)
#     is_super_admin = Column(Boolean, nullable=False, default=False)
#     modified_by = Column(Integer, nullable=True)
#     expiry_date = Column(DateTime(timezone=True), nullable=False)
    
#     role = Column(Enum(RoleEnum), nullable=False)