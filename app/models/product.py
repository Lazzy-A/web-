from sqlalchemy import Column, Integer,Float, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(20),unique=True,index=True,nullable=True)
    tradename = Column(String(100), nullable=False)
    shop = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    favourable = Column(String(100), nullable=True)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer,ForeignKey("categories.id",onupdate="SET NULL"),nullable=True,index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    category = relationship("Category", back_populates="products")
    inventory_logs = relationship("InventoryLog", back_populates="product")
