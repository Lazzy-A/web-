from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
class InventoryCheckCreate(BaseModel):
    product_id:int
    actual_stock:int
    note : Optional[str] = None

class InventoryCheckResponse(BaseModel):
    id : int
    product_id : int 
    product_name : Optional[str] = None
    old_stock : int 
    new_stock : int 
    difference : int
    operator : Optional[str] = None
    note : Optional[str] = None
    created_at : datetime

    class Config:
        from_attributes = True

