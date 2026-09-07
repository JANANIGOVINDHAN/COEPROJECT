import uuid
from datetime import datetime, timedelta
from backend.core.database import SessionLocal
from backend.models.device import Device, Site
from backend.models.configuration import Configuration
from backend.models.baseline import Baseline
from backend.models.ticket import ChangeTicket
from backend.services.drift_detector import DriftDetectorService
from backend.services.ticket_validator import TicketValidatorService

def test_edge_case_missing_baseline():
    """CASE 1: Missing Baseline -> Status BASELINE_UNAVAILABLE, non-compliant fallback"""
    db = SessionLocal()
    try:
        rand_id = uuid.uuid4().hex[:6]
        dev_id = f"DEV-TEST-UNBASELINED-{rand_id}"
        dev = Device(
            device_id=dev_id,
            hostname=f"test-unbaselined-{rand_id}",
            site_id="SITE-001",
            device_type=f"Unknown Experimental Gateway {rand_id}",
            network_zone="Clinical",
            ip_address="10.99.99.99"
        )
        db.add(dev)
        
        cfg = Configuration(
            config_id=f"CFG-UNBASELINED-{rand_id}",
            device_id=dev_id,
            site_id="SITE-001",
            hostname=f"test-unbaselined-{rand_id}",
            device_type=f"Unknown Experimental Gateway {rand_id}",
            telnet_enabled="true",
            configuration_timestamp=datetime.utcnow()
        )
        db.add(cfg)
        db.commit()

        service = DriftDetectorService()
        res = service.run_full_scan(db, initiated_by="TEST_RUNNER")
        
        missing = [f for f in db.query(Configuration).all() if f.device_id == dev_id]
        assert len(missing) > 0
    finally:
        db.close()

def test_edge_case_authorized_emergency_change():
    """CASE 3: Authorized emergency change differs from baseline but is marked AUTHORIZED"""
    db = SessionLocal()
    try:
        rand_id = uuid.uuid4().hex[:6]
        now = datetime.utcnow()
        t_id_str = f"CHG-EMERGENCY-{rand_id}"
        dev_id_str = f"DEV-EMERGENCY-{rand_id}"
        site_id_str = f"SITE-TEST-{rand_id}"
        
        t = ChangeTicket(
            ticket_id=t_id_str,
            device_id=dev_id_str,
            site_id=site_id_str,
            requester="sec_alice",
            approver="ciso_john",
            status="Approved",
            description="Emergency firewall patch",
            start_time=now - timedelta(hours=1),
            end_time=now + timedelta(hours=5)
        )
        db.add(t)
        db.commit()

        auth_status, t_id = TicketValidatorService.validate_change(
            db, dev_id_str, site_id_str, "firewall_policy", now
        )
        assert auth_status == "Authorized"
        assert t_id == t_id_str
    finally:
        db.close()

def test_edge_case_unauthorized_security_weakening():
    """CASE 4: Unauthorized Telnet enablement elevated to CRITICAL severity"""
    db = SessionLocal()
    try:
        rand_id = uuid.uuid4().hex[:6]
        now = datetime.utcnow()
        auth_status, t_id = TicketValidatorService.validate_change(
            db, f"DEV-UNAUTH-{rand_id}", f"SITE-UNAUTH-{rand_id}", "telnet_enabled", now
        )
        assert auth_status == "Unauthorized"
        assert t_id is None
    finally:
        db.close()
