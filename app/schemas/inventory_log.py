from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InventoryLog(BaseModel):
    id: int
    product_id: int
    product_name: str   
    quantity: int
    type: str
    note: str | None = None
    operator: str
    created_at: datetime

    class Config:
        from_attributes = True

class InventoryLogResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    type: str
    note: Optional[str] = None
    operator: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True