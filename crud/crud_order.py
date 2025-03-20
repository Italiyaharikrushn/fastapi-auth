from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Order, Product, OrderItem, ShippingAddress, BillingAddress, OrderStatus
from schemas import OrderCreateSchema

def create_order(db: Session, order_data: OrderCreateSchema):
    # Validate product existence before creating an order
    product_ids = [item.product_id for item in order_data.items]
    products = {p.id: p for p in db.query(Product).filter(Product.id.in_(product_ids)).all()}

    if len(products) != len(product_ids):
        missing_ids = set(product_ids) - products.keys()
        raise HTTPException(status_code=404, detail=f"Products not found: {missing_ids}")

    # Calculate total price
    total_price = sum(products[item.product_id].price * item.quantity for item in order_data.items)

    # Create new order
    new_order = Order(
        customer_id=order_data.customer_id,
        shipping_address_id=order_data.shipping_address_id,
        billing_address_id=order_data.billing_address_id,
        total_price=total_price,
        status=OrderStatus.pending  # Ensure initial status is set
    )
    db.add(new_order)
    db.flush()  # Assign ID before adding order items

    # Create order items
    order_items = [
        OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, price=products[item.product_id].price)
        for item in order_data.items
    ]
    
    db.bulk_save_objects(order_items)
    db.commit()
    db.refresh(new_order)
    
    return new_order

def update_order_status(db: Session, order_id: int, status: OrderStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

class CRUDOrder:
    # Define your CRUD methods here
    pass

crud_order = CRUDOrder()