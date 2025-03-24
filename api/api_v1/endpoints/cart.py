from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.cart import CartItemCreate, CartItemResponse, CartResponse, CartItemUpdate
from crud.crud_cart import crud_cart
from api.dependencies import get_current_user
from models import CartItem, Product

router = APIRouter()

@router.post("/", response_model=CartResponse)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart = crud_cart.add_to_cart(db, user.id, cart_item)
    
    # Fetch all cart items for the given cart
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    # Calculate total price
    total_price = sum(
        db.query(Product).filter(Product.id == item.product_id).first().price * item.quantity
        for item in cart_items
    )

    return {
        "id": cart.id,
        "user_id": user.id,
        "total_price": total_price,
        "cart_items": cart_items  # Since Pydantic models are used, it will convert automatically
    }

@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, update_data: CartItemUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.update_cart_item(db, user.id, cart_item_id, update_data)

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.remove_from_cart(db, user.id, cart_item_id)

@router.delete("/")
def clear_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.clear_cart(db, user.id)
