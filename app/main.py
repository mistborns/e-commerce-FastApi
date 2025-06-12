from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.products.admin_routes import router as admin_products_router
from app.products.public_routes import router as public_products_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as order_router

app = FastAPI()

@app.get("/")
def root():
     return {"message": "ecommerce with fastapi"}

app.include_router(auth_router)
app.include_router(admin_products_router)
app.include_router(public_products_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(order_router)
