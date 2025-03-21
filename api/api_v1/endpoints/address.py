from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from crud.crud_address import (
    create_shipping_address, get_shipping_address, get_all_shipping_addresses, update_shipping_address, delete_shipping_address,
    create_billing_address, get_billing_address, get_all_billing_addresses, update_billing_address, delete_billing_address
)
from schemas.address import (
    ShippingAddressCreate, ShippingAddressResponse, ShippingAddressUpdate,
    BillingAddressCreate, BillingAddressResponse, BillingAddressUpdate
)

router = APIRouter()

# 🚀 **Shipping Address Routes**

@router.post("/shipping/", response_model=ShippingAddressResponse)
def create_shipping_address_endpoint(address: ShippingAddressCreate, db: Session = Depends(get_db)):
    return create_shipping_address(db, address)

@router.get("/shipping/{address_id}", response_model=ShippingAddressResponse)
def get_shipping_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    address = get_shipping_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Shipping address not found")
    return address

@router.get("/shipping/", response_model=list[ShippingAddressResponse])
def get_all_shipping_addresses_endpoint(db: Session = Depends(get_db)):
    return get_all_shipping_addresses(db)

@router.put("/shipping/{address_id}", response_model=ShippingAddressResponse)
def update_shipping_address_endpoint(address_id: int, address: ShippingAddressUpdate, db: Session = Depends(get_db)):
    updated_address = update_shipping_address(db, address_id, address)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Shipping address not found")
    return updated_address

@router.delete("/shipping/{address_id}")
def delete_shipping_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    if not delete_shipping_address(db, address_id):
        raise HTTPException(status_code=404, detail="Shipping address not found")
    return {"message": "Shipping address deleted successfully"}

# 🚀 **Billing Address Routes**

@router.post("/billing/", response_model=BillingAddressResponse)
def create_billing_address_endpoint(address: BillingAddressCreate, db: Session = Depends(get_db)):
    return create_billing_address(db, address)

@router.get("/billing/{address_id}", response_model=BillingAddressResponse)
def get_billing_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    address = get_billing_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return address

@router.get("/billing/", response_model=list[BillingAddressResponse])
def get_all_billing_addresses_endpoint(db: Session = Depends(get_db)):
    return get_all_billing_addresses(db)

@router.put("/billing/{address_id}", response_model=BillingAddressResponse)
def update_billing_address_endpoint(address_id: int, address: BillingAddressUpdate, db: Session = Depends(get_db)):
    updated_address = update_billing_address(db, address_id, address)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return updated_address

@router.delete("/billing/{address_id}")
def delete_billing_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    if not delete_billing_address(db, address_id):
        raise HTTPException(status_code=404, detail="Billing address not found")
    return {"message": "Billing address deleted successfully"}