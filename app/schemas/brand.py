from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandCreate(BaseModel):
    name : str
    logo : Optional[str] = None
    description : Optional[str] = None

class BrandUpdate(BaseModel):
    name : Optional[str] = None
    logo : Optional[str] = None
    description : Optional[str] = None

class BrandResponse(BaseModel):
    id : int 
    name : str
    logo : Optional[str] = None
    description : Optional[str] = None
    created_at : datetime

    class Config:
        from_attributes = True