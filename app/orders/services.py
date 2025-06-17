import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.orders import models, schemas
from app.core.logger import logger

def get_orders_for_user(db: Session, user_id: int):
    try:
        return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.created_at.desc()).all()
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to fetch orders for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_order_details(db: Session, user_id: int, order_id: int):
    try:
        order = db.query(models.Order).filter_by(id=order_id, user_id=user_id).first()
        if not order:
            logger.warning(f"Order {order_id} not found for user {user_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to fetch a order detail for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
