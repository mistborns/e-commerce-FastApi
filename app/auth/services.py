from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.auth import schemas, models, utils
from fastapi import HTTPException, status

def create_user(db: Session, user: schemas.UserCreate) -> dict:
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Email already registered", "code": 400})
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


def generate_reset_token(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail= "User not found")
    

    token = utils.create_reset_token()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=utils.RESET_TOKEN_EXPIRE_MINUTES)
    reset_token_data = models.PasswordResetToken(user_id=user.id, token=token, expiration_time=expiration) #default for used is false already
    db.add(reset_token_data)
    db.commit()
    utils.send_reset_email(user.email, token)
    return {"message": "Password reset link sent to your email"}


def reset_user_password(data: schemas.ResetPassword,db: Session, ) -> dict:
   
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == data.token).first()
    if not reset_token or reset_token.used == "True":
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid or used token", "code": 400})
    
    expiration = reset_token.expiration_time
    if expiration.tzinfo is None: # adds timezone info to expiration time (it did not have that in db value)
        expiration = expiration.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expiration:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Token expired", "code": 400})
    
    user = db.query(models.User).filter(models.User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": True, "message": "User not found", "code": 404})
    
    user.hashed_password = utils.hash_password(data.new_password)
    reset_token.used = True
    db.commit()
    return {"message": "Password reset successfully"}