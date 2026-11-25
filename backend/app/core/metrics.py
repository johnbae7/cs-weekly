"""Prometheus 지표 정의. 이름·라벨은 docs/contract.md 5절과 같아야 합니다 (바꾸면 박준우 리뷰).

route 라벨에는 실제 주소가 아니라 경로 틀(/api/reports/{report_id})을 넣습니다.
"""

from prometheus_client import Counter, Histogram

HTTP_REQUESTS = Counter("cs_http_requests_total", "HTTP 요청 수", ["method", "route", "status"])
HTTP_LATENCY = Histogram("cs_http_request_duration_seconds", "HTTP 응답 시간(초)", ["method", "route"])
HTTP_ERRORS = Counter("cs_http_errors_total", "HTTP 오류 수(5xx)", ["method", "route"])

LLM_LATENCY = Histogram(
    "cs_llm_request_duration_seconds",
    "LLM 호출 응답 시간(초)",
    ["provider"],
    buckets=(1, 2, 5, 10, 20, 30, 60, 120),
)
LLM_REQUESTS = Counter("cs_llm_requests_total", "LLM 호출 수", ["provider", "result"])  # success / failure
LLM_FAILURES = Counter(
    "cs_llm_failures_total", "LLM 호출 실패 수", ["provider", "reason"]
)  # timeout / error / invalid_output / no_key
LLM_FALLBACKS = Counter("cs_llm_fallbacks_total", "다음 업체로 넘어간 횟수", ["from_provider"])

SECURITY_EVENTS = Counter("cs_security_events_total", "보안 이벤트 수", ["action", "result"])  # allowed / blocked

# 요청 수에 넣지 않는 경로 (프로브·수집)
SKIP_PATHS = {"/health", "/health/ready", "/metrics"}
