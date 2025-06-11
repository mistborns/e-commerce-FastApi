from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.products import schemas, services
from app.core.database import get_db

router = APIRouter(tags=["Public Products"])

@router.get("/products", response_model=schemas.ProductListResponse)
def list_public_products(category: str = None, min_price: float = None, max_price: float = None,
                         sort_by: str = None, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return services.filter_products(db, category, min_price, max_price, sort_by, page, page_size)

@router.get("/products/search", response_model=list[schemas.ProductOut])
def search_products(keyword: str, db: Session = Depends(get_db)):
    return services.search_products(db, keyword)

@router.get("/products/{product_id}", response_model=schemas.ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    return services.get_product_by_Id(db, product_id)
