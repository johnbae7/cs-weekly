"""모든 모델의 DeclarativeBase. Alembic(migrations/env.py)이 이 metadata로 테이블을 만듭니다."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
