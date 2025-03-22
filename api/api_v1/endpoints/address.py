from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from crud.crud_address import (
    create_billing_address, get_billing_address, get_all_billing_addresses, update_billing_address, delete_billing_address
)
from schemas.address import (
    BillingAddressCreate, BillingAddressResponse, BillingAddressUpdate
)
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/billing/", response_model=BillingAddressResponse)
def add_billing_address(
    address_data: BillingAddressCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return create_billing_address(db, user.id, address_data)

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
