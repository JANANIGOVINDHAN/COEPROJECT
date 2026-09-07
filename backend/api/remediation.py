from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.drift import DriftFinding
from backend.services.remediation_engine import RemediationEngineService

router = APIRouter(prefix="/remediation", tags=["Remediation"])

@router.get("/{finding_id}")
def get_remediation_for_finding(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(DriftFinding).filter(DriftFinding.finding_id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    remed = RemediationEngineService.get_remediation(finding.field_name, finding.current_value)
    return {
        "finding_id": finding.finding_id,
        "device_id": finding.device_id,
        "hostname": finding.hostname,
        "field_name": finding.field_name,
        "severity": finding.severity,
        "risk_score": finding.risk_score,
        "remediation_details": remed
    }
