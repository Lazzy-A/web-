from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ =  "categories"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50),unique=True,index=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)
    description = Column(String(200), nullable=True)
    sort_order = Column(Integer,default=0)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    # children:查询这个分类的所有子类
    # parent:查询这个分类的父级分类
    children = relationship("Category",back_populates="parent")
    parent = relationship("Category",remote_side=[id],back_populates="children")

    products = relationship("Product", back_populates="category")