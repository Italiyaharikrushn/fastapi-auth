from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from crud.crud_order import crud_order
from api.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.create_order(db, user["id"])

@router.put("/{order_id}")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    return crud_order.update_order_status(db, order_id, status)
