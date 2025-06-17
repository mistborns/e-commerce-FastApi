from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.products.admin_routes import router as admin_products_router
from app.products.public_routes import router as public_products_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as order_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exception_handler import  http_exception_handler,validation_exception_handler,unhandled_exception_handler


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


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)