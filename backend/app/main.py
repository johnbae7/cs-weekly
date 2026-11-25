"""FastAPI 앱 진입점.

- 업무 API는 settings.api_prefix(/api) 아래에 등록
- /health, /health/ready, /metrics는 접두사 없이 등록 (프로브·Prometheus가 파드에 직접 접근)
- 시작 시 AD-2: 오래된 GENERATING → GENERATION_FAILED
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.config import get_settings
from app.core.metrics import HTTP_ERRORS, HTTP_LATENCY, HTTP_REQUESTS, SKIP_PATHS
from app.routers import auth, deliveries, health, recipients, reports, uploads


def reset_stale_generating() -> None:
    """AD-2 / E-3: 파드가 생성 중에 종료돼 남은 GENERATING 보고서를 GENERATION_FAILED로 바꿈.

    TODO(유시웅): reports 테이블에서 status='GENERATING' 행을 GENERATION_FAILED로 UPDATE
    (DB가 없으면 아무것도 하지 않음)
    """


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_stale_generating()
    yield


settings = get_settings()

app = FastAPI(title="CS 위클리 API", version="0.1.0", lifespan=lifespan)

app.include_router(health.router)
for module in (auth, uploads, reports, deliveries, recipients):
    app.include_router(module.router, prefix=settings.api_prefix)


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", "unmatched")


@app.middleware("http")
async def record_metrics(request: Request, call_next):
    """요청 수·응답 시간·오류 수 기록 (docs/contract.md 5절)."""
    if request.url.path in SKIP_PATHS:
        return await call_next(request)
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        route = _route_template(request)
        HTTP_REQUESTS.labels(request.method, route, "500").inc()
        HTTP_ERRORS.labels(request.method, route).inc()
        HTTP_LATENCY.labels(request.method, route).observe(time.perf_counter() - start)
        raise
    route = _route_template(request)
    HTTP_REQUESTS.labels(request.method, route, str(response.status_code)).inc()
    HTTP_LATENCY.labels(request.method, route).observe(time.perf_counter() - start)
    if response.status_code >= 500:
        HTTP_ERRORS.labels(request.method, route).inc()
    return response
