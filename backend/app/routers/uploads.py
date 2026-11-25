"""업로드 (W2-05, F-3)

TODO(유시웅)
- API-02 POST /api/uploads → 201/400/403/413 (작성자). 응답: 행 수·오류 행
- API-14 GET  /api/uploads → 200/403 (작성자는 본인 것만, 검토자)
- API-03 GET  /api/uploads/{id}/consults → 200/403 (작성자·검토자, 공격 A1-1 대상)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/uploads", tags=["uploads"])
