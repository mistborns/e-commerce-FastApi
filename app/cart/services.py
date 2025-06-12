from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.cart import models, schemas
from app.products import models as product_models

def add_to_cart(db : Session ,user_id : int, cart_item: schemas.CartItemCreate):
    
    check_product = db.query(product_models.Product).filter(product_models.Product.id == cart_item.product_id).first()
    if not check_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if check_product.stock == 0:
         raise HTTPException(status_code=400, detail="Sorry!,  product out of stock")
    
    if cart_item.quantity > check_product.stock:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST , detail="quantity not available in stock")
    
    existing = db.query(models.Cart).filter(models.Cart.user_id==user_id, models.Cart.product_id == cart_item.product_id).first()
    if existing:
        existing.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing)
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
        return new_item

def get_cart_items(db: Session ,user_id: int):
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart empty")
    cart_items_list = [schemas.CartItemOut.model_validate(item, from_attributes=True) for item in cart_items]
    return schemas.CartResponse(items=cart_items_list)



def update_cart_item(db: Session, user_id: int, product_id: int, data: schemas.CartItemUpdate):
    try:
        product = db.query(product_models.Product).filter(product_models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if data.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Quantity exceeds available stock")

        item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        item.quantity = data.quantity
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating cart item")

# if cart item is deleted shouldnt the product quantity be updated 

def delete_cart_item(db: Session, user_id: int, product_id: int):
    try:
        item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        db.delete(item)
        db.commit()
        return {"message": "Cart item deleted"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting cart item")
    

def clear_cart(db: Session, user_id: int):
    try:
        db.query(models.CartItem).filter_by(user_id=user_id).delete()
        db.commit()
        return {"message": "Cart cleared"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error clearing cart")
