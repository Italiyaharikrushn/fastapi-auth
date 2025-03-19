from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    ffile_name = Column(String(255), nullable=False)  # Store UUID file name
    static_file_path = Column(String(255), nullable=False)  # Store file path

    product = relationship("Product", back_populates="document")
