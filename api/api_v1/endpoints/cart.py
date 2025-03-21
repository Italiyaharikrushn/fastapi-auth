from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.cart import CartItemCreate, CartResponse
from crud.crud_cart import crud_cart
from api.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartResponse)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_cart.add_to_cart(db, user["id"], cart_item)

@router.get("/", response_model=list[CartResponse])
def get_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart = crud_cart.get_cart(db, user["id"])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart.cart_items

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    success = crud_cart.remove_from_cart(db, user["id"], cart_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}
