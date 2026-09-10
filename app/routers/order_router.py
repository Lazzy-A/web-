from fastapi import APIRouter, Depends, HTTPException, status   
from app.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse,OrderStatusUpdate
from sqlalchemy.orm import Session  
from app.routers.user_router import get_current_user
from app.routers.inventory_router import InventoryLog

router = APIRouter(prefix="/orders", tags=["订单管理"])

def get_and_validate_order(
    order_id: int,
    db: Session,
    current_user: User
) -> Order:
    """查询订单并校验归属和状态（只允许操作 pending 状态的订单）"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单未找到")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作此订单")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="只有待处理状态的订单可以操作")
    return order

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    # 1. 查询商品
    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 2. 检查库存
    if product.stock < order_data.quantity:
        raise HTTPException(status_code=400, detail="库存不足")

    # 3. 扣库存、计算总价
    product.stock -= order_data.quantity
    total_price = product.price * order_data.quantity
        # 创建商品
    new_order = Order(
        user_id=current_user.id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price,
        status="pending"
    )
    # 将订单添加到数据库
    db.add(new_order)         
    db.commit()
    db.refresh(new_order)  # 刷新以获取新商品的ID和创建时间   
    # 返回新创建的商品数据
    return new_order

@router.get("/", response_model=list[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders(skip:int=0, limit:int=10, db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id==current_user.id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders
@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order(order_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    order = get_and_validate_order(order_id,db,current_user)
    return order

@router.put("/{order_id}/status", response_model=OrderResponse)
def updata_order_status(order_id:int,status_data:OrderStatusUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    order = get_and_validate_order(order_id,db,current_user)
    if status_data.status not in["completed", "cancelled"]:
        raise HTTPException(status_code=400,detail="无效状态")
    if status_data.status ==  "cancelled":
        product = db.query(Product).filter(Product.id == order.product_id).first()
        if not product:
            raise HTTPException(status_code=404,detail="商品不存在")
        product.stock +=order.quantity
        log = InventoryLog(
            product_id = product.id,
            quantity = order.quantity,
            type = "return",
            note = f"订单 {order.id} 取消，恢复库存",
            order_id = order.id,
            operator_id = current_user.id
        )
        db.add(log)
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(oder_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id==oder_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="订单未找到")
    if order.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="无权操作此订单")
    if order.status!="pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="只有待处理状态的订单可以删除")
    db.delete(order)
    db.commit()
    return {"message": "订单已删除"}

    