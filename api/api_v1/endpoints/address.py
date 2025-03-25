from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
import crud

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
    return crud.address.create(db, user.id, address_data)

@router.get("/billing/{address_id}", response_model=BillingAddressResponse)
def get_billing_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    address = crud.address.get(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return address

@router.get("/billing/", response_model=list[BillingAddressResponse])
def get_all_billing_addresses_endpoint(db: Session = Depends(get_db)):
    return crud.address.get(db)

@router.put("/billing/{address_id}", response_model=BillingAddressResponse)
def update_billing_address_endpoint(address_id: int, address: BillingAddressUpdate, db: Session = Depends(get_db)):
    updated_address = crud.address.update(db, address_id, address)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return updated_address

@router.delete("/billing/{address_id}")
def delete_billing_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    if not crud.address.remove(db, address_id):
        raise HTTPException(status_code=404, detail="Billing address not found")
    return {"message": "Billing address deleted successfully"}
