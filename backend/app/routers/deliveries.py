"""전달 (W3-03, F-5)

TODO(유시웅)
- API-10 POST /api/reports/{id}/deliveries → 202/403/409 (검토자, APPROVED 재확인, 전달 가드레일)
- API-15 GET  /api/reports/{id}/deliveries → 200/403/404 (검토자)
경로가 /reports/{id}/deliveries 이므로 이 라우터는 prefix 없이 전체 경로를 적습니다.
"""

from fastapi import APIRouter

router = APIRouter(tags=["deliveries"])
