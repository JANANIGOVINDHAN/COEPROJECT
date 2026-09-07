import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.device import Device, Site
from backend.models.configuration import Configuration
from backend.models.baseline import Baseline
from backend.models.drift import DriftFinding, ScanRun
from backend.models.audit import AuditLog

from backend.services.ticket_validator import TicketValidatorService
from backend.services.compliance_engine import ComplianceEngineService
from backend.services.risk_engine import RiskScoringEngine
from backend.services.evidence_engine import EvidenceEngineService
from backend.services.remediation_engine import RemediationEngineService

from backend.ml.anomaly_detection import IsolationForestAnomalyDetector
from backend.ml.risk_model import RiskClassifierModel

class DriftDetectorService:
    def __init__(self):
        self.anomaly_detector = IsolationForestAnomalyDetector()
        self.risk_classifier = RiskClassifierModel()

    def run_full_scan(self, db: Session, initiated_by: str = "SYSTEM") -> dict:
        scan_id = f"SCAN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
        devices = db.query(Device).all()
        
        devices_scanned = 0
        findings_created = []
        unauthorized_count = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

        for dev in devices:
            devices_scanned += 1
            # Get latest configuration record
            latest_config = db.query(Configuration).filter(
                Configuration.device_id == dev.device_id
            ).order_by(Configuration.configuration_timestamp.desc()).first()

            if not latest_config:
                continue

            # Get site details
            site = db.query(Site).filter(Site.site_id == dev.site_id).first()
            site_crit = site.criticality if site else 0.75
            site_name = site.name if site else dev.site_id

            # Find matching approved baseline for device type
            baseline = db.query(Baseline).filter(
                Baseline.device_type == dev.device_type,
                Baseline.status == "APPROVED"
            ).first()

            # Handle EDGE CASE 1: Missing baseline
            if not baseline:
                finding_id = f"FND-{scan_id[-6:]}-{dev.device_id}-BASE-{uuid.uuid4().hex[:4].upper()}"
                evidence = f"BASELINE_UNAVAILABLE: No approved baseline template found for device type '{dev.device_type}'."
                finding = DriftFinding(
                    finding_id=finding_id,
                    device_id=dev.device_id,
                    site_id=dev.site_id,
                    hostname=dev.hostname,
                    device_type=dev.device_type,
                    field_name="baseline_status",
                    baseline_value="APPROVED_TEMPLATE_EXISTS",
                    current_value="BASELINE_MISSING",
                    change_type="MISSING",
                    severity="HIGH",
                    risk_score=65.0,
                    anomaly_score=50.0,
                    authorization_status="Unauthorized",
                    compliance_status="Violation",
                    evidence=evidence,
                    recommended_action="Create and approve baseline template for device type " + dev.device_type,
                    status="OPEN"
                )
                db.add(finding)
                findings_created.append(finding)
                high_count += 1
                unauthorized_count += 1
                continue

            # Parse baseline JSON
            try:
                approved_dict = json.loads(baseline.approved_config_json)
            except Exception:
                approved_dict = {}

            # Field by field comparison
            fields_to_check = [
                "telnet_enabled", "ssh_enabled", "logging_enabled", "ntp_enabled",
                "https_enabled", "encryption_enabled", "port_security", "bpdu_guard",
                "dhcp_snooping", "guest_isolation", "network_segmentation", "firewall_policy"
            ]

            # Run compliance check
            compliance_evals = ComplianceEngineService.evaluate_configuration(db, latest_config)
            compliance_map = {item["field"]: item for item in compliance_evals}

            for idx, field_name in enumerate(fields_to_check):
                baseline_val = str(approved_dict.get(field_name, "true")).lower()
                current_val = str(getattr(latest_config, field_name, "false")).lower()

                # Check if mismatch/drift occurred
                if baseline_val != current_val:
                    # 1. Validate Change Ticket
                    auth_status, ticket_id = TicketValidatorService.validate_change(
                        db, dev.device_id, dev.site_id, field_name, latest_config.configuration_timestamp
                    )

                    # 2. Check compliance
                    comp_info = compliance_map.get(field_name, {})
                    comp_status = "Violation" if comp_info.get("status") == "FAIL" else "Compliant"
                    violated_rule_id = comp_info.get("rule_id") if comp_status == "Violation" else None

                    # 3. Calculate Anomaly Score with ML Isolation Forest
                    feature_vec = [
                        1 if current_val == "true" else 0,
                        1 if getattr(latest_config, "ssh_enabled", "true") == "true" else 0,
                        1 if getattr(latest_config, "logging_enabled", "true") == "true" else 0,
                        1 if getattr(latest_config, "guest_isolation", "true") == "true" else 0,
                        1 if getattr(latest_config, "dhcp_snooping", "true") == "true" else 0,
                        0.5, 0.5, 1 if auth_status == "Authorized" else 0, 1
                    ]
                    anomaly_score = self.anomaly_detector.predict_anomaly(feature_vec)

                    # 4. Calculate Risk Score
                    risk_score, severity, risk_breakdown = RiskScoringEngine.calculate_risk_score(
                        field_name=field_name,
                        auth_status=auth_status,
                        compliance_status=comp_status,
                        site_criticality=site_crit,
                        anomaly_score=anomaly_score,
                        affected_devices_count=1
                    )

                    # 5. Generate Evidence & Remediation
                    ts_str = latest_config.configuration_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    evidence = EvidenceEngineService.generate_evidence(
                        device_id=dev.device_id,
                        hostname=dev.hostname,
                        site_name=site_name,
                        field_name=field_name,
                        baseline_val=baseline_val,
                        current_val=current_val,
                        timestamp=ts_str,
                        ticket_id=ticket_id,
                        auth_status=auth_status,
                        violated_rule=violated_rule_id,
                        risk_score=risk_score,
                        risk_breakdown=risk_breakdown
                    )

                    remed = RemediationEngineService.get_remediation(field_name, current_val)
                    recommended_action = f"{remed['action']}\nCLI Command:\n{remed['cli_command']}"

                    finding_id = f"FND-{uuid.uuid4().hex[:8].upper()}-{dev.device_id}-{field_name.upper()[:6]}"

                    finding = DriftFinding(
                        finding_id=finding_id,
                        device_id=dev.device_id,
                        site_id=dev.site_id,
                        hostname=dev.hostname,
                        device_type=dev.device_type,
                        field_name=field_name,
                        baseline_value=baseline_val,
                        current_value=current_val,
                        change_type="MODIFIED",
                        severity=severity,
                        risk_score=risk_score,
                        anomaly_score=anomaly_score,
                        authorization_status=auth_status,
                        ticket_id=ticket_id,
                        compliance_status=comp_status,
                        violated_rule_id=violated_rule_id,
                        evidence=evidence,
                        recommended_action=recommended_action,
                        status="OPEN"
                    )
                    db.add(finding)
                    findings_created.append(finding)

                    if auth_status != "Authorized":
                        unauthorized_count += 1

                    if severity == "CRITICAL": critical_count += 1
                    elif severity == "HIGH": high_count += 1
                    elif severity == "MEDIUM": medium_count += 1
                    else: low_count += 1

        # Record scan run in database
        scan_record = ScanRun(
            scan_id=scan_id,
            devices_scanned=devices_scanned,
            findings_count=len(findings_created),
            unauthorized_count=unauthorized_count,
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            status="COMPLETED",
            initiated_by=initiated_by
        )
        db.add(scan_record)

        # Record audit log
        audit = AuditLog(
            user_email=initiated_by,
            user_role="System",
            action="SCAN_EXECUTED",
            object_type="ScanRun",
            object_id=scan_id,
            after_value=f"Scanned {devices_scanned} devices. Created {len(findings_created)} findings.",
            reason="Automated network configuration drift scan execution."
        )
        db.add(audit)

        db.commit()

        return {
            "scan_id": scan_id,
            "devices_scanned": devices_scanned,
            "findings_count": len(findings_created),
            "unauthorized_count": unauthorized_count,
            "critical_count": critical_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "status": "COMPLETED"
        }
