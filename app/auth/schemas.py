from enum import Enum
import re
from pydantic import BaseModel , EmailStr, Field, field_validator

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    name: str = Field(strip_whitespace=True, min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.user

    # password strength check 
    @field_validator("password")
    def strong_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[\W_]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class UserOut(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

    # Pydantic expects dictionoary , orm_mode/from attribute allows the serialization of SQLalchemy models
    class Config:    
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    def strong_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("must have uppercase")
        if not re.search(r"[a-z]", value):
            raise ValueError("must have lowercase")
        if not re.search(r"\d", value):
            raise ValueError("must have digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("must have special character")
        return value 
    
class RefreshTokenRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"