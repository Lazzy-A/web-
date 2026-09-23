from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import HTTPException,status
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.models.category import Category

async def get_products(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100, 
):
    # 查询商品，同时加载关联的分类
    query = select(Product).options(joinedload(Product.category))
    query = query.filter(Product.status == "online")
    query = query.offset(skip).limit(limit)
    db_result = await db.execute(query)
    products = db_result.scalars().all()
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
            "min_stock": p.min_stock,
            "status": p.status, 
        })
    return result
async def get_product(db: AsyncSession,product_id:int):
    stmt = select(Product).options(joinedload(Product.category)).filter(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    if product.status == "offline":
        raise HTTPException(status_code=404, detail="商品不存在")
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
        "status": product.status,
        "warn": "库存紧张" if product.stock < product.min_stock else None   
    }

async def create_product(db: AsyncSession,product_data: ProductCreate):
    if product_data.category_id is not None:
        stmt = select(Category).filter(Category.id == product_data.category_id)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()
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
    await db.commit()
    await db.refresh(new_product)  # 刷新以获取新商品的ID和创建时间   
    # 返回新创建的商品数据
    return new_product

async def update_product(db: AsyncSession,product_id: int, product_data: ProductCreate):
    query = select(Product).filter(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="商品未找到")
    # 更新商品信息
    product.tradename = product_data.tradename
    product.shop = product_data.shop
    product.price = product_data.price
    product.favourable = product_data.favourable
    product.stock = product_data.stock
    product.category_id = product_data.category_id  
    product.min_stock = product_data.min_stock
    await db.commit()
    await db.refresh(product)
    return product
async def  online_product(db:AsyncSession,product_id:int):
    query = select(Product).filter(Product.id==product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none() 

    if not product:
        raise HTTPException(status_code=404,detail="商品不存在")
    if product.status == "online":
        raise HTTPException(status_code=400,detail="商品已上架")
    product.status = "online"
    await db.commit()
    await db.refresh(product)
    return product
async def  offline_product(db:AsyncSession,product_id:int):
    query = select(Product).filter(Product.id==product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none() 

    if not product:
        raise HTTPException(status_code=404,detail="商品不存在")
    if product.status == "offline":
        raise HTTPException(status_code=400,detail="商品已下架")
    product.status = "offline"
    await db.commit()
    await db.refresh(product)
    return product