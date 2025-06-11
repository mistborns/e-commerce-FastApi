from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, services
from app.core.database import get_db
from app.middlewares.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[schemas.OrderSummary])
def order_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.get_orders_for_user(db, current_user.id)

@router.get("/{order_id}", response_model=schemas.OrderOut)
def order_details(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.get_order_details(db, current_user.id, order_id)
