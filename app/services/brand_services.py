from app.models.brand import Brand
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.brand import BrandCreate,BrandUpdate
from app.models.user import User

def get_brands(db:Session,skip:int,limit:int):
    brands = db.query(Brand).offset(skip).limit(limit).all()
    return brands

def get_brand(
    brands_id:int,
    db:Session
):

    brand = db.query(Brand).filter(Brand.id==brands_id).first()
    if not brand :
        raise HTTPException(status_code=404,detail="该品牌不存在")
    return brand

def created_brand(brand_data : BrandCreate,db:Session,current_user:User):
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

def updata_brand(brand_id : int,brand_data : BrandUpdate,db:Session,current_user:User):
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

def delete_brand(brand_id:int,db:Session,current_user:User):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
            raise HTTPException(status_code=404,detail="该品牌不存在")
    db.delete(brand)
    db.commit()
    return None
