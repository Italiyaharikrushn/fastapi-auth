from pydantic import BaseModel
from typing import Optional

class BillingAddressCreate(BaseModel):
    billing_fullname: str
    billing_address: str
    billing_city: str
    billing_state: Optional[str] = None
    billing_pincode: str
    billing_country: str
    billing_contact_number: str

class BillingAddressUpdate(BaseModel):
    billing_fullname: Optional[str] = None
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_pincode: Optional[str] = None
    billing_country: Optional[str] = None
    billing_contact_number: Optional[str] = None

class BillingAddressResponse(BillingAddressCreate):
    id: int
    user_id: int
