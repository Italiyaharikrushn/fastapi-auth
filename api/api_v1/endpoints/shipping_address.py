from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.shipping_address import ShippingAddressCreate, ShippingAddressOut
from crud.crud_shipping_address import crud_shipping_address
from db.session import get_db

router = APIRouter(prefix="/shipping-address", tags=["Shipping Address"])

@router.post("/", response_model=ShippingAddressOut)
def create_shipping_address(address_data: ShippingAddressCreate, db: Session = Depends(get_db)):
    """Create a new shipping address"""
    return crud_shipping_address.create_shipping_address(db, address_data.dict())

@router.get("/{address_id}", response_model=ShippingAddressOut)
def fetch_shipping_address(address_id: int, db: Session = Depends(get_db)):
    """Fetch a shipping address by ID"""
    address = crud_shipping_address.get_shipping_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Shipping address not found")
    return address