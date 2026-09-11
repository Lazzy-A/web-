from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.brand import Brand
from app.routers.user_router import get_current_user
from app.schemas.brand import BrandCreate,BrandResponse,BrandUpdate

router = APIRouter(prefix="/brands",tags=["品牌管理"])

@router.get("/",response_model=list[BrandResponse])
def get_brands(skip:int = 0,limit:int = 100,db:Session = Depends(get_db)):
    brands = db.query(Brand).offset(skip).limit(limit).all()
    return brands

@router.get("/{brands_id}",response_model=BrandResponse)
def get_brand(
    brands_id:int,
    db:Session=Depends(get_db)
):

    brand = db.query(Brand).filter(Brand.id==brands_id).first()
    if not brand :
        raise HTTPException(status_code=404,detail="该品牌不存在")
    return brand

@router.post("/",response_model=BrandResponse)
def created_brand(brand_data : BrandCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    existing = db.query(Brand).filter(Brand.name ==brand_data.name).first()
    if existing:
          raise HTTPException(status_code=400, detail="品牌名称已存在")
    new_brand = Brand(
        name = brand_data.name,
        logo = brand_data.logo,
        description = brand_data.description
    )
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand

@router.put("/{brand_id}",response_model=BrandResponse)
def updata_brand(brand_id : int,brand_data : BrandUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404,detail="该品牌不存在")
    if brand_data.name is not None:
        brand.name = brand_data.name
    if brand_data.logo is not None:
        brand.logo = brand_data.logo
    if brand_data.description is not None:
        brand.description = brand_data.description
    db.commit()
    db.refresh(brand)
    return brand

@router.delete("/{brand_id}",status_code=204)
def delete_brand(brand_id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
            raise HTTPException(status_code=404,detail="该商品不存在")
    db.delete(brand)
    db.commit()
    return None