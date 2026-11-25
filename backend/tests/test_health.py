from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_is_ok_without_db():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ready_is_503_without_db(monkeypatch):
    monkeypatch.setattr("app.routers.health.db_is_ready", lambda: False)
    res = client.get("/health/ready")
    assert res.status_code == 503


def test_ready_is_200_with_db(monkeypatch):
    monkeypatch.setattr("app.routers.health.db_is_ready", lambda: True)
    res = client.get("/health/ready")
    assert res.status_code == 200


def test_metrics_exposed_without_prefix():
    res = client.get("/metrics")
    assert res.status_code == 200
