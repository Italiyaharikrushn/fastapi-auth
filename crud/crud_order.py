from sqlalchemy.orm import Session
from models.order import Order, OrderStatusEnum
from models import OrderItem, Product, BillingAddress
from fastapi import HTTPException
from schemas.order import OrderCreate, OrderUpdate

class CRUDOrder:
    def create_order(self, db: Session, user_id: int, order_data: OrderCreate):
        billing_address = db.query(BillingAddress).filter(BillingAddress.id == order_data.billing_address_id, BillingAddress.user_id == user_id).first()
        if not billing_address :
            raise HTTPException(status_code=400, detail="Invalid billing or shipping address")

        new_order = Order(
            user_id=user_id,
            billing_address_id=order_data.billing_address_id,
            status=OrderStatusEnum.pending,
            total_price=0.0
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        total_price = 0.0
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {item.product_id} not found")
            order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
            db.add(order_item)
            total_price += product.price * item.quantity

        new_order.total_price = total_price
        db.commit()
        db.refresh(new_order)

        return new_order

    def update_order_status(self, db: Session, order_id: int, status: OrderStatusEnum):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            return order
        return None

    def get_order_by_id(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    def get_orders_by_user(self, db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()

crud_order = CRUDOrder()
