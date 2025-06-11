from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    total_amount: float
    status: OrderStatus
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderSummary(BaseModel):
    id: int
    created_at: datetime
    total_amount: float
    status: OrderStatus

    class Config:
        from_attributes = True
