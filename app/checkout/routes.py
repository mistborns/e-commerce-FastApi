from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.middlewares.dependencies import get_current_user
from app.core.database import get_db
from app.cart import models as cart_models
from app.products import models as product_models
from app.orders import models as order_models

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("")
def checkout(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        cart_items = db.query(cart_models.Cart).filter_by(user_id=current_user.id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total = 0
        order_items = []

        for item in cart_items:
            product = db.query(product_models.Product).filter_by(id=item.product_id).first()
            if not product or product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Product {item.product_id} is unavailable or out of stock")

            total += product.price * item.quantity
            product.stock -= item.quantity

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
        db.query(cart_models.Cart).filter_by(user_id=current_user.id).delete()
        db.commit()

        return {"message": "Payment successful, order placed", "order_id": order.id}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Checkout failed")
