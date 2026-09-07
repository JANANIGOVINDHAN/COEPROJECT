class RemediationEngineService:
    REMEDIATION_KNOWLEDGE_BASE = {
        "telnet_enabled": {
            "action": "Disable Telnet daemon on network control plane and enforce SSH v2 with TACACS+/RADIUS integration.",
            "cli_command": "no service telnet\nip ssh version 2",
            "reason": "Telnet transmits administrative credentials and device config in cleartext across the network.",
            "security_benefit": "Eliminates plain-text credential sniffing and unauthorized remote shell hijack.",
            "priority": "HIGH",
            "rollback_plan": "Re-enable Telnet temporarily via serial console if SSH key agreement fails during maintenance.",
            "manual_approval_required": True
        },
        "logging_enabled": {
            "action": "Re-enable syslog daemon and verify destination host 10.0.0.51 over UDP/514.",
            "cli_command": "logging enable\nlogging host 10.0.0.51",
            "reason": "Disabled logging obscures administrative actions and prevents SIEM correlation of security events.",
            "security_benefit": "Restores central audit log tracking for HIPAA and security compliance.",
            "priority": "HIGH",
            "rollback_plan": "Verify network route to syslog server before applying config change.",
            "manual_approval_required": False
        },
        "guest_isolation": {
            "action": "Enforce client isolation on Wireless LAN Controller for Guest SSID.",
            "cli_command": "wlan guest-wifi 1\n client isolation enable",
            "reason": "Non-isolated guest Wi-Fi clients can scan and attack internal medical devices on adjacent network segments.",
            "security_benefit": "Prevents lateral movement from guest devices into clinical networks.",
            "priority": "CRITICAL",
            "rollback_plan": "Ensure internal subnet routing tables isolate VLAN 100.",
            "manual_approval_required": True
        },
        "firewall_policy": {
            "action": "Revert firewall policy to approved template enforcing explicit DEFAULT_DENY.",
            "cli_command": "policy-map GLOBAL_IN\n rule 999 deny ip any any log",
            "reason": "Overly permissive or missing default-deny firewall policies expose clinical subnets.",
            "security_benefit": "Restores defense-in-depth zero-trust network boundaries.",
            "priority": "CRITICAL",
            "rollback_plan": "Save current running config to flash before executing policy commit.",
            "manual_approval_required": True
        },
        "dhcp_snooping": {
            "action": "Enable DHCP Snooping globally and configure trusted uplink trunk interfaces.",
            "cli_command": "ip dhcp snooping\nip dhcp snooping vlan 10,20,30",
            "reason": "Disabled DHCP snooping allows rogue DHCP servers to perform Man-in-the-Middle (MitM) redirection.",
            "security_benefit": "Prevents rogue default gateway advertisements.",
            "priority": "MEDIUM",
            "rollback_plan": "Verify trusted port bindings prior to enabling enforcement.",
            "manual_approval_required": False
        }
    }

    @staticmethod
    def get_remediation(field_name: str, current_value: str) -> dict:
        kb_item = RemediationEngineService.REMEDIATION_KNOWLEDGE_BASE.get(field_name)
        if kb_item:
            return kb_item

        return {
            "action": f"Revert attribute '{field_name}' to baseline approved standard state.",
            "cli_command": f"# Review device manual configuration for setting: {field_name}",
            "reason": f"Configuration setting '{field_name}' deviates from baseline policy.",
            "security_benefit": "Ensures configuration standardization across hospital network sites.",
            "priority": "MEDIUM",
            "rollback_plan": "Perform configuration backup before manual edit.",
            "manual_approval_required": True
        }
