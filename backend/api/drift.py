from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.drift import DriftFinding
from backend.schemas.drift import DriftFindingOut, ScanRequest, ScanSummary
from backend.services.drift_detector import DriftDetectorService
from backend.services.finding_lifecycle import FindingLifecycleService

router = APIRouter(prefix="/drift", tags=["Drift Detection"])

drift_service = DriftDetectorService()

@router.post("/scan", response_model=ScanSummary)
def trigger_drift_scan(req: ScanRequest = ScanRequest(), db: Session = Depends(get_db)):
    """
    Triggers automated configuration drift scan across all hospital sites and devices.
    """
    result = drift_service.run_full_scan(db, initiated_by="API_SCAN_TRIGGER")
    return result

@router.get("/findings", response_model=list[DriftFindingOut])
def get_drift_findings(
    site_id: str | None = None,
    device_type: str | None = None,
    severity: str | None = None,
    authorization_status: str | None = None,
    compliance_status: str | None = None,
    status: str | None = None,
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(DriftFinding)
    if site_id:
        query = query.filter(DriftFinding.site_id == site_id)
    if device_type:
        query = query.filter(DriftFinding.device_type == device_type)
    if severity:
        query = query.filter(DriftFinding.severity == severity)
    if authorization_status:
        query = query.filter(DriftFinding.authorization_status == authorization_status)
    if compliance_status:
        query = query.filter(DriftFinding.compliance_status == compliance_status)
    if status:
        query = query.filter(DriftFinding.status == status)

    return query.order_by(DriftFinding.risk_score.desc()).limit(limit).all()

@router.get("/findings/{finding_id}", response_model=DriftFindingOut)
def get_finding_by_id(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(DriftFinding).filter(DriftFinding.finding_id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{finding_id}' not found")
    return finding

@router.patch("/findings/{finding_id}/status", response_model=DriftFindingOut)
def update_finding_status(
    finding_id: str,
    status: str = Body(..., embed=True),
    notes: str | None = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """
    Phase 2: Updates lifecycle status of a drift finding (OPEN, ACKNOWLEDGED, IN_PROGRESS, REMEDIATED, EXEMPTED).
    """
    try:
        updated = FindingLifecycleService.update_finding_status(db, finding_id, status, notes=notes)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/findings/{finding_id}/remediate")
def remediate_finding(finding_id: str, db: Session = Depends(get_db)):
    """
    Phase 2: Executes automated fix simulation to remediate the selected configuration drift.
    """
    try:
        res = FindingLifecycleService.execute_remediation_action(db, finding_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
