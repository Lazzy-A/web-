from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.inventory_log import InventoryLog
from app.models.user import User
from app.schemas.inventory_log import InventoryLogResponse
from app.routers.user_router import get_current_user
from typing import Optional
from datetime import datetime   
def parse_date(date_str : str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


router = APIRouter(prefix="/inventory", tags=["库存管理"])

@router.post("/in", status_code=201)
def inbound(barcode : str,quantity : int = 0,tradename : str = None,shop : str =None,price : float = None,favourable : str = None,note : str = "",db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    if quantity <=0:
        raise HTTPException(status_code=400,detail="入库数量必须大于0")

    # 1.根据条形码查找商品
    product = db.query(Product).filter(Product.barcode == barcode).first()

    # 2.商品不存在，检查是否提供了创建信息
    if not product:
        if not tradename or price is None:
            raise HTTPException(status_code=404, detail="商品不存在，请提供商品名称和价格以创建新商品")

    # 创建新商品
    product = Product(
        barcode = barcode,
        tradename = tradename,
        shop = shop or "未指定店铺",
        price = price,
        favourable = favourable,
        stock = 0 
    )
    db.add(product)
    db.flush()
    # 2.增加库存
    product.stock += quantity

    # 3.记录库存流水
    log = InventoryLog(
        product_id = product.id,
        quantity = quantity,
        type = "inbound",
        note = note,
        operator_id = current_user.id
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {
        "message": "入库成功",
        "product_id": product.id,
        "barcode": product.barcode,
        "tradename": product.tradename,
        "new_stock": product.stock,
        "log_id": log.id
    }
@router.get("/log", response_model=list[InventoryLogResponse] )
def get_log(product_id : int | None=None,start_date : str | None=None,end_date : str | None=None,skip:int =0,limit: int =100,db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    query = db.query(InventoryLog)  
    if product_id:
        query = query.filter(InventoryLog.product_id == product_id)
    if start_date:
            start_date = parse_date(start_date)
            query = query.filter(InventoryLog.created_at >= start_date)
    if end_date:
                end_date = parse_date(end_date)
                query = query.filter(InventoryLog.created_at <= end_date)
    logs = query.order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit).all()
    reslut = []
    for log in logs:
        reslut.append({
            "id": log.id,
            "product_id": log.product_id,
            "product_name": log.product.tradename if log.product else None,
            "quantity": log.quantity,
            "type": log.type,
            "note": log.note,
            "operator": log.operator.username if log.operator else None,
            "created_at": log.created_at,
           
        })

    return reslut
            
            