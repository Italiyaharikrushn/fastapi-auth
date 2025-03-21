from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
