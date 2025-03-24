from pydantic import BaseModel
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    subtotal: float

class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    cart_items: List[CartItemResponse]

    class Config:
        orm_mode = True

#         from pydantic import BaseModel
# from typing import List

# # Request Schema for Adding an Item to Cart
# class CartItemCreate(BaseModel):
#     product_id: int
#     quantity: int

# class CartItemUpdate(BaseModel):
#     quantity: int

# # Response Schema for Cart Item
# class CartItemResponse(BaseModel):
#     id: int
#     product_id: int
#     quantity: int

# # Response Schema for Cart
# class CartResponse(BaseModel):
#     id: int
#     user_id: int
#     total_price: float
#     cart_items: List[CartItemResponse]

#     class Config:
#         orm_mode = True
