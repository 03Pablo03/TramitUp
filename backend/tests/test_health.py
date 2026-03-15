from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    response_data = r.json()
    assert "status" in response_data
    # Status can be "healthy", "degraded", or "unhealthy"
    assert response_data["status"] in ["healthy", "degraded", "unhealthy"]
    assert "timestamp" in response_data
    assert "version" in response_data
    assert "environment" in response_data


def test_health_legacy():
    r = client.get("/health-legacy")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["service"] == "tramitup-api"


def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_live():
    r = client.get("/live")
    assert r.status_code == 200
    assert r.json()["status"] == "alive"


def test_classify_requires_json():
    r = client.post("/api/v1/classify", json={})
    assert r.status_code == 422  # missing required field
