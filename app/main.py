from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

@app.get("/")
def root():
     return {"message": "ecommerce with fastapi"}

app.include_router(auth_router)

