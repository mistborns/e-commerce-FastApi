from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.cart import schemas, services
from app.core.database import get_db
from app.middlewares.dependencies import require_roles

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("", response_model=schemas.CartResponse)
def view_cart(db: Session = Depends(get_db), current_user=Depends(require_roles(["user"]))):
    return services.get_cart_items(db, current_user.id)
    

@router.post("", response_model=schemas.CartItemOut)
def add_item(item: schemas.CartItemCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["user"]))):
    return services.add_to_cart(db, current_user.id, item)

@router.put("/{product_id}",response_model=schemas.CartItemOut)
def update_item(product_id: int, data: schemas.CartItemUpdate,
                 db: Session = Depends(get_db), current_user=Depends(require_roles(["user"]))):
    return services.update_cart_item(db, current_user.id, product_id, data)

@router.delete("/{product_id}")
def delete_item(product_id: int, db: Session = Depends(get_db), current_user=Depends(require_roles(["user"]))):
    return services.delete_cart_item(db, current_user.id, product_id)
