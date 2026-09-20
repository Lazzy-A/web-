from fastapi import APIRouter, Depends, status   
from app.database import get_async_db
from app.schemas.product import ProductResponse,ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.services import product_service

router = APIRouter(prefix="/products", tags=["商品管理"])

@router.get("/", response_model=list[ProductResponse])
async def get_products(
     db:AsyncSession = Depends(get_async_db),
    skip:int = 0,
    limit:int = 100,
    category_id : Optional[int] = None,
):
    return await product_service.get_products(db,skip,limit,category_id)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    return await product_service.get_product(db, product_id)
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data:ProductCreate,
    db:AsyncSession=Depends(get_async_db),
    ):
    return await product_service.create_product(db,product_data)

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product_id : int,
    product_data:ProductCreate,
    db: AsyncSession = Depends(get_async_db),
):
    return await product_service.update_product(db, product_id,product_data)
@router.put("/{product_id}/online",response_model=ProductResponse)
async def online_product(
    product_id : int,
    db:AsyncSession=Depends(get_async_db),
):
    return await product_service.online_product(db,product_id)
@router.put("/{product_id}/offline",response_model=ProductResponse)
async def offline_product(
    product_id : int,
    db:AsyncSession=Depends(get_async_db),
):
    return await product_service.offline_product(db,product_id)