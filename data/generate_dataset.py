import os
import json
import random
import datetime
import pandas as pd
import numpy as np

# Ensure data directories exist
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
CLEANED_DIR = os.path.join(os.path.dirname(__file__), "cleaned")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ----------------------------------------------------
# 1. CONSTANTS & DOMAIN MASTER DATA
# ----------------------------------------------------
SITES = [
    {"site_id": "SITE-001", "name": "Main Hospital", "criticality": 1.0, "code": "MAIN"},
    {"site_id": "SITE-002", "name": "Emergency Care Center", "criticality": 0.95, "code": "EMERGENCY"},
    {"site_id": "SITE-003", "name": "Diagnostic Center", "criticality": 0.85, "code": "DIAG"},
    {"site_id": "SITE-004", "name": "Pharmacy", "criticality": 0.75, "code": "PHARM"},
    {"site_id": "SITE-005", "name": "Remote Clinic", "criticality": 0.65, "code": "CLINIC"},
    {"site_id": "SITE-006", "name": "Research Center", "criticality": 0.70, "code": "RESEARCH"},
    {"site_id": "SITE-007", "name": "Children's Hospital", "criticality": 0.90, "code": "PEDS"},
    {"site_id": "SITE-008", "name": "Cardiology Center", "criticality": 0.85, "code": "CARDIO"},
    {"site_id": "SITE-009", "name": "Cancer Center", "criticality": 0.85, "code": "ONCOLOGY"},
    {"site_id": "SITE-010", "name": "Administration Center", "criticality": 0.50, "code": "ADMIN"}
]

DEVICE_TYPES = [
    "Core Router", "Edge Router", "Firewall", "Switch",
    "Wireless Controller", "Access Point", "VPN Gateway", "IoT Gateway"
]

NETWORK_ZONES = [
    "Clinical", "Guest", "Medical IoT", "Administration", "Server", "Management"
]

