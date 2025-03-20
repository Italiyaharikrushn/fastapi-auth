from pydantic import BaseModel

class ShippingAddressCreate(BaseModel):
    customer_id: int
    address: str
    city: str
    state: str
    postal_code: str
    country: str

class ShippingAddressUpdate(BaseModel):
    address: str
    city: str
    state: str
    postal_code: str
    country: str

class ShippingAddressOut(BaseModel):
    id: int
    customer_id: int
    address: str
    city: str
    state: str
    postal_code: str
    country: str

    class Config:
        orm_mode = True
