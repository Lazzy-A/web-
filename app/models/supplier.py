from sqlalchemy import Column, Integer, String, DateTime,ForeignKey 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 
from app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True,nullable=False,index=True)
    contact = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    products = relationship("Product", back_populates="supplier")   
    