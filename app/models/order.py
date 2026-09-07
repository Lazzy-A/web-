from sqlalchemy import Column, Integer,Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    