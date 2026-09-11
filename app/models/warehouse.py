from sqlalchemy import Column,Integer,ForeignKey,String,DateTime
from typing import Optional
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50),unique= True,nullable=False,index=True)
    address = Column(String(200),nullable= True)
    manager = Column(String(50),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    products = relationship("Product",back_populates="warehouse")