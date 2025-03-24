from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.cart import CartItemCreate, CartItemUpdate
from crud.crud_cart import crud_cart
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/")
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.add_to_cart(db, user.id, cart_item)

@router.get("/")
def get_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.get_cart(db, user.id)

@router.put("/{cart_item_id}")
def update_cart_item(cart_item_id: int, update_data: CartItemUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.update_cart_item(db, user.id, cart_item_id, update_data)

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.remove_from_cart(db, user.id, cart_item_id)

@router.delete("/")
def clear_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.clear_cart(db, user.id)
