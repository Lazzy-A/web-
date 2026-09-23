from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.user import User
from app.schemas.category import CategoryTree, CategoryCreate,CategoryResponse,CategoryUpdate
from sqlalchemy.orm import Session  
from app.routers.user_router import get_current_user
from app.services import category_services

router = APIRouter(prefix="/categories", tags=["分类管理"])

# 1.查询所有分类
@router.get("/",response_model=list[CategoryResponse])
def get_categories(skip: int = 0,limit:int=100,db:Session = Depends(get_db)):
    return category_services.get_categories(skip,limit,db)

@router.get("/tree", response_model=list[CategoryTree])
def get_category_tree(db:Session = Depends (get_db)):
    return category_services.get_category_tree(db)

# 2.查询单个分类详细
@router.get("/{category_id}",response_model=CategoryResponse)
def get_category(category_id:int,db:Session = Depends(get_db)):
    return category_services.get_category(category_id,db)

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return category_services.create_category(category_data,db,current_user)

@router.put("/{category_id}",response_model=CategoryResponse)
def update_category(category_id : int,category_data : CategoryUpdate, db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    return category_services.update_category(category_id,category_data,db,current_user)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id : int,db : Session=Depends(get_db),current_user : User=Depends(get_current_user)):
    return category_services.delete_categoy(category_id,db,current_user)