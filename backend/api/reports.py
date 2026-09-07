from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.report_generator import ReportGeneratorService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/drift")
def get_drift_report_pdf(db: Session = Depends(get_db)):
    pdf_bytes = ReportGeneratorService.generate_pdf_report(db, title="Hospital Network Drift Sentinel - Executive Report")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Hospital_Network_Drift_Report.pdf"}
    )

@router.get("/compliance")
def get_compliance_report_pdf(db: Session = Depends(get_db)):
    pdf_bytes = ReportGeneratorService.generate_pdf_report(db, title="Hospital Network Compliance Audit Report")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Hospital_Compliance_Audit_Report.pdf"}
    )
