from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.products import schemas, services
from app.core.database import get_db
from app.middlewares.dependencies import require_roles

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

@router.post("", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), 
                   current_user=Depends(require_roles(["admin"]))):
    
    return services.create_product(db, product)


@router.get("", response_model=schemas.ProductListResponse)
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
                  current_user=Depends(require_roles(["admin"]))):
    
    return services.get_products(db, skip, limit)


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_Id(product_id: int, db: Session = Depends(get_db), 
                current_user=Depends(require_roles(["admin"]))):
    
    return services.get_product_by_Id(db, product_id)


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), 
                   current_user=Depends(require_roles(["admin"]))):
    
    return services.update_product(db, product_id, product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), 
                   current_user=Depends(require_roles(["admin"]))):
    
    return services.delete_product(db, product_id)
