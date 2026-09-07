import os
import json
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.database import engine, Base, SessionLocal
from backend.core.security import get_password_hash

from backend.models.user import User
from backend.models.device import Device, Site
from backend.models.configuration import Configuration
from backend.models.baseline import Baseline
from backend.models.compliance import ComplianceRule
from backend.models.ticket import ChangeTicket
from backend.services.drift_detector import DriftDetectorService

def seed_database():
    print("Creating database schema tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    # 1. Seed Demo Users
    users_to_seed = [
        {"email": "admin@hospital.org", "username": "admin", "password": "adminpassword123", "name": "Dr. Sarah Jenkins (CISO)", "role": "Administrator"},
        {"email": "security@hospital.org", "username": "security", "password": "securitypassword123", "name": "Alex Mercer (Sec Analyst)", "role": "Security Analyst"},
        {"email": "network@hospital.org", "username": "network", "password": "networkpassword123", "name": "Carlos Rivera (Sr Net Eng)", "role": "Network Engineer"}
    ]
    
    for u in users_to_seed:
        existing = db.query(User).filter(User.username == u["username"]).first()
        if not existing:
            db_user = User(
                email=u["email"],
                username=u["username"],
                hashed_password=get_password_hash(u["password"]),
                full_name=u["name"],
                role=u["role"]
            )
            db.add(db_user)
    print("Demo users seeded successfully.")

    # 2. Seed Sites & Devices from cleaned CSV
    sites_data = [
        {"site_id": "SITE-001", "name": "Main Hospital", "code": "MAIN", "criticality": 1.0},
        {"site_id": "SITE-002", "name": "Emergency Care Center", "code": "EMERGENCY", "criticality": 0.95},
        {"site_id": "SITE-003", "name": "Diagnostic Center", "code": "DIAG", "criticality": 0.85},
        {"site_id": "SITE-004", "name": "Pharmacy", "code": "PHARM", "criticality": 0.75},
        {"site_id": "SITE-005", "name": "Remote Clinic", "code": "CLINIC", "criticality": 0.65},
        {"site_id": "SITE-006", "name": "Research Center", "code": "RESEARCH", "criticality": 0.70},
        {"site_id": "SITE-007", "name": "Children's Hospital", "code": "PEDS", "criticality": 0.90},
        {"site_id": "SITE-008", "name": "Cardiology Center", "code": "CARDIO", "criticality": 0.85},
        {"site_id": "SITE-009", "name": "Cancer Center", "code": "ONCOLOGY", "criticality": 0.85},
        {"site_id": "SITE-010", "name": "Administration Center", "code": "ADMIN", "criticality": 0.50}
    ]
    for s in sites_data:
        if not db.query(Site).filter(Site.site_id == s["site_id"]).first():
            db.add(Site(**s))

    dev_csv = os.path.join(settings.DATA_DIR, "cleaned", "devices_cleaned.csv")
    if os.path.exists(dev_csv):
        dev_df = pd.read_csv(dev_csv)
        for _, row in dev_df.iterrows():
            d_id = str(row["device_id"])
            if d_id and not db.query(Device).filter(Device.device_id == d_id).first():
                db.add(Device(
                    device_id=d_id,
                    hostname=str(row["hostname"]),
                    site_id=str(row["site_id"]),
                    site_name=str(row.get("site_name", row["site_id"])),
                    device_type=str(row["device_type"]),
                    network_zone=str(row["network_zone"]),
                    ip_address=str(row["ip_address"]),
                    mac_address=str(row.get("mac_address", "00:50:56:00:00:00")),
                    firmware_version=str(row.get("firmware_version", "v15.2")),
                    status=str(row.get("status", "ONLINE"))
                ))
        print("Devices seeded from cleaned dataset.")

    # 3. Seed Compliance Rules
    rules_csv = os.path.join(settings.DATA_DIR, "cleaned", "compliance_cleaned.csv")
    if os.path.exists(rules_csv):
        rules_df = pd.read_csv(rules_csv)
        for _, r in rules_df.iterrows():
            r_id = str(r["rule_id"])
            if not db.query(ComplianceRule).filter(ComplianceRule.rule_id == r_id).first():
                db.add(ComplianceRule(
                    rule_id=r_id,
                    rule_name=str(r["rule_name"]),
                    category=str(r["category"]),
                    description=str(r["description"]),
                    severity=str(r["severity"]),
                    field=str(r["field"]),
                    operator=str(r["operator"]),
                    expected_value=str(r["expected_value"]),
                    enabled=True
                ))
        print("Compliance rules seeded.")

    # 4. Seed Change Tickets
    tickets_csv = os.path.join(settings.DATA_DIR, "cleaned", "tickets_cleaned.csv")
    if os.path.exists(tickets_csv):
        tickets_df = pd.read_csv(tickets_csv).head(500) # Seed top 500 for DB efficiency
        for _, t in tickets_df.iterrows():
            t_id = str(t["ticket_id"])
            if not db.query(ChangeTicket).filter(ChangeTicket.ticket_id == t_id).first():
                db.add(ChangeTicket(
                    ticket_id=t_id,
                    device_id=str(t["device_id"]) if pd.notna(t["device_id"]) else None,
                    site_id=str(t["site_id"]),
                    requester=str(t["requester"]),
                    approver=str(t["approver"]) if pd.notna(t["approver"]) else None,
                    status=str(t["status"]),
                    description=str(t["description"]),
                    requested_changes=str(t.get("requested_changes", "")),
                    start_time=pd.to_datetime(t["start_time"]),
                    end_time=pd.to_datetime(t["end_time"])
                ))
        print("Change tickets seeded.")

    # 5. Seed Baselines
    device_types = [
        "Core Router", "Edge Router", "Firewall", "Switch",
        "Wireless Controller", "Access Point", "VPN Gateway", "IoT Gateway"
    ]
    
    for dt in device_types:
        b_id = f"BSL-{dt.replace(' ', '-').upper()}-GLOBAL"
        if not db.query(Baseline).filter(Baseline.device_type == dt).first():
            config_template = {
                "telnet_enabled": "false",
                "ssh_enabled": "true",
                "logging_enabled": "true",
                "ntp_enabled": "true",
                "https_enabled": "true",
                "encryption_enabled": "true",
                "port_security": "true",
                "bpdu_guard": "true",
                "dhcp_snooping": "true",
                "guest_isolation": "true",
                "network_segmentation": "true",
                "firewall_policy": "ALLOW_ESTABLISHED,DEFAULT_DENY",
                "password_policy": "ENFORCED",
                "backup_enabled": "true"
            }
            db.add(Baseline(
                baseline_id=b_id,
                name=f"Approved Standard Baseline for {dt}",
                device_type=dt,
                version=1,
                status="APPROVED",
                approved_config_json=json.dumps(config_template),
                approved_by="CAB_Board_Chair"
            ))

    # 6. Seed Configurations from cleaned CSV
    cfg_csv = os.path.join(settings.DATA_DIR, "cleaned", "configurations_cleaned.csv")
    if os.path.exists(cfg_csv):
        cfg_df = pd.read_csv(cfg_csv).head(600) # Seed 600 config snapshots
        for _, c in cfg_df.iterrows():
            c_id = str(c["config_id"])
            if not db.query(Configuration).filter(Configuration.config_id == c_id).first():
                db.add(Configuration(
                    config_id=c_id,
                    device_id=str(c["device_id"]),
                    site_id=str(c["site_id"]),
                    hostname=str(c["hostname"]),
                    device_type=str(c["device_type"]),
                    firmware_version=str(c.get("firmware_version", "v15.2")),
                    ssh_enabled=str(c.get("ssh_enabled", "true")),
                    telnet_enabled=str(c.get("telnet_enabled", "false")),
                    https_enabled=str(c.get("https_enabled", "true")),
                    ntp_enabled=str(c.get("ntp_enabled", "true")),
                    logging_enabled=str(c.get("logging_enabled", "true")),
                    encryption_enabled=str(c.get("encryption_enabled", "true")),
                    port_security=str(c.get("port_security", "true")),
                    bpdu_guard=str(c.get("bpdu_guard", "true")),
                    dhcp_snooping=str(c.get("dhcp_snooping", "true")),
                    guest_isolation=str(c.get("guest_isolation", "true")),
                    network_segmentation=str(c.get("network_segmentation", "true")),
                    firewall_policy=str(c.get("firewall_policy", "ALLOW_ESTABLISHED,DEFAULT_DENY")),
                    configuration_timestamp=pd.to_datetime(c["configuration_timestamp"])
                ))
        print("Configuration snapshots seeded.")

    db.commit()

    # 7. Run initial drift scan to populate DriftFindings
    print("Running initial automated configuration drift scan...")
    drift_service = DriftDetectorService()
    scan_res = drift_service.run_full_scan(db, initiated_by="INITIAL_SEED_SCAN")
    print("Initial scan completed:", scan_res)

    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
