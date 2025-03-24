# from sqlalchemy.orm import Session
# from models import Cart, CartItem, Product
# from schemas.cart import CartItemCreate, CartItemUpdate
# from fastapi import HTTPException

# class CRUDCart:
#     def add_to_cart(self, db: Session, user_id: int, cart_item: CartItemCreate):
#         cart = db.query(Cart).filter(Cart.user_id == user_id).first()
#         if not cart:
#             cart = Cart(user_id=user_id)
#             db.add(cart)
#             db.commit()
#             db.refresh(cart)
        
#         cart_item_obj = CartItem(cart_id=cart.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
#         db.add(cart_item_obj)
#         db.commit()
#         db.refresh(cart_item_obj)
#         return self.get_cart(db, user_id)

#     def update_cart_item(self, db: Session, user_id: int, cart_item_id: int, update_data: CartItemUpdate):
#         cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.cart_id == Cart.id, Cart.user_id == user_id).first()
#         if not cart_item:
#             raise HTTPException(status_code=404, detail="Cart item not found")

#         if update_data.quantity <= 0:
#             raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

#         cart_item.quantity = update_data.quantity
#         db.commit()
#         db.refresh(cart_item)
#         return cart_item

#     def get_cart(self, db: Session, user_id: int):
#             cart = db.query(Cart).filter(Cart.user_id == user_id).first()
#             if not cart:
#                 return {"message": "Cart is empty", "cart_items": []}
            
#             cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
#             total_price = sum(
#                 db.query(Product).filter(Product.id == item.product_id).first().price * item.quantity
#                 for item in cart_items
#             )
#             return {"cart_id": cart.id, "user_id": user_id, "total_price": total_price, "cart_items": cart_items}

#     def remove_from_cart(self, db: Session, user_id: int, cart_item_id: int):
#         cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.cart_id == Cart.id, Cart.user_id == user_id).first()
#         if not cart_item:
#             raise HTTPException(status_code=404, detail="Cart item not found")

#         db.delete(cart_item)
#         db.commit()
#         return {"message": "Cart item removed successfully"}

#     def clear_cart(self, db: Session, user_id: int):
#         cart = db.query(Cart).filter(Cart.user_id == user_id).first()
#         if not cart:
#             raise HTTPException(status_code=404, detail="Cart not found")

#         db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
#         db.commit()
#         return {"message": "Cart cleared successfully"}

# crud_cart = CRUDCart()

from models.order import Order, OrderStatusEnum
from models import OrderItem, Product, BillingAddress, Cart, CartItem
from fastapi import HTTPException
from crud.base import CRUDBase
from schemas.cart import CartItemCreate, CartItemUpdate

class CRUDCart(CRUDBase[Cart, CartItemCreate, CartItemUpdate]):
    ...

cart = CRUDCart(Order)