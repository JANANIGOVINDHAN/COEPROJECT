from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from backend.core.database import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True, nullable=False)
    site_id = Column(String, index=True, nullable=False)
    hostname = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    firmware_version = Column(String, nullable=True)
    
    # Configuration Details
    vlan_configuration = Column(Text, nullable=True)
    allowed_vlans = Column(Text, nullable=True)
    native_vlan = Column(Integer, default=1)
    ip_address = Column(String, nullable=True)
    subnet = Column(String, nullable=True)
    routing_protocol = Column(String, nullable=True)
    static_routes = Column(Text, nullable=True)
    ospf_enabled = Column(String, default="false")
    bgp_enabled = Column(String, default="false")
    firewall_policy = Column(Text, nullable=True)
    acl_rules = Column(Text, nullable=True)
    ssh_enabled = Column(String, default="true")
    telnet_enabled = Column(String, default="false")
    https_enabled = Column(String, default="true")
    snmp_version = Column(String, default="v3")
    snmp_community = Column(String, nullable=True)
    ntp_enabled = Column(String, default="true")
    ntp_server = Column(String, nullable=True)
    logging_enabled = Column(String, default="true")
    syslog_server = Column(String, nullable=True)
    dns_server = Column(String, nullable=True)
    password_policy = Column(String, default="ENFORCED")
    encryption_enabled = Column(String, default="true")
    port_security = Column(String, default="true")
    bpdu_guard = Column(String, default="true")
    dhcp_snooping = Column(String, default="true")
    spanning_tree = Column(String, default="MSTP")
    guest_isolation = Column(String, default="true")
    network_segmentation = Column(String, default="true")
    admin_access = Column(String, default="SSH_TACACS")
    backup_enabled = Column(String, default="true")
    
    configuration_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
