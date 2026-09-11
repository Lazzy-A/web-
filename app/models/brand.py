from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50),unique=True,nullable=False,index=True)
    logo = Column(String(200),nullable=True)
    description = Column(String(200),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default = func.now())
    products = relationship("Product",back_populates="brand")