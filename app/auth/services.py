from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.auth import schemas, models, utils
from fastapi import HTTPException, status
from app.core.logger import logger 

# function creates a user in db
def create_user(db: Session, user: schemas.UserCreate) -> dict:
    try:    
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            logger.warning(f"registering with existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
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
        logger.info(f"New user created: {user.email}")
        return new_user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# authenticates user
def authenticate_user(email: str, password: str, db: Session):
    try:    
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user or not utils.verify_password(password, user.hashed_password):
            logger.warning(f"authentication fail for email: {email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        logger.info(f"User authenticated successfully: {email}")
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# generates token for password reset / sends email
def generate_reset_token(email: str, db: Session):
    try:    
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            logger.warning(f"Password reset attempt for non-existing user: {email}")
            raise HTTPException(status_code=404, detail= "User not found")
        

        token = utils.create_reset_token()
        expiration = datetime.now(timezone.utc) + timedelta(minutes=utils.RESET_TOKEN_EXPIRE_MINUTES)
        reset_token_data = models.PasswordResetToken(user_id=user.id, token=token, expiration_time=expiration) #default for used is false already
        db.add(reset_token_data)
        db.commit()
        utils.send_reset_email(user.email, token)

        logger.info(f"Password reset link sent to: {email}")
        return {"message": "Password reset link sent to your email"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error generating reset token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# validates reset token and actually resets password 
def reset_user_password(data: schemas.ResetPassword,db: Session, ) -> dict:
    try:
        reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == data.token).first()

        if not reset_token or reset_token.used == True:
            logger.warning(f"Invalid or used token attempt: {data.token}")
            raise HTTPException(status_code=400, detail="Invalid or used token")
        
        expiration = reset_token.expiration_time
        if expiration.tzinfo is None: # adds timezone info to expiration time (it did not have that in db value)
            expiration = expiration.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > expiration:
            logger.warning(f"Expired token attempt: {data.token}")
            raise HTTPException(status_code=400, detail={"error": True, "message": "Token expired", "code": 400})
        
        user = db.query(models.User).filter(models.User.id == reset_token.user_id).first()
        if not user:
            logger.warning(f"User not found for reset token: {data.token}")
            raise HTTPException(status_code=404, detail={"error": True, "message": "User not found", "code": 404})
        
        user.hashed_password = utils.hash_password(data.new_password)
        reset_token.used = True
        db.commit()

        logger.info(f"Password reset successfully for user: {user.email}")
        return {"message": "Password reset successfully"}
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")