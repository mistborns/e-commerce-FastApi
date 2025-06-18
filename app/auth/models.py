from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum
from app.core.database import Base
import enum
from sqlalchemy.orm import relationship

# role enum
class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

# user table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    # defined relationship
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")


# reset token table
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    # relationship 
    user = relationship("User", back_populates="password_reset_tokens")
