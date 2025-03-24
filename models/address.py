from sqlalchemy import Column, Integer, String, ForeignKey
from db.base_class import Base

class BillingAddress(Base):
    __tablename__ = "billing_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)

    billing_fullname = Column(String, nullable=False)
    billing_address = Column(String, nullable=False)
    billing_city = Column(String, nullable=False)
    billing_state = Column(String, nullable=False)
    billing_pincode = Column(String, nullable=False)
    billing_country = Column(String, nullable=False)
    billing_contact_number = Column(String, nullable=False)