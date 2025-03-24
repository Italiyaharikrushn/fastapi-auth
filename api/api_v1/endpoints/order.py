from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from crud.crud_order import crud_order
from schemas.order import OrderCreate
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/checkout/")
def checkout(order_data: OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.checkout(db, user.id, order_data.billing_address_id)

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.get_order_by_id(db, order_id)
