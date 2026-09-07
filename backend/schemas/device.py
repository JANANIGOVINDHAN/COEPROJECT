from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SiteOut(BaseModel):
    id: int
    site_id: str
    name: str
    code: str
    criticality: float
    location: Optional[str] = None

    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    device_id: str
    hostname: str
    site_id: str
    site_name: Optional[str] = None
    device_type: str
    network_zone: str
    ip_address: str
    mac_address: Optional[str] = None
    firmware_version: Optional[str] = None
    status: str = "ONLINE"

class DeviceCreate(DeviceBase):
    pass

class DeviceOut(DeviceBase):
    id: int
    last_scanned: Optional[datetime] = None

    class Config:
        from_attributes = True
