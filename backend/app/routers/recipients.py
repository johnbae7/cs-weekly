"""수신자 허용 목록 (F-5)

TODO(유시웅)
- API-11 GET·PUT /api/recipients → 200/403 (검토자만). 작성자가 호출하면 403 + 보안 이벤트(A4-2)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/recipients", tags=["recipients"])
