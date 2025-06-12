from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.orders import models, schemas

def get_orders_for_user(db: Session, user_id: int):
    try:
        return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.created_at.desc()).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error fetching orders")

def get_order_details(db: Session, user_id: int, order_id: int):
    try:
        order = db.query(models.Order).filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error retrieving order")
