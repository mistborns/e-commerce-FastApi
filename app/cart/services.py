from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.cart import models, schemas
from app.products import models as product_models
from app.core.logger import logger


def add_to_cart(db : Session ,user_id : int, cart_item: schemas.CartItemCreate):
    try:        
        check_product = db.query(product_models.Product).filter(product_models.Product.id == cart_item.product_id).first()
        if not check_product:
            logger.warning(f"Product with ID {cart_item.product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        if check_product.stock == 0:
            logger.warning(f"Product with ID {cart_item.product_id} is out of stock")
            raise HTTPException(status_code=400, detail="Sorry!,  product out of stock")
        
        if cart_item.quantity > check_product.stock:
            logger.warning(f"Requested quantity {cart_item.quantity} exceeds stock for product {cart_item.product_id}.")
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST , detail="quantity not available in stock")
        
        existing = db.query(models.Cart).filter(models.Cart.user_id==user_id, models.Cart.product_id == cart_item.product_id).first()
        if existing:
            existing.quantity += cart_item.quantity
            db.commit()
            db.refresh(existing)
            logger.info(f"increased quantity of {cart_item.product_id} in {user_id}'s cart.")
            return existing
        else:
            new_item = models.Cart(
                user_id=user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
                )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            logger.info(f"Added new product {cart_item.product_id}in user {user_id}'s cart.")
            return new_item
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding to cart : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_cart_items(db: Session ,user_id: int):
    try:    
        cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
        if not cart_items:
            logger.info(f"User {user_id} has an empty cart.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart empty")
        
        #converts the orm models objects in list (cart_items) to pydantic models(CartItemOut)
        cart_items_list = [schemas.CartItemOut.model_validate(item, from_attributes=True) for item in cart_items]
        return schemas.CartResponse(items=cart_items_list) 
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching cart items : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def update_cart_item(db: Session, user_id: int, product_id: int, data: schemas.CartItemUpdate):
    try:
        product = db.query(product_models.Product).filter(product_models.Product.id == product_id).first()
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found")
        
        if data.quantity > product.stock:
            logger.warning(f"Requested quantity {data.quantity} exceeds stock for product {product_id}")
            raise HTTPException(status_code=400, detail="Quantity exceeds available stock")

        item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            logger.warning(f"Cart item for product {product_id} not found for user {user_id}.")
            raise HTTPException(status_code=404, detail="Cart item not found")

        item.quantity = data.quantity
        db.commit()
        db.refresh(item)
        logger.info(f"Updated cart item quantity for user {user_id} with product {product_id}")
        return item
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating cart item : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# if cart item is deleted shouldnt the product quantity be updated 

def delete_cart_item(db: Session, user_id: int, product_id: int):
    try:
        item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            logger.warning(f"Cart item for product {product_id} not found for user {user_id}.")
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        db.delete(item)
        db.commit()
        logger.info(f"Deleted cart item for user {user_id} with product {product_id}.")
        return {"message": "Cart item deleted"}
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Erron deleting cart item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

