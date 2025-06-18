
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.middlewares.dependencies import get_current_user
from app.core.database import get_db
from app.cart import models as cart_models
from app.products import models as product_models
from app.orders import models as order_models
from app.core.logger import logger

router = APIRouter(prefix="/checkout", tags=["Checkout"])


# checkout route
@router.post("")
def checkout(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        cart_items = db.query(cart_models.Cart).filter_by(user_id=current_user.id).all() # gets item list
        if not cart_items:
            logger.info(f"User {current_user.id} attempted checkout with empty cart.")
            raise HTTPException(status_code=400, detail="Cart is empty")

        total = 0
        order_items = []

        for item in cart_items: # iterating through every product
            product = db.query(product_models.Product).filter_by(id=item.product_id).first()
            if not product or product.stock < item.quantity:
                logger.warning(f"Checkout failed for user {current_user.id},products out of stock")
                raise HTTPException(status_code=400, detail=f"Product {item.product_id} is unavailable or out of stock")

            total += product.price * item.quantity
            product.stock -= item.quantity # decreases product quantity after checkout only 

            order_items.append(order_models.OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            ))

        order = order_models.Order(
            user_id=current_user.id,
            total_amount=total,
            status=order_models.OrderStatus.paid,
            items=order_items
        )
        db.add(order)
        db.query(cart_models.Cart).filter_by(user_id=current_user.id).delete() # deletes the user cart 
        db.commit()

        logger.info(f"User {current_user.id} placed order {order.id} successfully.")
        return {"message": "Payment successful, order placed", "order_id": order.id}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Checkout failed for user : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
