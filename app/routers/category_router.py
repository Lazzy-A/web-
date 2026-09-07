from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryTree, CategoryCreate,CategoryResponse,CategoryUpdate
from sqlalchemy.orm import Session  
from app.routers.user_router import get_current_user
from sqlalchemy import func
from app.models.product import Product

router = APIRouter(prefix="/categories", tags=["分类管理"])

# 1.查询所有分类
@router.get("/",response_model=list[CategoryResponse])
def get_categories(skip: int = 0,limit:int=100,db:Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.get("/tree", response_model=list[CategoryTree])
def get_category_tree(db:Session = Depends (get_db)):
    #   查询所有顶级分类（parent_id 为 None）
    root_categories = db.query(Category).filter(Category.parent_id.is_(None)).order_by(Category.sort_order.desc()).all()
    # 递归构建树结构
    def build_tree(category:Category) -> dict:
         # 查询当前分类的所有子分类
         children = db.query(Category).filter(Category.parent_id == category.id).order_by(Category.sort_order.desc()).all()
         return {
            "id": category.id,
            "name": category.name,
            "parent_id": category.parent_id,
            "description": category.description,
            "sort_order": category.sort_order,
            "created_at": category.created_at,
            "children": [build_tree(child) for child in children]
        }
    # 对每个顶级分类构建树
    return [build_tree(root) for root in root_categories ]

# 2.查询单个分类详细
@router.get("/{category_id}",response_model=CategoryResponse)
def get_category(category_id:int,db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404,detail="分类不存在")
    # 统计分类下的商品数量
    product_count = db.query(func.count(Product.id)).filter(Product.category_id == category_id).scalar()
    # 构造返回数据（手动填充 product_count）
    return {
        "id": category.id,
        "name": category.name,
        "parent_id": category.parent_id,
        "description": category.description,
        "sort_order": category.sort_order,
        "created_at": category.created_at,
        "product_count": product_count or 0   # 如果为 None，默认 0
    }

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    # 1. 校验：同一父级下不能有重名分类
    exiting = db.query(Category).filter(Category.name == category_data.name,Category.parent_id == category_data.parent_id).first()
    if exiting:
        raise HTTPException(status_code=400, detail="该分类在此父级下已存在")

    # 2. 检查父级是否存在
    if category_data.parent_id is not None:
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="父级分类不存在")
    # 3.创建新分类对象保存
    new_category = Category(
        name=category_data.name,
        parent_id=category_data.parent_id,
        description=category_data.description,
        sort_order=category_data.sort_order or 0
    )
    # 将分类添加到数据库
    db.add(new_category)         
    db.commit()
    db.refresh(new_category)    
    # 返回新创建的商品数据
    return new_category

@router.put("/{category_id}",response_model=CategoryResponse)
def update_category(
    category_id : int,
    category_data : CategoryUpdate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    # 1.查询更新的分类是否存在
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404,detail="分类不存在")

    # 2.检查同一父级是否重名
    if category_data.name is not None:
        exisiting = db.query(Category).filter(
            Category.name == category_data.name,
            Category.parent_id == category_data.parent_id,
            Category.id != category_id
        ).first()
        if exisiting:
            raise HTTPException(status_code=400,detail="该名称在此父级下已存在")

    # 3.检验父级合法性
    if category_data.parent_id is not None:
        if category_data.parent_id == category_id:
            raise HTTPException(status_code=400, detail="不能将自身设为父级")
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404,detail="父级分类不存在")
    # 如果父级的父级链条中包含了当前分类，则拒绝
    def is_ancestor(cat_id,target_id):
        while cat_id is not None:
            if cat_id == target_id:
                return True

            parent_obj = db.query(Category).filter(Category.id == cat_id).first()
            cat_id = parent_obj.parent_id if parent_obj else None
            return False

    if is_ancestor(category_data.parent_id,category_id):
        raise HTTPException(status_code=400,detail="不能将父级设为自身的子级")

    # 4.更新字段
    if category_data.name is not None:
        category.name = category_data.name

    if category_data.parent_id is not None:
        category.parent_id = category_data.parent_id

    if category_data.description is not None:
        category.description = category_data.description

    if category_data.sort_order is not None:
        category.sort_order = category_data.sort_order

    # 5.更新数据库
    db.commit   
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
def delete_categoy(
        category_id : int,
        db : Session = Depends(get_db),
        current_user : User =Depends(get_current_user)
):
    # 1.查询删除的分类是否存在
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404,detail="分类不存在")

    # 2.检查该分类下是否有子级
    children = db.query(Category).filter(Category.parent_id == category_id).all()
    if children:
        pass

    # 3.执行删除
    db.delete(category)
    db.commit()

    return None