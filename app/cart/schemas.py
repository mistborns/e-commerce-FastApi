from typing import List, Optional
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int 

    class Config:
        from_attributes=True

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)

class CartResponse(BaseModel):
    items: List[CartItemOut]

    class Config:
        from_attributes=True