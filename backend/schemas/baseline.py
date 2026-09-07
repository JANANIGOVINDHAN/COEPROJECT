from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaselineCreate(BaseModel):
    name: str
    device_type: str
    site_id: Optional[str] = None
    approved_config_json: str
    approved_by: str = "Admin"

class BaselineOut(BaseModel):
    id: int
    baseline_id: str
    name: str
    device_type: str
    site_id: Optional[str] = None
    version: int
    status: str
    approved_config_json: str
    approved_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
