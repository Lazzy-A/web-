from pydantic import BaseModel,field_serializer
from typing import Optional
from datetime import datetime

class SupplierCreate(BaseModel):
    name: str
    contact: Optional[str] = None
    phone: Optional[str] =  None
    address: Optional[str]= None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime

    @field_serializer("created_at")
    def serialize_dt(self,dt:datetime,_info):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    class Config:
        ormfrom_attributes_mode = True
    
    