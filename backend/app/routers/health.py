"""상태 확인·지표 (API-12, API-13, API-16). /api 접두사 없이 등록합니다.

- /health       : 생존 여부만. DB를 보지 않음 → Kubernetes liveness probe
- /health/ready : DB 연결 포함 → Kubernetes readiness probe
분리 여부는 박준우 님 최종 확인 대기 (시트에는 분리안 반영).
"""

from fastapi import APIRouter, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.core.database import db_is_ready

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/health/ready")
def health_ready(response: Response) -> dict:
    if db_is_ready():
        return {"status": "ready", "db": "ok"}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "not_ready", "db": "unavailable"}


@router.get("/metrics")
def metrics() -> Response:
    """API-13: Prometheus 지표. Ingress로 외부 공개하지 않음 (클러스터 내부 전용)."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
