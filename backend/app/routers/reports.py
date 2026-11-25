"""보고서 (W2-06, W3-01~03, F-4·F-5)

TODO(유시웅)
- API-04 POST  /api/reports → 202/403 (작성자, 백그라운드 생성 시작)
- API-05 GET   /api/reports → 200 (역할별 결과 다름)
- API-06 GET   /api/reports/{id} → 200/403/404
- API-07 PATCH /api/reports/{id} → 200/403/409 (검토자, PENDING_APPROVAL, 문장 절 1·4·6만)
- API-08 POST  /api/reports/{id}/approve → 200/403/409 (검토 필요는 사유 확인 필수)
- API-09 POST  /api/reports/{id}/reject → 200/403/409 (사유 필수)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])
