from pydantic import BaseModel,field_serializer
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    tradename: str
    shop: str
    price: float
    favourable: Optional[str] = None
    stock: int
    category_id : Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    tradename: str
    shop: str
    price: float
    favourable: Optional[str] =None
    stock: int
    category_id : Optional[int] = None
    category_name : Optional[str] = None
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self,dt:datetime,_info):
        return dt.isoformat()

    class Config:
        from_attributes = True
