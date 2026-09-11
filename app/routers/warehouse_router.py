from fastapi import APIRouter,Depends,HTTPException,status
from app.database import get_db
from app.models.user import User
from app.routers.user_router import get_current_user
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate,WarehouseResponse,WarehouseUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/warehouses", tags=["仓库管理"])

@router.get("/",response_model=list[WarehouseResponse])
def get_warehouses(skip:int = 0,limit:int = 100,db:Session=Depends(get_db)):
    warehouses = db.query(Warehouse).offset(skip).limit(limit).all()
    return warehouses
@router.get("/{warehouse_id}",response_model=WarehouseResponse)
def get_warehouse(warehouse_id:int,db:Session=Depends(get_db)):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404,detail="仓库不存在")
    return warehouse
@router.post("/",response_model=WarehouseResponse,status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse_data:WarehouseCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    existing = db.query(Warehouse).filter(Warehouse.name == warehouse_data.name).first()
    if existing:
        raise HTTPException(status_code=400,detail="仓库已存在")
    new_warehouse = Warehouse(
        name = warehouse_data.name,
        address = warehouse_data.address,
        manager = warehouse_data.manager
    )
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

@router.put("/{warehouse_id}",response_model=WarehouseResponse)
def update_warehouse(warehouse_id:int,warehouse_data:WarehouseUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404,detail="仓库不存在")
    if warehouse_data.name is not None:
        warehouse.name = warehouse_data.name
    if warehouse_data.address is not None:
            warehouse.address = warehouse_data.address
    if warehouse_data.manager is not None:
            warehouse.manager = warehouse_data.manager
    db.commit()
    db.refresh(warehouse)
    return warehouse

@router.delete("/{warehouse_id}",status_code=204)
def delete_warehouse(warehouse_id : int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
     warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
     if not warehouse:
             raise HTTPException(status_code=404,detail="仓库不存在")
     db.delete(warehouse)
     db.commit()
     return None