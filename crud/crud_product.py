from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate

class CRUDProduct:
    def create(self, db: Session, product: ProductCreate, user):
        if user.role != "seller":
            return None
        db_product = Product(
            title=product.title,
            description=product.description,
            price=product.price,
            stock=product.stock,
            image=product.image,
            seller_id=user.id  # ✅ Fix here
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update_product(self, db: Session, product_id: int, updated_data: dict, user: dict):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product or (user.role == "seller" and product.seller_id != user.id):  # ✅ Fix here
            return None
        for key, value in updated_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    def get_all_products(self, db: Session, user: dict):
        if user.role == "seller":
            return db.query(Product).filter(Product.seller_id == user.id).all()  # ✅ Fix here
        return db.query(Product).all()

    def get_product_by_id(self, db: Session, product_id: int, user: dict):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product or (user.role == "seller" and product.seller_id != user.id):  # ✅ Fix here
            return None
        return product

    def delete_product(self, db: Session, product_id: int, user: dict):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product or (user.role == "seller" and product.seller_id != user.id):  # ✅ Fix here
            return None
        db.delete(product)
        db.commit()
        return product

crud_product = CRUDProduct()
