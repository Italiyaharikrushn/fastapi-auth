from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.cart import CartItemCreate, CartItemUpdate
import crud
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/")
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.cart.create(db, user.id, cart_item)

@router.get("/")
def get_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.cart.get(db, user.id)

@router.put("/{cart_item_id}")
def update_cart_item(cart_item_id: int, update_data: CartItemUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.cart.update(db, user.id, cart_item_id, update_data)

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.cart.remove(db, user.id, cart_item_id)

@router.delete("/")
def clear_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.cart.remove(db, user.id)
