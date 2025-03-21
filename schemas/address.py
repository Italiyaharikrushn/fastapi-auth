from pydantic import BaseModel

# **Shipping Address Schemas**
class ShippingAddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class ShippingAddressUpdate(ShippingAddressCreate):
    pass

class ShippingAddressResponse(ShippingAddressCreate):
    id: int

    class Config:
        orm_mode = True

# **Billing Address Schemas**
class BillingAddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class BillingAddressUpdate(BillingAddressCreate):
    pass

class BillingAddressResponse(BillingAddressCreate):
    id: int

    class Config:
        orm_mode = True
