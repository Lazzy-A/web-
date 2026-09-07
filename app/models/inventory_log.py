from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False,index=True)
    quantity = Column(Integer, nullable=False)  # 正数：入库，负数：出库
    type = Column(String(20), nullable=False)   # inbound, outbound, return, adjus
    note = Column(String(200),nullable=False)   # 备注  
    operator_id = Column(Integer,ForeignKey("users.id"),nullable=False) # 操作人
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    product = relationship("Product", back_populates="inventory_logs")
    operator = relationship("User", back_populates="inventory_logs")