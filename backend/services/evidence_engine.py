class EvidenceEngineService:
    @staticmethod
    def generate_evidence(
        device_id: str,
        hostname: str,
        site_name: str,
        field_name: str,
        baseline_val: str,
        current_val: str,
        timestamp: str,
        ticket_id: str | None,
        auth_status: str,
        violated_rule: str | None,
        risk_score: float,
        risk_breakdown: dict
    ) -> str:
        ticket_str = f"Ticket {ticket_id} (Approved)" if ticket_id and auth_status == "Authorized" else "No valid approved ticket found"
        rule_str = f"Compliance Rule {violated_rule} violated" if violated_rule else "No explicit rule violation"
        
        evidence = (
            f"=== DRIFT EVIDENCE FINDING ===\n"
            f"Device: {hostname} ({device_id})\n"
            f"Site: {site_name}\n"
            f"Changed Field: '{field_name}'\n"
            f"Approved Baseline: {baseline_val}\n"
            f"Current Active Config: {current_val}\n"
            f"Timestamp Detected: {timestamp}\n"
            f"Ticket Authorization: {auth_status} - {ticket_str}\n"
            f"Compliance Status: {rule_str}\n"
            f"Calculated Composite Risk: {risk_score}/100\n"
            f"Risk Factor Breakdown:\n"
            f"  - Security Impact: {risk_breakdown.get('security_score')}/100\n"
            f"  - Compliance Violation: {risk_breakdown.get('compliance_score')}/100\n"
            f"  - Authorization Deficit: {risk_breakdown.get('authorization_score')}/100\n"
            f"  - Site Criticality: {risk_breakdown.get('site_criticality')}/100\n"
            f"  - Anomaly Score: {risk_breakdown.get('anomaly_score')}/100\n"
            f"  - Blast Radius: {risk_breakdown.get('blast_radius')}/100\n"
            f"Detection Context: Unsanctioned drift in key network setting '{field_name}' exposes high operational or cyber exposure in hospital network infrastructure."
        )
        return evidence
