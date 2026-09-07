from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.inventory_log import InventoryLog
from app.models.user import User
from app.routers.user_router import get_current_user

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