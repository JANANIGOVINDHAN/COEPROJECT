from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from backend.core.database import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    criticality = Column(Float, default=0.75) # 0.0 to 1.0
    location = Column(String, nullable=True)

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    hostname = Column(String, index=True, nullable=False)
    site_id = Column(String, ForeignKey("sites.site_id"), index=True, nullable=False)
    site_name = Column(String, nullable=True)
    device_type = Column(String, nullable=False) # Core Router, Firewall, Switch, etc.
    network_zone = Column(String, nullable=False) # Clinical, Guest, Medical IoT, etc.
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=True)
    firmware_version = Column(String, nullable=True)
    status = Column(String, default="ONLINE")
    last_scanned = Column(DateTime, default=datetime.utcnow)
