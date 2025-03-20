from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.billing_address import BillingAddressCreate, BillingAddressOut
from crud.crud_billing_address import crud_billing_address
from db.session import get_db

router = APIRouter(prefix="/billing-address", tags=["Billing Address"])

@router.post("/", response_model=BillingAddressOut)
def add_billing_address(address_data: BillingAddressCreate, db: Session = Depends(get_db)):
    """Adds a new billing address"""
    return crud_billing_address.create_billing_address(db, address_data.dict())

@router.get("/{customer_id}", response_model=BillingAddressOut)
def fetch_billing_address(customer_id: int, db: Session = Depends(get_db)):
    """Fetch the billing address for a customer"""
    address = crud_billing_address.get_billing_address(db, customer_id)
    if not address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return address
