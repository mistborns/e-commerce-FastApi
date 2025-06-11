from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str
    image_url: Optional[HttpUrl] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None  
    image_url: Optional[HttpUrl] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    total: int
    products: List[ProductOut]

