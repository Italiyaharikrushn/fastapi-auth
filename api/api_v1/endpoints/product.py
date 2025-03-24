from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
import crud
from db.session import get_db
from api.dependencies import get_current_user # Middleware for authentication

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    user = Depends(get_current_user)
):
    new_product = crud.product.create(db, obj_in=product, created_by=user)

    if not new_product:
        raise HTTPException(status_code=403, detail="Only sellers can create products")
    
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, 
    updated_data: ProductUpdate, 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    updated_product = crud.product.update(db, product_id, updated_data.dict(), user)
    if not updated_product:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    return updated_product

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud.product.get_all_products(db, user)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    product = crud.product.get_by_id(db, product_id, user)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not authorized to view")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    deleted_product = crud.product.remove(db, product_id, user)
    if not deleted_product:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    return {"message": "Product deleted successfully"}
