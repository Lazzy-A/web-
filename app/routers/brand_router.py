from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.brand import Brand
from app.routers.user_router import get_current_user
from app.schemas.brand import BrandCreate,BrandResponse,BrandUpdate
from app.services import brand_services

router = APIRouter(prefix="/brands",tags=["品牌管理"])

@router.get("/",response_model=list[BrandResponse])
def get_brands(db:Session= Depends(get_db),skip:int=0,limit:int=100):
    return brand_services.get_brands(db,skip,limit)
@router.get("/{brands_id}",response_model=BrandResponse)
def get_brand(brands_id:int,db:Session=Depends(get_db)):
    return brand_services.get_brand(brands_id,db)
@router.post("/",response_model=BrandResponse)
def created_brand(brand_data : BrandCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return brand_services.created_brand(brand_data,db,current_user)
@router.put("/{brand_id}",response_model=BrandResponse)
def updata_brand(brand_id : int,brand_data : BrandUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return brand_services.updata_brand(brand_id,brand_data,db,current_user)
@router.delete("/{brand_id}",status_code=204)
def delete_brand(brand_id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    return brand_services.delete_brand(brand_id,db,current_user)