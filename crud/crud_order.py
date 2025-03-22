from sqlalchemy.orm import Session
from models.order import Order, OrderStatusEnum
from models import OrderItem, Product, BillingAddress
from fastapi import HTTPException
from schemas.order import OrderCreate, OrderUpdate
from typing import Optional

class CRUDOrder:
    def create_order(self, db: Session, user_id: int, order_data: OrderCreate):
        billing_address = db.query(BillingAddress).filter(
            BillingAddress.id == order_data.billing_address_id, 
            BillingAddress.user_id == user_id
        ).first()

        if not billing_address:
            raise HTTPException(status_code=400, detail="Invalid billing address")

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

    def update_order_status(self, db: Session, order_id: int, status: OrderStatusEnum, seller_id: Optional[int] = None):
        order_items = (
            db.query(OrderItem)
            .join(Product)
            .filter(OrderItem.order_id == order_id, Product.seller_id == seller_id)
            .all()
        )

        if not order_items:
            raise HTTPException(status_code=400, detail="Order not found or not authorized")

        for item in order_items:
            item.status = status

        remaining_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if all(item.status in [OrderStatusEnum.cancelled, OrderStatusEnum.ready_to_ship] for item in remaining_items):
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status = (
                    OrderStatusEnum.ready_to_ship if all(item.status == OrderStatusEnum.ready_to_ship for item in remaining_items) else OrderStatusEnum.cancelled
                )

        db.commit()
        return {"message": f"Order {order_id} updated successfully"}

    def get_order_by_id(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    def get_orders_by_user(self, db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()

    def get_orders_for_seller(self, db: Session, seller_id: int):
        order_items = (
            db.query(OrderItem)
            .join(Product)
            .filter(Product.seller_id == seller_id)
            .all()
        )

        if not order_items:
            raise HTTPException(status_code=404, detail="No orders found for this seller")

        order_ids = {item.order_id for item in order_items}  # Get unique order IDs

        orders = db.query(Order).filter(Order.id.in_(order_ids)).all()

        return orders

crud_order = CRUDOrder()
