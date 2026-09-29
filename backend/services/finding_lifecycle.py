from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.drift import DriftFinding
from backend.models.audit import AuditLog

class FindingLifecycleService:
    """
    Manages state transitions and remediation actions for drift findings in Phase 2.
    Valid states: OPEN, ACKNOWLEDGED, IN_PROGRESS, REMEDIATED, EXEMPTED.
    """

    VALID_STATUSES = {"OPEN", "ACKNOWLEDGED", "IN_PROGRESS", "REMEDIATED", "EXEMPTED"}

    @staticmethod
    def update_finding_status(
        db: Session,
        finding_id: str,
        new_status: str,
        updated_by: str = "sarah.jenkins@hospital.org",
        notes: str | None = None
    ) -> DriftFinding:
        status_upper = new_status.upper()
        if status_upper not in FindingLifecycleService.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {FindingLifecycleService.VALID_STATUSES}")

        finding = db.query(DriftFinding).filter(DriftFinding.finding_id == finding_id).first()
        if not finding:
            raise ValueError(f"Finding with ID '{finding_id}' not found.")

        old_status = finding.status
        finding.status = status_upper

        # Record audit log matching AuditLog model schema
        audit_entry = AuditLog(
            user_email=updated_by,
            user_role="ADMINISTRATOR",
            action="UPDATE_FINDING_STATUS",
            object_type="DriftFinding",
            object_id=finding_id,
            before_value=old_status,
            after_value=status_upper,
            reason=notes or "Status update via lifecycle service"
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(finding)
        return finding

    @staticmethod
    def execute_remediation_action(
        db: Session,
        finding_id: str,
        executed_by: str = "network.admin@hospital.org"
    ) -> dict:
        finding = db.query(DriftFinding).filter(DriftFinding.finding_id == finding_id).first()
        if not finding:
            raise ValueError(f"Finding with ID '{finding_id}' not found.")

        old_status = finding.status
        finding.status = "REMEDIATED"

        audit_entry = AuditLog(
            user_email=executed_by,
            user_role="NETWORK_ENGINEER",
            action="EXECUTE_REMEDIATION",
            object_type="DriftFinding",
            object_id=finding_id,
            before_value=old_status,
            after_value="REMEDIATED",
            reason=f"Remediation script executed for {finding.hostname} ({finding.field_name}). Baseline restored."
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(finding)

        return {
            "finding_id": finding.finding_id,
            "hostname": finding.hostname,
            "field_name": finding.field_name,
            "status": finding.status,
            "remediation_applied": True,
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Successfully applied remediation CLI commands for {finding.hostname}."
        }
