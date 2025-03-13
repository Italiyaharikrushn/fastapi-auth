from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, DateTime
from db.base_class import Base
from datetime import datetime, timedelta

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
    expiry_date = Column(DateTime, nullable=True, default=lambda: datetime.utcnow() + timedelta(days=365))
