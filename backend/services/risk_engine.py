from backend.core.config import settings

class RiskScoringEngine:
    # Default configurable field weights
    FIELD_WEIGHTS = {
        "telnet_enabled": 1.0,
        "firewall_policy": 1.0,
        "guest_isolation": 0.95,
        "network_segmentation": 0.95,
        "ssh_enabled": 0.90,
        "password_policy": 0.90,
        "encryption_enabled": 0.90,
        "logging_enabled": 0.85,
        "syslog_server": 0.85,
        "dhcp_snooping": 0.85,
        "bpdu_guard": 0.80,
        "ntp_enabled": 0.70,
        "firmware_version": 0.60,
        "snmp_version": 0.75,
        "backup_enabled": 0.50
    }

    @staticmethod
    def calculate_risk_score(
        field_name: str,
        auth_status: str,
        compliance_status: str,
        site_criticality: float = 0.75,
        anomaly_score: float = 20.0,
        affected_devices_count: int = 1
    ) -> tuple[float, str, dict]:
        """
        Calculates composite risk score (0 - 100) and returns (score, severity_label, breakdown)
        """
        # 1. Security field weight score
        field_weight = RiskScoringEngine.FIELD_WEIGHTS.get(field_name, 0.70)
        security_score = field_weight * 100.0

        # 2. Compliance Score (100 if violation, 0 if pass)
        compliance_score = 100.0 if compliance_status == "Violation" else 0.0

        # 3. Authorization Score
        if auth_status == "Unauthorized":
            auth_score = 100.0
        elif auth_status in ["Pending Approval", "Expired Authorization", "Mismatched Ticket"]:
            auth_score = 65.0
        else: # Authorized
            auth_score = 0.0

        # 4. Site Criticality Score (0.0 to 1.0 -> 0 to 100)
        site_crit_score = min(100.0, max(0.0, site_criticality * 100.0))

        # 5. Blast Radius Score (based on affected devices)
        blast_radius = min(100.0, affected_devices_count * 15.0)

        # Composite Formula Calculation
        total_risk = (
            0.30 * security_score +
            0.20 * compliance_score +
            0.15 * auth_score +
            0.15 * site_crit_score +
            0.10 * anomaly_score +
            0.10 * blast_radius
        )

        total_risk = round(min(100.0, max(0.0, total_risk)), 1)

        # Map to severity label based on configurable thresholds
        if total_risk >= settings.CRITICAL_THRESHOLD:
            severity = "CRITICAL"
        elif total_risk >= settings.HIGH_THRESHOLD:
            severity = "HIGH"
        elif total_risk >= settings.MEDIUM_THRESHOLD:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        breakdown = {
            "security_score": round(security_score, 1),
            "compliance_score": round(compliance_score, 1),
            "authorization_score": round(auth_score, 1),
            "site_criticality": round(site_crit_score, 1),
            "anomaly_score": round(anomaly_score, 1),
            "blast_radius": round(blast_radius, 1),
            "final_score": total_risk
        }

        return total_risk, severity, breakdown
