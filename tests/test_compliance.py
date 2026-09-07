from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_compliance_rules():
    res = client.get("/compliance/rules")
    assert res.status_code == 200
    rules = res.json()
    assert len(rules) >= 30

def test_get_tickets():
    res = client.get("/tickets")
    assert res.status_code == 200
    tickets = res.json()
    assert len(tickets) > 0
