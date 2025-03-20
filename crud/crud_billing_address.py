from sqlalchemy.orm import Session
from models import BillingAddress

class CRUDBillingAddress:
    def get_billing_address(self, db: Session, address_id: int):
        return db.query(BillingAddress).filter(BillingAddress.id == address_id).first()

    def create_billing_address(self, db: Session, address_data):
        db_address = BillingAddress(**address_data)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

crud_billing_address = CRUDBillingAddress()
