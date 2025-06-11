from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.products.admin_routes import router as admin_products_router
from app.products.public_routes import router as public_products_router

app = FastAPI()

@app.get("/")
def root():
     return {"message": "ecommerce with fastapi"}

app.include_router(auth_router)
app.include_router(admin_products_router)
app.include_router(public_products_router)

