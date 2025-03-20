from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.cart import CartCreate, CartResponseSchema
from crud.crud_cart import crud_cart
from db.session import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartResponseSchema)
def add_item_to_cart(cart_data: CartCreate, db: Session = Depends(get_db)):
    """Adds an item to the cart"""
    return crud_cart.add_to_cart(db, cart_data)

@router.get("/{customer_id}", response_model=CartResponseSchema)
def fetch_cart(customer_id: int, db: Session = Depends(get_db)):
    """Fetch the cart for a customer"""
    return crud_cart.get_cart(db, customer_id)

@router.delete("/{cart_item_id}")
def remove_item_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    """Remove an item from the cart"""
    return crud_cart.remove_cart_item(db, cart_item_id)
