from fastapi import HTTPException
from app.models.product import Product
from app.models.user import User
from app.models.inventory_log import InventoryLog
from app.schemas.inventory_check import InventoryCheckCreate
from app.models.inventory_check import InventoryCheck
from sqlalchemy.orm import Session
from datetime import datetime
def parse_date(date_str : str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")
def inbound(barcode : str,quantity : int,tradename : str,shop : str,price : float,favourable : str,note : str,db : Session,current_user : User):
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
def get_log(product_id : int,start_date : str,end_date : str,skip:int,limit: int,db : Session,current_user : User):
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
def check_inventory(check_data:InventoryCheckCreate ,db:Session,current_user:User):
     product_id = check_data.product_id
     actual_stock = check_data.actual_stock
     product = db.query(Product).filter(Product.id == product_id).first()
     if not product:
          raise HTTPException(status_code=404,detail="商品不存在")
     difference = actual_stock - product.stock
     if difference == 0:
        raise HTTPException(status_code=400,detail="库存无变化")
     old_stock = product.stock
     product.stock = actual_stock
     check = InventoryCheck(
          product_id = product.id,
          old_stock = old_stock,
          new_stock = check_data.actual_stock,
          difference = difference,
          operator_id = current_user.id,
          note = check_data.note
     )
     db.add(check)

     log = InventoryLog(
          product_id = product.id,
          quantity = difference,
          type = "gain" if difference > 0 else "loss",
          note = f"盘点：{check_data.note or ''}",
          operator_id = current_user.id
     )
     db.add(log)
     db.commit()
     db.refresh(check)

     return {
        "id": check.id,
        "product_id": product.id,
        "product_name": product.tradename,
        "old_stock": check.old_stock,
        "new_stock": check.new_stock,
        "difference": check.difference,
        "operator": current_user.username,
        "note": check.note,
        "created_at": check.created_at
    }
