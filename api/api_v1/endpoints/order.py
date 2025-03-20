from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.order import OrderCreateSchema, OrderResponseSchema, OrderStatus
from crud.crud_order import create_order, update_order_status, get_order, delete_order
from db.session import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponseSchema)
def place_order(order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    """Creates a new order"""
    return create_order(db, order_data)

@router.put("/{order_id}/status/{status}")
def change_order_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    """Updates the status of an order"""
    return update_order_status(db, order_id, status)

@router.get("/{order_id}", response_model=OrderResponseSchema)
def fetch_order(order_id: int, db: Session = Depends(get_db)):
    """Fetch order details"""
    return get_order(db, order_id)

@router.delete("/{order_id}")
def remove_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    return delete_order(db, order_id)
