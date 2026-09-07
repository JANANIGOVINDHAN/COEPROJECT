from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.device import Device, Site
from backend.schemas.device import DeviceOut, SiteOut

router = APIRouter(tags=["Sites & Devices"])

@router.get("/sites", response_model=list[SiteOut])
def get_sites(db: Session = Depends(get_db)):
    return db.query(Site).all()

@router.get("/devices", response_model=list[DeviceOut])
def get_devices(site_id: str | None = None, device_type: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Device)
    if site_id:
        query = query.filter(Device.site_id == site_id)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    return query.all()

@router.get("/devices/{device_id}", response_model=DeviceOut)
def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")
    return device
