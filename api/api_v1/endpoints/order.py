from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
import crud
from schemas.order import OrderCreate
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/checkout/")
def checkout(order_data: OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.order.checkout(db, user.id, order_data.billing_address_id)

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.order.get(db, order_id)

@router.put("/orders/{order_id}/accept")
async def accept_order(order_id: int, db: Session = Depends(get_db)):
    return crud.order.accept_order(db=db, order_id=order_id)