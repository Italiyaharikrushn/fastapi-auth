from sqlalchemy.orm import Session
from models import ShippingAddress

class CRUDShippingAddress:
    def get_shipping_address(self, db: Session, address_id: int):
        return db.query(ShippingAddress).filter(ShippingAddress.id == address_id).first()

    def create_shipping_address(self, db: Session, address_data):
        db_address = ShippingAddress(**address_data)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

crud_shipping_address = CRUDShippingAddress()
