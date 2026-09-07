from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DriftFindingOut(BaseModel):
    id: int
    finding_id: str
    device_id: str
    site_id: str
    hostname: str
    device_type: str
    field_name: str
    baseline_value: Optional[str] = None
    current_value: Optional[str] = None
    change_type: str
    severity: str
    risk_score: float
    anomaly_score: float
    authorization_status: str
    ticket_id: Optional[str] = None
    compliance_status: str
    violated_rule_id: Optional[str] = None
    evidence: str
    recommended_action: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ScanRequest(BaseModel):
    site_id: Optional[str] = None
    device_id: Optional[str] = None

class ScanSummary(BaseModel):
    scan_id: str
    devices_scanned: int
    findings_count: int
    unauthorized_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    status: str
