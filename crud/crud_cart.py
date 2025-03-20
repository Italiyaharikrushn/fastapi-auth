from sqlalchemy.orm import Session
from models.cart import Cart, CartItem

class CRUDCart:
    def get_cart(self, db: Session, cart_id: int):
        return db.query(Cart).filter(Cart.id == cart_id).first()

    def create_cart(self, db: Session, cart_data):
        db_cart = Cart(**cart_data)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart

    def add_to_cart(self, db: Session, cart_id: int, product_id: int, quantity: int, price: float):
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity, price=price)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

crud_cart = CRUDCart()
