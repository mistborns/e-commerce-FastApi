
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.products import models, schemas
from sqlalchemy import asc , desc
from app.core.logger import logger

# creates product
def create_product(db: Session, product: schemas.ProductCreate):
    try:    #**obj.model_dump unpacks the dict and converts to kv pairs 
        db_product = models.Product(**product.model_dump()) # model_dump converts pydantic models to dict 
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product created with ID {db_product.id}")
        return db_product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# gets all products
def get_products(db: Session, page: int = 1, limit: int = 10):
    try:

        skip = (page - 1) * limit

        total = db.query(models.Product).count()

        products = db.query(models.Product).offset(skip).limit(limit).all()

        logger.info(f"Fetched every product")
        return {"total": total, "products": products}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

# specific product by id 
def get_product_by_Id(db: Session, product_id: int):
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            logger.warning(f"Product with ID {product_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# update product
def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    try:
        product = get_product_by_Id(db, product_id)
        for key, value in product_data.model_dump(exclude_unset=True).items(): # corrected this dict to model_dump
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        logger.info(f"Product {product_id} updated")
        return product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# delete product
def delete_product(db: Session, product_id: int):
    try:
        product = get_product_by_Id(db, product_id)
        db.delete(product)
        db.commit()
        logger.info(f"Product {product_id} deleted")
        return {"detail": "Product deleted successfully"}
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
# search products
def search_products(db: Session, keyword: str):
    try:
        results = db.query(models.Product).filter(models.Product.name.ilike(f"%{keyword}%")).all()

        if not results:
            raise HTTPException(status_code=404, detail=f"Product with {keyword} keyword not foubnd")
        logger.info(f"Search for '{keyword}' returned {len(results)} results")
        return results
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error searching products with keyword '{keyword}': {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching products")

# filter diff prods
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

        if sort_by == "price_asc":
            query = query.order_by(asc(models.Product.price))
        elif sort_by == "price_desc":
            query = query.order_by(desc(models.Product.price))


        total = query.count()
        skip = (page - 1) * page_size
        products = query.offset(skip).limit(page_size).all()

        logger.info(f"Filtered products: total={total}, returned={len(products)}, page={page}, category={category}")
        return {"total": total, "products": products}
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error filtering products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
