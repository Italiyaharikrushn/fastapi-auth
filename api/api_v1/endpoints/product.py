from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from crud import crud_product
from db.session import get_db
from api.dependencies import get_current_user # Middleware for authentication

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    new_product = crud_product.create(db, product, user)
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
    updated_product = crud_product.update_product(db, product_id, updated_data.dict(), user)
    if not updated_product:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    return updated_product

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_product.get_all_products(db, user)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    product = crud_product.get_product_by_id(db, product_id, user)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not authorized to view")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    deleted_product = crud_product.delete_product(db, product_id, user)
    if not deleted_product:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    return {"message": "Product deleted successfully"}
