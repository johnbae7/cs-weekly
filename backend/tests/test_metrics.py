from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

EXPECTED = [
    "cs_http_requests_total",
    "cs_http_request_duration_seconds",
    "cs_http_errors_total",
    "cs_llm_request_duration_seconds",
    "cs_llm_requests_total",
    "cs_llm_failures_total",
    "cs_llm_fallbacks_total",
    "cs_security_events_total",
]


def test_contract_metrics_exposed():
    client.get("/api/not-found")
    body = client.get("/metrics").text
    for name in EXPECTED:
        assert name in body, name


def test_request_counted_with_route_template():
    client.get("/api/not-found")
    body = client.get("/metrics").text
    assert 'cs_http_requests_total{method="GET",route="unmatched",status="404"}' in body


def test_probes_not_counted():
    client.get("/health")
    body = client.get("/metrics").text
    assert 'route="/health"' not in body
