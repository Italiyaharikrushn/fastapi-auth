from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from api import dependencies
from models.product import Product
from models.user import User
from models.document import Document
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from crud.crud_product import create_product, get_products, get_product_by_id, update_product, delete_product
from db.session import get_db
from api.dependencies import get_current_user
import uuid
import shutil

router = APIRouter()

IMAGE_DIR = Path("static/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# add product
@router.post("/add", response_model=ProductResponse)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data)

# get all product
@router.get("/", response_model=list[ProductResponse])
def fetch_products( db: Session = Depends(get_db), current_seller: User = Depends(get_current_user)):
    return get_products(db, current_seller)

# get singel product
@router.get("/{product_id}", response_model=ProductResponse)
def fetch_product(product_id: int, db: Session = Depends(get_db), current_seller: User = Depends(get_current_user)):
    product = get_product_by_id(db, product_id, current_seller)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# update product
@router.put("/{product_id}", response_model=ProductResponse)
def modify_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_seller: User = Depends(get_current_user),):
    updated_product = update_product(db, product_id, product_update, current_seller)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# delete product
@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db), current_seller: User = Depends(get_current_user)):
    deleted_product = delete_product(db, product_id, current_seller)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
