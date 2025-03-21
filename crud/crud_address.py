from sqlalchemy.orm import Session
from models.address import ShippingAddress, BillingAddress
from schemas.address import ShippingAddressCreate, BillingAddressCreate, ShippingAddressUpdate, BillingAddressUpdate

# **Shipping Address CRUD**
def create_shipping_address(db: Session, address: ShippingAddressCreate):
    db_address = ShippingAddress(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_shipping_address(db: Session, address_id: int):
    return db.query(ShippingAddress).filter(ShippingAddress.id == address_id).first()

def get_all_shipping_addresses(db: Session):
    return db.query(ShippingAddress).all()

def update_shipping_address(db: Session, address_id: int, address: ShippingAddressUpdate):
    db_address = db.query(ShippingAddress).filter(ShippingAddress.id == address_id).first()
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_shipping_address(db: Session, address_id: int):
    db_address = db.query(ShippingAddress).filter(ShippingAddress.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        return True
    return False

# **Billing Address CRUD**
def create_billing_address(db: Session, address: BillingAddressCreate):
    db_address = BillingAddress(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_billing_address(db: Session, address_id: int):
    return db.query(BillingAddress).filter(BillingAddress.id == address_id).first()

def get_all_billing_addresses(db: Session):
    return db.query(BillingAddress).all()

def update_billing_address(db: Session, address_id: int, address: BillingAddressUpdate):
    db_address = db.query(BillingAddress).filter(BillingAddress.id == address_id).first()
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_billing_address(db: Session, address_id: int):
    db_address = db.query(BillingAddress).filter(BillingAddress.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        return True
    return False
