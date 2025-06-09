from enum import Enum
from pydantic import BaseModel , EmailStr, Field

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

class UserOut(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

    # Pydantic expects dictionoary , orm_mode/from attribute allows the serialization of SQLalchemy models
    class Config:    
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)