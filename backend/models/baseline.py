from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.core.database import Base

class Baseline(Base):
    __tablename__ = "baselines"

    id = Column(Integer, primary_key=True, index=True)
    baseline_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False, index=True) # Firewall, Switch, etc.
    site_id = Column(String, nullable=True, index=True) # Null for global type baseline
    version = Column(Integer, default=1)
    status = Column(String, default="APPROVED") # APPROVED, DRAFT, PROPOSED, ARCHIVED
    
    # Approved baseline values stored as JSON text
    approved_config_json = Column(Text, nullable=False)
    
    approved_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BaselineVersion(Base):
    __tablename__ = "baseline_versions"

    id = Column(Integer, primary_key=True, index=True)
    baseline_id = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    approved_config_json = Column(Text, nullable=False)
    changed_by = Column(String, nullable=False)
    change_reason = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
