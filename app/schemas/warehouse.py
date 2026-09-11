from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WarehouseCreate(BaseModel):
    name : str
    address:Optional[str] = None
    manager:Optional[str] = None

class WarehouseUpdate(BaseModel):
    name:Optional[str] = None
    address:Optional[str] = None
    manager:Optional[str] = None

class WarehouseResponse(BaseModel):
    id:int
    name:str
    address:Optional[str] = None
    manager:Optional[str] = None
    created_at:datetime
    class Config:
        from_attributes = True