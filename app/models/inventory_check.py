from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class InventoryCheck(Base):
    __tablename__ = "inventory_checks"
    id = Column(Integer,primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey("products.id"),index=True,nullable=False)
    old_stock = Column(Integer,nullable=False)
    new_stock = Column(Integer,nullable = False)
    difference = Column(Integer,nullable=False)
    operator_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    note = Column(String(200),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    product = relationship("Product",back_populates="inventory_checks")