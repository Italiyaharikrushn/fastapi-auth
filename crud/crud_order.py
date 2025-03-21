from sqlalchemy.orm import Session
from models.order import Order, OrderStatusEnum

class CRUDOrder:
    def create_order(self, db: Session, user_id: int):
        order = Order(user_id=user_id)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def update_order_status(self, db: Session, order_id: int, status: OrderStatusEnum):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            return order
        return None

crud_order = CRUDOrder()
