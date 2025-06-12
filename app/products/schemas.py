from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional, List


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, strip_whitespace=True)
    description: Optional[str] 
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1, strip_whitespace=True)
    image_url: Optional[HttpUrl] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    description: Optional[str] 
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    image_url: Optional[HttpUrl] = None

    
class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    total: int 
    products: List[ProductOut]