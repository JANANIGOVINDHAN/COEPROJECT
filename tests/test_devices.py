from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_sites():
    res = client.get("/sites")
    assert res.status_code == 200
    sites = res.json()
    assert len(sites) >= 10

def test_get_devices():
    res = client.get("/devices")
    assert res.status_code == 200
    devs = res.json()
    assert len(devs) > 50
