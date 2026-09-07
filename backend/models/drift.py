from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime
from backend.core.database import Base

class DriftFinding(Base):
    __tablename__ = "drift_findings"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True, nullable=False)
    site_id = Column(String, index=True, nullable=False)
    hostname = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    
    field_name = Column(String, nullable=False)
    baseline_value = Column(Text, nullable=True)
    current_value = Column(Text, nullable=True)
    change_type = Column(String, nullable=False) # MODIFIED, ADDED, REMOVED, MISSING
    
    severity = Column(String, index=True, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, index=True, nullable=False) # 0 to 100
    anomaly_score = Column(Float, default=0.0)
    
    authorization_status = Column(String, index=True, nullable=False) # Authorized, Unauthorized, Pending Approval, Expired Authorization, Mismatched Ticket
    ticket_id = Column(String, nullable=True)
    compliance_status = Column(String, nullable=False) # Compliant, Violation, N/A
    violated_rule_id = Column(String, nullable=True)
    
    evidence = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    
    status = Column(String, default="OPEN") # OPEN, ACKNOWLEDGED, RESOLVED, IGNORED
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ScanRun(Base):
    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, unique=True, index=True, nullable=False)
    devices_scanned = Column(Integer, default=0)
    findings_count = Column(Integer, default=0)
    unauthorized_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    status = Column(String, default="COMPLETED") # COMPLETED, FAILED, IN_PROGRESS
    initiated_by = Column(String, default="SYSTEM")
    created_at = Column(DateTime, default=datetime.utcnow)
