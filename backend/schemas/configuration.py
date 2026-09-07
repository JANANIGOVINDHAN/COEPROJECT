from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConfigurationOut(BaseModel):
    id: int
    config_id: str
    device_id: str
    site_id: str
    hostname: str
    device_type: str
    firmware_version: Optional[str] = None
    vlan_configuration: Optional[str] = None
    allowed_vlans: Optional[str] = None
    native_vlan: Optional[int] = 1
    ip_address: Optional[str] = None
    subnet: Optional[str] = None
    routing_protocol: Optional[str] = None
    firewall_policy: Optional[str] = None
    acl_rules: Optional[str] = None
    ssh_enabled: Optional[str] = "true"
    telnet_enabled: Optional[str] = "false"
    https_enabled: Optional[str] = "true"
    snmp_version: Optional[str] = "v3"
    ntp_enabled: Optional[str] = "true"
    logging_enabled: Optional[str] = "true"
    syslog_server: Optional[str] = None
    password_policy: Optional[str] = "ENFORCED"
    encryption_enabled: Optional[str] = "true"
    port_security: Optional[str] = "true"
    bpdu_guard: Optional[str] = "true"
    dhcp_snooping: Optional[str] = "true"
    guest_isolation: Optional[str] = "true"
    network_segmentation: Optional[str] = "true"
    backup_enabled: Optional[str] = "true"
    configuration_timestamp: datetime

    class Config:
        from_attributes = True
