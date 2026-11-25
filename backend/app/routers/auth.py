"""로그인 (W2-04, F-6)

TODO(유시웅)
- API-01 POST /api/auth/login → 200/401. 토큰에 역할·그룹 포함
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])
