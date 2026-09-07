from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

# 创建分类时，前端传什么
class CategoryCreate(BaseModel):
    name:str
    parent_id:Optional[int]=None  # 默认顶级分类
    description : Optional[str] = None
    sort_order: Optional[int] = 0

#  更新分类时，前端传什么
class CategoryUpdate(BaseModel):
    name:Optional[str] = None
    parent_id : Optional[int] = None
    description : Optional[str] =None
    sort_order : Optional[int] = None

# 查询单个分类是，后端传什么
class CategoryResponse(BaseModel):
    id : int
    name : str
    parent_id : Optional[int] = None
    description : Optional[str] = None
    sort_order : int
    created_at : datetime
    product_count : int = 0

    class Config:
        from_attributes = True

# 查询分类树时，每个节点需要包含子节点列表
class CategoryTree(BaseModel):
    id : int
    name : str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    sort_order: int
    created_at: datetime
    children : List['CategoryTree'] = []  # 子分类列表，递归结构
    product_count: int = 0   # 新增

    class Config:
        from_attributes =True

# 解决递归分类类型引用问题
CategoryTree.model_rebuild()