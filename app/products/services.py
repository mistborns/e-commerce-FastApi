from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.products import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    try:
        db_product = models.Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating product")

def get_products(db: Session, skip: int = 0, limit: int = 10):
    try:
        total = db.query(models.Product).count()
        products = db.query(models.Product).offset(skip).limit(limit).all()
        return {"total": total, "products": products}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error fetching products")

def get_product_by_Id(db: Session, product_id: int):
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error retrieving product")

def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    try:
        product = get_product_by_Id(db, product_id)
        for key, value in product_data.model_dump(exclude_unset=True).items(): # corrected this dict to model_dump
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating product")

def delete_product(db: Session, product_id: int):
    try:
        product = get_product_by_Id(db, product_id)
        db.delete(product)
        db.commit()
        return {"detail": "Product deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting product")

def search_products(db: Session, keyword: str):
    try:
        return db.query(models.Product).filter(models.Product.name.ilike(f"%{keyword}%")).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error searching products")

def filter_products(db: Session, category: str = None, min_price: float = None, max_price: float = None,
                    sort_by: str = None, page: int = 1, page_size: int = 10):
    try:
        query = db.query(models.Product)

        if category:
            query = query.filter(models.Product.category == category)
        if min_price is not None:
            query = query.filter(models.Product.price >= min_price)
        if max_price is not None:
            query = query.filter(models.Product.price <= max_price)

        if sort_by in ["price", "name", "stock"]:
            query = query.order_by(getattr(models.Product, sort_by))

        total = query.count()
        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()
        return {"total": total, "products": products}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error filtering products")

