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
        order_items_list = []

        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {item.product_id} not found")

            order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, status=OrderStatusEnum.pending)
            db.add(order_item)
            total_price += product.price * item.quantity
            order_items_list.append(order_item)

        new_order.total_price = total_price
        db.commit()
        db.refresh(new_order)

        return {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "status": new_order.status,
            "total_price": new_order.total_price,
            "order_items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "status": item.status,
                }
                for item in order_items_list
            ],
        }

    def get_order_by_id(self, db: Session, order_id: int):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None

        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        return {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_price": order.total_price,
            "order_items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "status": item.status,
                }
                for item in order_items
            ],
        }

    def get_orders_by_user(self, db: Session, user_id: int):
        orders = db.query(Order).filter(Order.user_id == user_id).all()
        return [
            {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "total_price": order.total_price,
                "order_items": [
                    {
                        "id": item.id,
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "status": item.status,
                    }
                    for item in db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
                ],
            }
            for order in orders
        ]

    def get_orders_for_seller(self, db: Session, seller_id: int):
        order_items = (
            db.query(OrderItem)
            .join(Product)
            .filter(Product.seller_id == seller_id)
            .all()
        )

        if not order_items:
            raise HTTPException(status_code=404, detail="No orders found for this seller")

        order_ids = {item.order_id for item in order_items}

        orders = db.query(Order).filter(Order.id.in_(order_ids)).all()

        return [
            {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "total_price": order.total_price,
                "order_items": [
                    {
                        "id": item.id,
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "status": item.status,
                    }
                    for item in db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
                ],
            }
            for order in orders
        ]

crud_order = CRUDOrder()
