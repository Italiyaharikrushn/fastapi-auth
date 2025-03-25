from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
import crud
from db.session import get_db
from api.dependencies import get_current_user # Middleware for authentication
from models import Product

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    if user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can create products")

    new_product = Product(
        title=product.title,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image=product.image,
        seller_id=user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, 
    updated_data: ProductUpdate, 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == user.id).first()
    
    if not product:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")

    for key, value in updated_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user.role == "seller":
        products = db.query(Product).filter(Product.seller_id == current_user.id).all()
    else:
        products = db.query(Product).all()

    product_list = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "seller_id": p.seller_id,
            "image_url": p.image,
        }
        for p in products
    ]

    return product_list

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == user.id).first()

    if not product:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
