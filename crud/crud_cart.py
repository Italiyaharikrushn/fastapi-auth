from sqlalchemy.orm import Session
from models import Cart, CartItem
from schemas.cart import CartItemCreate

class CRUDCart:
    def add_to_cart(self, db: Session, user_id: int, cart_item: CartItemCreate):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        cart_item_obj = CartItem(cart_id=cart.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.add(cart_item_obj)
        db.commit()
        db.refresh(cart_item_obj)
        return cart_item_obj
    
    def get_cart(self, db: Session, user_id: int):
        return db.query(Cart).filter(Cart.user_id == user_id).first()
    
    def remove_from_cart(self, db: Session, user_id: int, cart_item_id: int):
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.cart.user_id == user_id).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return True
        return False

crud_cart = CRUDCart()
