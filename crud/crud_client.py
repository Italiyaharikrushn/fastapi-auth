from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.client import Client
from db.base_class import Base
from schemas.client import ClientBase,ClientCreate,ClientUpdate
ModelType = TypeVar("ModelType", bound=Base)

class CRUDClient(CRUDBase[Client, ClientCreate,ClientUpdate]): 
    def get(self, db: Session):
        return db.query(Client).all()
    
    def get_by_id(self, db: Session, client_id: int):
        return db.query(Client).filter(Client.id == client_id).first()
    
    def update(self, db: Session, db_obj: Client, obj_in: ClientUpdate):
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int):
        return db.query(Client).filter(Client.id == id).first()

client = CRUDClient(Client)
