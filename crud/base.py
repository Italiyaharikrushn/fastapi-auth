from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from models import User, Cart, OrderItem
from sqlalchemy.orm import Session
from db.base_class import Base
from schemas.user import UserSearch
from models.order import Order, OrderStatusEnum
from fastapi import HTTPException
from schemas.order import OrderCreate

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int=0, limit: int=100,
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()    
 
    def create(self, db: Session, *, obj_in: CreateSchemaType, created_by=None) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["created_by"] = created_by
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        modified_by=None
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["modified_by"] = modified_by
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def checkout(self, db: Session, user_id: int, billing_address_id: int, order_data: OrderCreate) -> Order:
        cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "active").first()
        if not cart:
            raise HTTPException(status_code=400, detail="Cart is empty or not found.")
        
        db_order = Order(
            user_id=user_id,
            billing_address_id=billing_address_id,
            status=OrderStatusEnum.PENDING,
            total_amount=cart.total_amount,
            created_by=user_id
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        for cart_item in cart.items:
            db_order_item = OrderItem(
                order_id=db_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price,  # Assuming the CartItem has a product relationship
            )
            db.add(db_order_item)
        
        db.commit()
        return db_order
    
    def accept_order(self, db: Session, order_id: int) -> Order:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if db_order.status != OrderStatusEnum.PENDING:
            raise HTTPException(status_code=400, detail="Order is already accepted or processed")
        
        db_order.status = OrderStatusEnum.ACCEPTED
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return db_order