COMPLIANCE_RULES = [
    {"rule_id": "RULE-001", "rule_name": "Disable Telnet", "category": "Security", "description": "Telnet protocol must be disabled across all devices.", "severity": "CRITICAL", "field": "telnet_enabled", "operator": "==", "expected_value": "false"},
    {"rule_id": "RULE-002", "rule_name": "Enable SSH v2", "category": "Security", "description": "SSH v2 must be enabled for secure remote management.", "severity": "HIGH", "field": "ssh_enabled", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-003", "rule_name": "Guest Wi-Fi Isolation", "category": "Segmentation", "description": "Guest Wi-Fi traffic must be strictly isolated from internal networks.", "severity": "CRITICAL", "field": "guest_isolation", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-004", "rule_name": "No VLAN Overlap", "category": "Segmentation", "description": "Clinical and Guest VLANs must not share subnet segment or tags.", "severity": "HIGH", "field": "network_segmentation", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-005", "rule_name": "Centralized Syslog", "category": "Logging", "description": "Logging must be enabled and set to centralized syslog server.", "severity": "MEDIUM", "field": "logging_enabled", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-006", "rule_name": "NTP Time Sync", "category": "Operations", "description": "NTP time synchronization must be enabled.", "severity": "MEDIUM", "field": "ntp_enabled", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-007", "rule_name": "AES-256 Encryption", "category": "Security", "description": "Encryption must be enabled for all wireless and WAN traffic.", "severity": "HIGH", "field": "encryption_enabled", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-008", "rule_name": "HTTPS Admin Access", "category": "Security", "description": "HTTPS must be enforced for admin web portals.", "severity": "HIGH", "field": "https_enabled", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-009", "rule_name": "Medical IoT Segmentation", "category": "Segmentation", "description": "Medical IoT devices must be isolated on VLAN 300-399.", "severity": "CRITICAL", "field": "port_security", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-010", "rule_name": "Firewall Default Deny", "category": "Firewall", "description": "Firewall policies must enforce explicit default deny rule.", "severity": "CRITICAL", "field": "firewall_policy", "operator": "contains", "expected_value": "DEFAULT_DENY"},
    {"rule_id": "RULE-011", "rule_name": "SNMP v3 Enforcement", "category": "Management", "description": "Legacy SNMP v1/v2c disabled, SNMP v3 mandatory.", "severity": "HIGH", "field": "snmp_version", "operator": "==", "expected_value": "v3"},
    {"rule_id": "RULE-012", "rule_name": "BPDU Guard Active", "category": "Switching", "description": "BPDU Guard must be active on access ports.", "severity": "MEDIUM", "field": "bpdu_guard", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-013", "rule_name": "DHCP Snooping Enabled", "category": "Switching", "description": "DHCP Snooping must prevent rogue DHCP servers.", "severity": "HIGH", "field": "dhcp_snooping", "operator": "==", "expected_value": "true"},
    {"rule_id": "RULE-014", "rule_name": "Strong Password Policy", "category": "Authentication", "description": "Complex password policy enforced on local accounts.", "severity": "MEDIUM", "field": "password_policy", "operator": "==", "expected_value": "ENFORCED"},
    {"rule_id": "RULE-015", "rule_name": "Automated Config Backup", "category": "Operations", "description": "Nightly configuration backup must be enabled.", "severity": "LOW", "field": "backup_enabled", "operator": "==", "expected_value": "true"}
]

# Add more rules to reach 30+ rules
for i in range(16, 32):
    COMPLIANCE_RULES.append({
        "rule_id": f"RULE-0{i:02d}",
        "rule_name": f"Compliance Standard Metric {i}",
        "category": random.choice(["Security", "Segmentation", "Logging", "Operations", "Management"]),
        "description": f"Standard operational security compliance policy metric #{i}",
        "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
        "field": random.choice(["admin_access", "spanning_tree", "snmp_community", "static_routes", "dns_server"]),
        "operator": "==",
        "expected_value": "APPROVED"
    })

# ----------------------------------------------------
# 2. GENERATE RAW DEVICES (100+ Devices)
# ----------------------------------------------------
def generate_devices(count=110):
    devices = []
    for i in range(1, count + 1):
        site = random.choice(SITES)
        dtype = random.choice(DEVICE_TYPES)
        dev_id = f"DEV-{site['code']}-{dtype[:3].upper()}-{i:03d}"
        hostname = f"{site['code'].lower()}-{dtype.lower().replace(' ', '-')}-{i:03d}"
        ip = f"10.{random.randint(1, 10)}.{random.randint(1, 250)}.{random.randint(1, 254)}"
        
        # Inject raw errors into 5% of rows
        if random.random() < 0.05:
            ip = random.choice(["999.300.1.1", "invalid_ip", "10.0.0.256", ""])
        if random.random() < 0.03:
            dev_id = "" # missing device id
        if random.random() < 0.03:
            hostname = hostname.upper() # inconsistent casing

        devices.append({
            "device_id": dev_id,
            "hostname": hostname,
            "site_id": site["site_id"],
            "site_name": site["name"],
            "device_type": dtype,
            "network_zone": random.choice(NETWORK_ZONES),
            "ip_address": ip,
            "mac_address": f"00:50:56:{random.randint(10,99):02x}:{random.randint(10,99):02x}:{random.randint(10,99):02x}",
            "firmware_version": random.choice(["v15.2(4)S", "v17.3.1", "v7.2.4", "v9.1.2"]),
            "status": "ONLINE" if random.random() > 0.05 else "OFFLINE"
        })
    df_dev = pd.DataFrame(devices)
    # Add explicit duplicate records
    df_dev = pd.concat([df_dev, df_dev.iloc[:3]], ignore_index=True)
    return df_dev

# ----------------------------------------------------
# 3. GENERATE CHANGE TICKETS (5,000+ Tickets)
# ----------------------------------------------------
def generate_tickets(devices_df, count=5200):
    tickets = []
    base_time = datetime.datetime.now() - datetime.timedelta(days=90)
    valid_dev_ids = [d for d in devices_df["device_id"].tolist() if d]
    
    reasons = [
        "Routine maintenance patch", "Emergency firewall rule update",
        "VLAN reconfiguration for IoT", "Firmware security hotfix",
        "Syslog server migration", "Disable legacy Telnet interface",
        "Wi-Fi guest network tuning", "BGP route policy expansion"
    ]
    
    for i in range(1, count + 1):
        t_id = f"CHG-{i:06d}"
        dev_id = random.choice(valid_dev_ids)
        site_id = random.choice(SITES)["site_id"]
        status = random.choice(["Approved", "Approved", "Approved", "Completed", "Pending", "Draft", "Rejected", "Expired"])
        
        start_offset = random.randint(1, 90) * 24 + random.randint(0, 59)
        start_time = base_time + datetime.timedelta(hours=start_offset)
        end_time = start_time + datetime.timedelta(hours=random.randint(2, 48))
        
        # Inject raw errors
        if random.random() < 0.03:
            start_time_str = "INVALID_TIMESTAMP_STRING"
        else:
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            
        tickets.append({
            "ticket_id": t_id,
            "device_id": dev_id if random.random() > 0.02 else "",
            "site_id": site_id,
            "requester": random.choice(["net_admin_alice", "sec_bob", "ops_charlie", "admin_diana"]),
            "approver": random.choice(["cab_mgr_steve", "ciso_john", "director_mark"]) if status in ["Approved", "Completed"] else "",
            "status": status,
            "description": random.choice(reasons),
            "requested_changes": "telnet_enabled: false, ssh_enabled: true, logging_enabled: true",
            "start_time": start_time_str,
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": (start_time - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(tickets)

# ----------------------------------------------------
# 4. GENERATE CONFIGURATION RECORDS (10,000+ Snapshots)
# ----------------------------------------------------
def generate_configurations(devices_df, tickets_df, count=10500):
    configs = []
    base_time = datetime.datetime.now() - datetime.timedelta(days=90)
    valid_devices = devices_df[devices_df["device_id"] != ""].to_dict("records")
    
    for i in range(1, count + 1):
        dev = random.choice(valid_devices)
        dev_id = dev["device_id"]
        site_id = dev["site_id"]
        
        # Standard baseline configuration values
        telnet = "false"
        ssh = "true"
        logging = "true"
        ntp = "true"
        https = "true"
        encryption = "true"
        guest_iso = "true"
        port_sec = "true"
        dhcp_snoop = "true"
        bpdu = "true"
        pw_policy = "ENFORCED"
        snmp_v = "v3"
        fw_policy = "ALLOW_ESTABLISHED,DEFAULT_DENY"
        vlan_cfg = "10,20,30,100,200,300"
        
        # Drift Injection logic (35% probability of drift per snapshot)
        has_drift = random.random() < 0.35
        drift_type = "SAFE"
        if has_drift:
            drift_kind = random.choice([
                "UNAUTHORIZED_TELNET", "LOGGING_DISABLED", "GUEST_ISO_DISABLED",
                "FIREWALL_PERMISSIVE", "DHCP_SNOOPING_DISABLED", "AUTHORIZED_PATCH"
            ])
            if drift_kind == "UNAUTHORIZED_TELNET":
                telnet = "true"
                drift_type = "UNAUTHORIZED"
            elif drift_kind == "LOGGING_DISABLED":
                logging = "false"
                drift_type = "UNAUTHORIZED"
            elif drift_kind == "GUEST_ISO_DISABLED":
                guest_iso = "false"
                drift_type = "UNAUTHORIZED"
            elif drift_kind == "FIREWALL_PERMISSIVE":
                fw_policy = "ALLOW_ALL"
                drift_type = "UNAUTHORIZED"
            elif drift_kind == "DHCP_SNOOPING_DISABLED":
                dhcp_snoop = "false"
                drift_type = "UNAUTHORIZED"
            elif drift_kind == "AUTHORIZED_PATCH":
                ssh = "true"
                logging = "true"
                drift_type = "AUTHORIZED"

        ts = base_time + datetime.timedelta(minutes=random.randint(1, 90*24*60))
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        
        # Inject raw dataset anomalies
        if random.random() < 0.04:
            telnet = random.choice(["True", "TRUE", "1", "enabled", "YES"])
        if random.random() < 0.03:
            vlan_cfg = "10,20,,9999,VLAN_ERR" # malformed vlan string
        if random.random() < 0.02:
            ts_str = "2029-99-99 99:99:99" # invalid timestamp

        configs.append({
            "config_id": f"CFG-{i:07d}",
            "device_id": dev_id if random.random() > 0.01 else None,
            "site_id": site_id,
            "hostname": dev["hostname"],
            "device_type": dev["device_type"],
            "firmware_version": dev["firmware_version"],
            "vlan_configuration": vlan_cfg,
            "allowed_vlans": "10,20,30,100,200",
            "native_vlan": 1,
            "ip_address": dev["ip_address"],
            "subnet": "255.255.255.0",
            "routing_protocol": "OSPF",
            "static_routes": "0.0.0.0/0 via 10.1.1.1",
            "ospf_enabled": "true",
            "bgp_enabled": "false",
            "firewall_policy": fw_policy,
            "acl_rules": "PERMIT_CLINICAL,DENY_GUEST_TO_INTERNAL",
            "ssh_enabled": ssh,
            "telnet_enabled": telnet,
            "https_enabled": https,
            "snmp_version": snmp_v,
            "snmp_community": "PUBLIC_COMMUNITY" if random.random() < 0.05 else "SECURE_SNMP_COMMUNITY",
            "ntp_enabled": ntp,
            "ntp_server": "10.0.0.50",
            "logging_enabled": logging,
            "syslog_server": "10.0.0.51",
            "dns_server": "10.0.0.2",
            "password_policy": pw_policy,
            "encryption_enabled": encryption,
            "port_security": port_sec,
            "bpdu_guard": bpdu,
            "dhcp_snooping": dhcp_snoop,
            "spanning_tree": "MSTP",
            "guest_isolation": guest_iso,
            "network_segmentation": "true",
            "admin_access": "SSH_TACACS",
            "backup_enabled": "true",
            "configuration_timestamp": ts_str,
            "drift_type_label": drift_type
        })
        
    df_cfg = pd.DataFrame(configs)
    # Inject duplicated configuration snapshots
    df_cfg = pd.concat([df_cfg, df_cfg.iloc[:50]], ignore_index=True)
    return df_cfg

# ----------------------------------------------------
# 5. GENERATE NETWORK EVENTS (20,000+ Events)
# ----------------------------------------------------
def generate_events(devices_df, count=20500):
    events = []
    base_time = datetime.datetime.now() - datetime.timedelta(days=90)
    valid_devs = devices_df[devices_df["device_id"] != ""].to_dict("records")
    
    event_types = [
        "CONFIG_CHANGE", "LOGIN_SUCCESS", "LOGIN_FAILED",
        "PORT_DOWN", "PORT_UP", "ACL_DENY_SPIKE", "NTP_SYNC_LOST"
    ]
    
    for i in range(1, count + 1):
        dev = random.choice(valid_devs)
        etype = random.choice(event_types)
        ts = base_time + datetime.timedelta(minutes=random.randint(1, 90*24*60))
        
        events.append({
            "event_id": f"EVT-{i:08d}",
            "device_id": dev["device_id"],
            "site_id": dev["site_id"],
            "event_type": etype,
            "severity": "CRITICAL" if etype in ["ACL_DENY_SPIKE", "CONFIG_CHANGE"] else "INFO",
            "message": f"Network event {etype} registered on device {dev['hostname']}",
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(events)


# ----------------------------------------------------
# 6. DATA CLEANING PIPELINE & FEATURE ENGINEERING
# ----------------------------------------------------
def run_data_cleaning_pipeline(raw_devs, raw_configs, raw_tickets, raw_rules, raw_events):
    quality_metrics = {
        "raw_devices": len(raw_devs),
        "raw_configs": len(raw_configs),
        "raw_tickets": len(raw_tickets),
        "raw_rules": len(raw_rules),
        "raw_events": len(raw_events),
        "removed_duplicates": 0,
        "fixed_missing_values": 0,
        "invalid_ips_cleaned": 0,
        "normalized_booleans": 0,
        "clean_configs_count": 0
    }
    
    # Clean Devices
    dev_clean = raw_devs.drop_duplicates(subset=["device_id", "hostname"]).copy()
    quality_metrics["removed_duplicates"] += len(raw_devs) - len(dev_clean)
    dev_clean = dev_clean[dev_clean["device_id"].notna() & (dev_clean["device_id"] != "")]
    
    # Fix IP addresses
    def clean_ip(ip):
        if not isinstance(ip, str): return "10.0.0.1"
        parts = ip.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            return ip
        quality_metrics["invalid_ips_cleaned"] += 1
        return "10.0.0.1"
        
    dev_clean["ip_address"] = dev_clean["ip_address"].apply(clean_ip)
    
    # Clean Tickets
    tickets_clean = raw_tickets.drop_duplicates(subset=["ticket_id"]).copy()
    tickets_clean["device_id"] = tickets_clean["device_id"].fillna("UNKNOWN")
    
    def clean_ts(ts):
        try:
            return pd.to_datetime(ts).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            
    tickets_clean["start_time"] = tickets_clean["start_time"].apply(clean_ts)
    tickets_clean["end_time"] = tickets_clean["end_time"].apply(clean_ts)
    
    # Clean Configs
    cfg_clean = raw_configs.drop_duplicates(subset=["config_id"]).copy()
    quality_metrics["removed_duplicates"] += len(raw_configs) - len(cfg_clean)
    cfg_clean = cfg_clean[cfg_clean["device_id"].notna()]
    
    # Normalize Boolean strings
    bool_fields = [
        "ssh_enabled", "telnet_enabled", "https_enabled", "ntp_enabled",
        "logging_enabled", "encryption_enabled", "port_security", "bpdu_guard",
        "dhcp_snooping", "guest_isolation", "network_segmentation", "backup_enabled"
    ]
    
    def normalize_bool(val):
        if str(val).lower() in ["true", "1", "yes", "enabled"]:
            return "true"
        return "false"
        
    for bf in bool_fields:
        if bf in cfg_clean.columns:
            cfg_clean[bf] = cfg_clean[bf].apply(normalize_bool)
            quality_metrics["normalized_booleans"] += 1
            
    cfg_clean["configuration_timestamp"] = cfg_clean["configuration_timestamp"].apply(clean_ts)
    quality_metrics["clean_configs_count"] = len(cfg_clean)
    
    # Save Cleaned Datasets
    dev_clean.to_csv(os.path.join(CLEANED_DIR, "devices_cleaned.csv"), index=False)
    cfg_clean.to_csv(os.path.join(CLEANED_DIR, "configurations_cleaned.csv"), index=False)
    tickets_clean.to_csv(os.path.join(CLEANED_DIR, "tickets_cleaned.csv"), index=False)
    raw_rules.to_csv(os.path.join(CLEANED_DIR, "compliance_cleaned.csv"), index=False)
    raw_events.to_csv(os.path.join(CLEANED_DIR, "network_events_cleaned.csv"), index=False)
    
    with open(os.path.join(CLEANED_DIR, "data_quality_report.json"), "w") as f:
        json.dump(quality_metrics, f, indent=2)
        
    print("Data cleaning completed. Quality Report:", quality_metrics)
    return dev_clean, cfg_clean, tickets_clean, raw_rules

# ----------------------------------------------------
# 7. FEATURE ENGINEERING FOR ML
# ----------------------------------------------------
def run_feature_engineering(dev_df, cfg_df, ticket_df):
    features = []
    
    for idx, row in cfg_df.iterrows():
        # Feature computation
        telnet_num = 1 if row.get("telnet_enabled") == "true" else 0
        ssh_num = 1 if row.get("ssh_enabled") == "true" else 0
        logging_num = 1 if row.get("logging_enabled") == "true" else 0
        guest_iso_num = 1 if row.get("guest_isolation") == "true" else 0
        dhcp_snoop_num = 1 if row.get("dhcp_snooping") == "true" else 0
        
        security_weakening_score = (telnet_num * 0.4) + ((1 - ssh_num) * 0.3) + ((1 - logging_num) * 0.3)
        segmentation_risk_score = (1 - guest_iso_num) * 0.5 + (1 - dhcp_snoop_num) * 0.5
        
        # Check if matching ticket exists within window
        cfg_ts = pd.to_datetime(row["configuration_timestamp"])
        dev_tickets = ticket_df[ticket_df["device_id"] == row["device_id"]]
        
        has_authorized_ticket = 0
        for _, t in dev_tickets.iterrows():
            if t["status"] in ["Approved", "Completed"]:
                t_start = pd.to_datetime(t["start_time"])
                t_end = pd.to_datetime(t["end_time"])
                if t_start <= cfg_ts <= t_end + pd.Timedelta(hours=6):
                    has_authorized_ticket = 1
                    break
                    
        num_changed_fields = 0
        if telnet_num == 1: num_changed_fields += 1
        if ssh_num == 0: num_changed_fields += 1
        if logging_num == 0: num_changed_fields += 1
        if guest_iso_num == 0: num_changed_fields += 1
        
        # Risk target calculation for supervised Random Forest model
        if security_weakening_score > 0.5 and has_authorized_ticket == 0:
            target_risk_label = "CRITICAL"
            risk_num = 3
        elif security_weakening_score > 0.2 and has_authorized_ticket == 0:
            target_risk_label = "HIGH"
            risk_num = 2
        elif num_changed_fields > 0 and has_authorized_ticket == 1:
            target_risk_label = "LOW"
            risk_num = 0
        elif num_changed_fields > 0:
            target_risk_label = "MEDIUM"
            risk_num = 1
        else:
            target_risk_label = "LOW"
            risk_num = 0
            
        features.append({
            "config_id": row["config_id"],
            "device_id": row["device_id"],
            "telnet_num": telnet_num,
            "ssh_num": ssh_num,
            "logging_num": logging_num,
            "guest_iso_num": guest_iso_num,
            "dhcp_snoop_num": dhcp_snoop_num,
            "security_weakening_score": security_weakening_score,
            "segmentation_risk_score": segmentation_risk_score,
            "has_authorized_ticket": has_authorized_ticket,
            "num_changed_fields": num_changed_fields,
            "risk_label": target_risk_label,
            "risk_num": risk_num
        })
        
    feat_df = pd.DataFrame(features)
    feat_df.to_csv(os.path.join(PROCESSED_DIR, "ml_features.csv"), index=False)
    print(f"Feature engineering completed. Processed {len(feat_df)} rows for ML.")

# ----------------------------------------------------
# MAIN EXECUTION SCRIPT
# ----------------------------------------------------
if __name__ == "__main__":
    print("Generating synthetic hospital network datasets...")
    devices_df = generate_devices(110)
    devices_df.to_csv(os.path.join(RAW_DIR, "devices_raw.csv"), index=False)
    
    tickets_df = generate_tickets(devices_df, 5200)
    tickets_df.to_csv(os.path.join(RAW_DIR, "change_tickets_raw.csv"), index=False)
    
    configs_df = generate_configurations(devices_df, tickets_df, 10500)
    configs_df.to_csv(os.path.join(RAW_DIR, "configurations_raw.csv"), index=False)
    
    rules_df = pd.DataFrame(COMPLIANCE_RULES)
    rules_df.to_csv(os.path.join(RAW_DIR, "compliance_rules_raw.csv"), index=False)
    
    events_df = generate_events(devices_df, 20500)
    events_df.to_csv(os.path.join(RAW_DIR, "network_events_raw.csv"), index=False)
    
    print("Raw dataset generation complete.")
    
    # Run data cleaning and feature pipeline
    d_clean, c_clean, t_clean, r_clean = run_data_cleaning_pipeline(
        devices_df, configs_df, tickets_df, rules_df, events_df
    )
    
    run_feature_engineering(d_clean, c_clean, t_clean)
    print("All datasets generated, cleaned, and processed successfully!")
