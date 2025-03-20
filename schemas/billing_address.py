from pydantic import BaseModel

class BillingAddressCreate(BaseModel):
    customer_id: int
    address: str
    city: str
    state: str
    postal_code: str
    country: str

class BillingAddressUpdate(BaseModel):
    address: str
    city: str
    state: str
    postal_code: str
    country: str

class BillingAddressOut(BaseModel):
    id: int
    customer_id: int
    address: str
    city: str
    state: str
    postal_code: str
    country: str

    class Config:
        orm_mode = True
