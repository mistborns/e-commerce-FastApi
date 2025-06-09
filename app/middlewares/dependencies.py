from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from app.core.database import get_db
from app.auth.models import User
from app.auth.utils import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # chechks for logged in or requesting user 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# role checking for certain apis
def require_roles(required_roles: list, current_user: User = Depends(get_current_user)) -> User:
    # authorization checks basically
    if current_user.role not in required_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user
