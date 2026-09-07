from fastapi.testclient import TestClient
from backend.main import app
from backend.services.risk_engine import RiskScoringEngine

client = TestClient(app)

def test_drift_scan_and_findings():
    res = client.post("/drift/scan")
    assert res.status_code == 200
    scan_res = res.json()
    assert "scan_id" in scan_res
    assert scan_res["devices_scanned"] > 0

    res_findings = client.get("/drift/findings")
    assert res_findings.status_code == 200
    findings = res_findings.json()
    assert len(findings) > 0

def test_risk_score_calculation():
    score, severity, breakdown = RiskScoringEngine.calculate_risk_score(
        field_name="telnet_enabled",
        auth_status="Unauthorized",
        compliance_status="Violation",
        site_criticality=1.0,
        anomaly_score=80.0,
        affected_devices_count=2
    )
    assert score >= 75.0
    assert severity == "CRITICAL"
    assert "security_score" in breakdown
