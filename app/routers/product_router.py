from fastapi import APIRouter, Depends, HTTPException, status   
from app.database import get_db
from app.models.user import User
from app.routers.user_router import get_current_user
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductResponse
from sqlalchemy.orm import Session,joinedload
from typing import Optional

router = APIRouter(prefix="/products", tags=["商品管理"])

@router.get("/", response_model=list[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category_id : Optional[int] = None,   
    db: Session = Depends(get_db)
):
    # 查询商品，同时加载关联的分类
    query = db.query(Product).options(joinedload(Product.category))
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    products = query.offset(skip).limit(limit).all()
    # 手动构造返回列表，填充 category_name
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "tradename": p.tradename,
            "shop": p.shop,
            "price": p.price,
            "favourable": p.favourable,
            "stock": p.stock,
            "category_id": p.category_id,
            "category_name": p.category.name if p.category else None,  # ← 关键
            "created_at": p.created_at,
            "warn": "库存紧张" if p.stock < p.min_stock else None,
            "min_stock": p.min_stock    
        })
    return result

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id:int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品未找到")
    
    return {
        "id": product.id,
        "tradename": product.tradename,
        "shop": product.shop,
        "price": product.price,
        "favourable": product.favourable,
        "stock": product.stock,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "created_at": product.created_at,
        "min_stock": product.min_stock,
        "warn": "库存紧张" if product.stock < product.min_stock else None,

        
    }
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if product_data.category_id is not None:
        category = db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404,detail="分类不存在")
    # 创建商品
    new_product = Product(
        tradename=product_data.tradename,
        shop=product_data.shop,
        price=product_data.price,
        favourable=product_data.favourable,
        stock=product_data.stock,
        category_id = product_data.category_id,
        min_stock=product_data.min_stock    
    )
    # 将新商品添加到数据库
    db.add(new_product)         
    db.commit()
    db.refresh(new_product)  # 刷新以获取新商品的ID和创建时间   
    # 返回新创建的商品数据
    return new_product
@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品未找到")
    
    # 更新商品信息
    product.tradename = product_data.tradename
    product.shop = product_data.shop
    product.price = product_data.price
    product.favourable = product_data.favourable
    product.stock = product_data.stock
    product.category_id = product_data.category_id  
    product.min_stock = product_data.min_stock

    
    db.commit()
    db.refresh(product)
    
    return product