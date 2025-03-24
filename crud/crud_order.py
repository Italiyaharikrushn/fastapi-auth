from sqlalchemy.orm import Session
from models.order import Order, OrderStatusEnum
from models import OrderItem, Product, BillingAddress, Cart, CartItem
from fastapi import HTTPException

class CRUDOrder:
    def checkout(self, db: Session, user_id: int, billing_address_id: int):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise HTTPException(status_code=400, detail="Cart is empty")

        billing_address = db.query(BillingAddress).filter(BillingAddress.id == billing_address_id, BillingAddress.user_id == user_id).first()
        if not billing_address:
            raise HTTPException(status_code=400, detail="Invalid billing address")

        new_order = Order(
            user_id=user_id,
            billing_address_id=billing_address_id,
            status=OrderStatusEnum.pending,
            total_price=0.0
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        total_price = 0.0

        for item in cart_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {item.product_id} not found")

            order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, status=OrderStatusEnum.pending)
            db.add(order_item)
            total_price += product.price * item.quantity

        new_order.total_price = total_price
        db.commit()
        db.refresh(new_order)

        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()

        return {
            "message": "Order placed successfully",
            "order_id": new_order.id,
            "total_price": new_order.total_price
        }

    def get_order_by_id(self, db: Session, order_id: int):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        return {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_price": order.total_price,
            "order_items": order_items
        }

    def accept_order(self, db: Session, order_id: int):
        # Step 1: Retrieve the order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Step 2: Ensure the order is in 'pending' status
        if order.status != OrderStatusEnum.pending:
            raise HTTPException(status_code=400, detail="Order cannot be accepted because it is not in pending status")

        # Step 3: Update the order status to 'accepted'
        order.status = OrderStatusEnum.ready_to_ship
        db.commit()  # Commit the changes to the database
        db.refresh(order)  # Refresh the order object to get the updated status
        
        return {
            "message": "Order accepted and marked as ready to ship",
            "order_id": order.id,
            "status": order.status
        }

crud_order = CRUDOrder()
