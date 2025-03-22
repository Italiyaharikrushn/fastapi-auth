from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from crud.crud_order import crud_order
from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crud_order.create_order(db, user.id, order_data)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/user/orders", response_model=list[OrderResponse])
def get_user_orders(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.get_orders_by_user(db, user.id)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, status: OrderUpdate, db: Session = Depends(get_db)):
    order = crud_order.update_order_status(db, order_id, status.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
