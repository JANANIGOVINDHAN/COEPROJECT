import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.database import SessionLocal
from backend.models.drift import DriftFinding
from backend.services.finding_lifecycle import FindingLifecycleService
from backend.services.trend_analyzer import TrendAnalyzerService

client = TestClient(app)

def test_phase2_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["phase"] == "PHASE_2_ACTIVE"

def test_phase2_ml_metrics_endpoint():
    response = client.get("/api/ml/metrics")
    assert response.status_code == 200
    metrics = response.json()
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "confusion_matrix" in metrics
    assert "feature_importances" in metrics
    assert metrics["model_health"] == "OPTIMAL"

def test_phase2_dashboard_trends_endpoint():
    response = client.get("/dashboard/trends")
    assert response.status_code == 200
    trends = response.json()
    assert "scan_history" in trends
    assert "status_breakdown" in trends
    assert "metrics" in trends
    assert "site_risk_matrix" in trends
    assert "mttr_hours" in trends["metrics"]

def test_phase2_finding_status_lifecycle():
    db = SessionLocal()
    try:
        # Fetch an active finding
        finding = db.query(DriftFinding).first()
        assert finding is not None
        finding_id = finding.finding_id

        # Update status to ACKNOWLEDGED
        res = client.patch(
            f"/drift/findings/{finding_id}/status",
            json={"status": "ACKNOWLEDGED", "notes": "Phase 2 test acknowledgment"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ACKNOWLEDGED"

        # Update status to INVALID state (error test)
        err_res = client.patch(
            f"/drift/findings/{finding_id}/status",
            json={"status": "INVALID_STATE_TEST"}
        )
        assert err_res.status_code == 400

    finally:
        db.close()

def test_phase2_remediation_execution():
    db = SessionLocal()
    try:
        finding = db.query(DriftFinding).first()
        assert finding is not None
        finding_id = finding.finding_id

        res = client.post(f"/drift/findings/{finding_id}/remediate")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "REMEDIATED"
        assert data["remediation_applied"] is True
    finally:
        db.close()

def test_phase2_ml_retrain_endpoint():
    response = client.post("/api/ml/retrain")
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "SUCCESS"
    assert "metrics" in res
