from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.configuration import Configuration
from backend.schemas.configuration import ConfigurationOut

router = APIRouter(prefix="/configurations", tags=["Configurations"])

@router.get("", response_model=list[ConfigurationOut])
def get_configurations(device_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Configuration)
    if device_id:
        query = query.filter(Configuration.device_id == device_id)
    return query.order_by(Configuration.configuration_timestamp.desc()).limit(limit).all()

@router.get("/{id}", response_model=ConfigurationOut)
def get_configuration_by_id(id: int, db: Session = Depends(get_db)):
    cfg = db.query(Configuration).filter(Configuration.id == id).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="Configuration record not found")
    return cfg
