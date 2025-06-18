from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth import schemas, services, utils


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db, user)



@router.post("/signin")
def signin(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = services.authenticate_user(user.email, user.password, db)
    
    # jwt token generation
    access_token = utils.create_access_token({"sub": db_user.email, "role": db_user.role})
    refresh_token = utils.create_refresh_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    return services.generate_reset_token(request.email, db)



@router.post("/reset-password")
def reset_password(data: schemas.ResetPassword, db: Session = Depends(get_db)):
    
    return services.reset_user_password(data, db)


@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(refresh_token: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    return services.refresh_access_token(refresh_token.token, db)