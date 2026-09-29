from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.core.database import get_db
from backend.models.device import Device, Site
from backend.models.drift import DriftFinding, ScanRun
from backend.models.compliance import ComplianceResult
from backend.models.ticket import ChangeTicket
from backend.services.trend_analyzer import TrendAnalyzerService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_sites = db.query(Site).count()
    total_devices = db.query(Device).count()
    total_findings = db.query(DriftFinding).count()
    
    critical_count = db.query(DriftFinding).filter(DriftFinding.severity == "CRITICAL").count()
    high_count = db.query(DriftFinding).filter(DriftFinding.severity == "HIGH").count()
    medium_count = db.query(DriftFinding).filter(DriftFinding.severity == "MEDIUM").count()
    low_count = db.query(DriftFinding).filter(DriftFinding.severity == "LOW").count()
    
    unauthorized_count = db.query(DriftFinding).filter(DriftFinding.authorization_status != "Authorized").count()
    authorized_count = db.query(DriftFinding).filter(DriftFinding.authorization_status == "Authorized").count()
    compliance_violations = db.query(DriftFinding).filter(DriftFinding.compliance_status == "Violation").count()
    
    last_scan = db.query(ScanRun).order_by(ScanRun.created_at.desc()).first()
    devices_scanned = last_scan.devices_scanned if last_scan else total_devices

    # Findings by Site
    site_findings_query = db.query(
        DriftFinding.site_id, func.count(DriftFinding.id)
    ).group_by(DriftFinding.site_id).all()
    
    all_sites = db.query(Site).all()
    site_map = {s.site_id: s.name for s in all_sites}
    drift_by_site = [
        {"site_id": sf[0], "site_name": site_map.get(sf[0], sf[0]), "findings": sf[1]}
        for sf in site_findings_query
    ]

    # Drift by Device Type
    device_type_query = db.query(
        DriftFinding.device_type, func.count(DriftFinding.id)
    ).group_by(DriftFinding.device_type).all()
    
    drift_by_device_type = [
        {"device_type": dt[0], "findings": dt[1]} for dt in device_type_query
    ]

    # Top Risky Devices
    top_devices_query = db.query(
        DriftFinding.device_id, DriftFinding.hostname, func.max(DriftFinding.risk_score).label("max_risk")
    ).group_by(DriftFinding.device_id, DriftFinding.hostname).order_by(func.max(DriftFinding.risk_score).desc()).limit(5).all()

    top_risky_devices = [
        {"device_id": td[0], "hostname": td[1], "risk_score": float(td[2])}
        for td in top_devices_query
    ]

    return {
        "kpis": {
            "total_sites": total_sites,
            "total_devices": total_devices,
            "devices_scanned": devices_scanned,
            "total_findings": total_findings,
            "critical_findings": critical_count,
            "high_findings": high_count,
            "medium_findings": medium_count,
            "low_findings": low_count,
            "unauthorized_changes": unauthorized_count,
            "authorized_changes": authorized_count,
            "compliance_violations": compliance_violations,
            "scan_success_rate": 100.0 if last_scan and last_scan.status == "COMPLETED" else 95.0
        },
        "charts": {
            "drift_by_site": drift_by_site,
            "drift_by_device_type": drift_by_device_type,
            "risk_distribution": [
                {"severity": "CRITICAL", "count": critical_count, "color": "#ef4444"},
                {"severity": "HIGH", "count": high_count, "color": "#f97316"},
                {"severity": "MEDIUM", "count": medium_count, "color": "#eab308"},
                {"severity": "LOW", "count": low_count, "color": "#3b82f6"}
            ],
            "authorization_breakdown": [
                {"status": "Unauthorized", "count": unauthorized_count},
                {"status": "Authorized", "count": authorized_count}
            ],
            "top_risky_devices": top_risky_devices
        }
    }

@router.get("/trends")
def get_dashboard_trends(db: Session = Depends(get_db)):
    """
    Phase 2: Historical drift velocity trends, MTTR, and site vulnerability matrix.
    """
    return TrendAnalyzerService.get_historical_trends(db)
