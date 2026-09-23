from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.inventory_log import InventoryLogResponse
from app.schemas.inventory_check import InventoryCheckCreate,InventoryCheckResponse
from app.routers.user_router import get_current_user
from app.services import inventory_services



router = APIRouter(prefix="/inventory", tags=["库存管理"])

@router.post("/in", status_code=201)
def inbound(barcode : str,quantity : int = 0,tradename : str = None,shop : str =None,price : float = None,favourable : str = None,note : str = "",db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
   return inventory_services.inbound(barcode,quantity,tradename,shop,price,favourable,note,db,current_user)
@router.get("/log", response_model=list[InventoryLogResponse] )
def get_log(product_id : int | None=None,start_date : str | None=None,end_date : str | None=None,skip:int =0,limit: int =100,db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    return inventory_services.get_log(product_id,start_date,end_date,skip,limit,db,current_user)

@router.post("/check",response_model=InventoryCheckResponse)
def check_inventory(check_data:InventoryCheckCreate ,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return inventory_services.check_inventory(check_data,db,current_user)