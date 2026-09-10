from fastapi import APIRouter,Depends,HTTPException,status
from app.database import get_db
from app.models.user import User
from app.schemas.supplier import SupplierCreate,SupplierResponse,SupplierUpdate
from app.routers.user_router import get_current_user    
from sqlalchemy.orm import Session
from app.models.supplier import Supplier

router = APIRouter(
    prefix="/suppliers",
    tags=["供应商管理"])

@router.get("/",response_model=list[SupplierResponse])
def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.get("/{supplier_id}",response_model=SupplierResponse)
def get_supplier(supplier_id:int,db:Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="供应商不存在")
    return supplier 

@router.post("/",response_model=SupplierResponse,status_code=status.HTTP_201_CREATED)
def create_supplier(supplier_data:SupplierCreate,db:Session = Depends(get_db),_current_user:User = Depends(get_current_user)):
    query = db.query(Supplier).filter(Supplier.name == supplier_data.name)
    if query.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="供应商已存在")
    new_supplier = Supplier(
        name=supplier_data.name,
        phone=supplier_data.phone,
        address=supplier_data.address,
        contact=supplier_data.contact,
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

@router.put("/{supplier_id}",response_model=SupplierResponse)
def update_supplier(
    supplier_id:int,
    supplier_data:SupplierUpdate,
    db:Session = Depends(get_db),
    _current_user:User = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()    
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="供应商不存在")
    if supplier_data.name is not None:
        supplier.name = supplier_data.name
    if supplier_data.contact is not None:
        supplier.contact = supplier_data.contact
    if supplier_data.phone is not None:
        supplier.phone = supplier_data.phone
    if supplier_data.address is not None:
        supplier.address = supplier_data.address

    db.commit()
    db.refresh(supplier)
    return supplier
@router.delete("/{supplier_id}", status_code=status.HTTP_200_OK)
def delete_supplier(
    supplier_id:int,
    db:Session = Depends(get_db),
    _current_user:User = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="供应商不存在")
    db.delete(supplier)     
    db.commit()
    return {"message": "供应商已删除"}
