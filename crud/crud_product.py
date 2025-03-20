# from typing import TypeVar
# from pydantic import BaseModel
# from models.product import Product
# from crud.base import CRUDBase
# from schemas.product import ProductCreate, ProductUpdate
# from db.base_class import Base
# from sqlalchemy.orm import Session

# ModelType = TypeVar("ModelType", bound=Base)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# def create_product(db: Session, product_data: ProductCreate):
#     new_product = Product(**product_data.dict())
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product

# def get_products(db: Session):
#     return db.query(Product).all()

# def get_product_by_id(db: Session, product_id: int):
#     return db.query(Product).filter(Product.id == product_id).first()

# def update_product(db: Session, product_id: int, product_update: ProductUpdate):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product:
#         for key, value in product_update.dict(exclude_unset=True).items():
#             setattr(product, key, value)
#         db.commit()
#         db.refresh(product)
#     return product

# def delete_product(db: Session, product_id: int):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product:
#         db.delete(product)
#         db.commit()
#     return product

from typing import TypeVar, Optional, List
from pydantic import BaseModel
from models import Product, User
from crud.base import CRUDBase
from schemas.product import ProductCreate, ProductUpdate
from db.base_class import Base
from fastapi import Depends, HTTPException
from api import dependencies
from sqlalchemy.orm import Session
import logging
from api.dependencies import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# create product
def create_product(db: Session, product_data: ProductCreate) -> Optional[Product]:
    try:
        new_product = Product(**product_data.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        logger.info(f"Product created successfully: {new_product.id}")
        return new_product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        db.rollback()
        return None

# get all product
def get_products(db: Session, current_seller: User) -> List[Product]:
    products = db.query(Product).filter(Product.seller_id == current_seller.id).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this seller")
    
    return products

# get single product
def get_product_by_id(db: Session, product_id: int, current_seller: User) -> Optional[Product]:
    product = db.query(Product).filter(
        Product.id == product_id, Product.seller_id == current_seller.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or access denied")

    return product

# update product
def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            update_data = product_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            db.commit()
            db.refresh(product)
            logger.info(f"Product updated: {product.id}")
            return product
        else:
            logger.warning(f"Product not found with ID: {product_id}")
            return None
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        db.rollback()
        return None

# create product
def delete_product(db: Session, product_id: int) -> Optional[Product]:
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            logger.info(f"Product deleted: {product.id}")
            return product
        else:
            logger.warning(f"Product not found with ID: {product_id}")
            return None
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        db.rollback()
        return None


# # get all product
# def get_products(db: Session, role: str, seller_id: Optional[int]) -> List[Product]:
#     try:
#         if role == "seller" and seller_id:
#             products = db.query(Product).filter(Product.seller_id == seller_id).all()
#             logger.info(f"Retrieved {len(products)} products for seller ID: {seller_id}")
#         else:
#             products = db.query(Product).all()
#             logger.info(f"Retrieved {len(products)} products for {role}")
#         return products
#     except Exception as e:
#         logger.error(f"Error retrieving products: {e}")
#         return []

# # get single product
# def get_product_by_id(db: Session, product_id: int, role: str, seller_id: Optional[int]) -> Optional[Product]:
#     try:
#         if role == "seller" and seller_id:
#             product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller_id).first()
#         else:
#             product = db.query(Product).filter(Product.id == product_id).first()

#         if product:
#             logger.info(f"Product retrieved: {product.id}")
#         else:
#             logger.warning(f"Product not found with ID: {product_id} for role: {role}")
#         return product
#     except Exception as e:
#         logger.error(f"Error retrieving product by ID: {e}")
#         return None
