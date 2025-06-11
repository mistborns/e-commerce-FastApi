from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id" , ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    product = relationship("Product")