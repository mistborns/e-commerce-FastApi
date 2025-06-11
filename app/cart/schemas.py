from typing import List, Optional
from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int 

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int 

    class Config:
        from_attributes=True

class CartItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: int

class CartResponse(BaseModel):
    items: List[CartItemOut]