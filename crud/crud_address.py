from sqlalchemy.orm import Session
from models.address import BillingAddress
from schemas.address import BillingAddressCreate, BillingAddressUpdate

# Create Billing Address
def create_billing_address(db: Session, user_id: int, address_data: BillingAddressCreate):
    new_address = BillingAddress(user_id=user_id, **address_data.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

# Get Single Billing Address
def get_billing_address(db: Session, address_id: int):
    return db.query(BillingAddress).filter(BillingAddress.id == address_id).first()

# Get All Billing Addresses
def get_all_billing_addresses(db: Session):
    return db.query(BillingAddress).all()

# Update Billing Address
def update_billing_address(db: Session, address_id: int, address: BillingAddressUpdate):
    db_address = db.query(BillingAddress).filter(BillingAddress.id == address_id).first()
    if db_address:
        for key, value in address.dict(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

# Delete Billing Address
def delete_billing_address(db: Session, address_id: int):
    db_address = db.query(BillingAddress).filter(BillingAddress.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        return True
    return False
