from sqlalchemy import Column, Integer, String
from db.base_class import Base

class Client(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(250), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=True)
    gender = Column(String(8), nullable=True)
