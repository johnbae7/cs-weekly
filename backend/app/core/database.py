"""SQLAlchemy 엔진·세션. PostgreSQL(개발: Supabase, 배포: Amazon RDS)에 백엔드만 직접 연결합니다 (AD-6)."""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

_engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)


def normalize_db_url(url: str) -> str:
    """postgresql:// 또는 postgres:// 로 적어도 설치된 psycopg(3) 드라이버를 쓰게 맞춤."""
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


# DB가 응답하지 않을 때 /health/ready 등이 오래 멈추지 않도록 연결 시간 제한(초)
DB_CONNECT_TIMEOUT = 3


def connect_args_for(url: str) -> dict:
    """PostgreSQL이면 연결 시간 제한을 넣음 (테스트용 sqlite에는 넣지 않음)."""
    if url.startswith("postgresql"):
        return {"connect_timeout": DB_CONNECT_TIMEOUT}
    return {}


def get_engine() -> Engine | None:
    """DATABASE_URL이 없으면 None (DB 없이도 앱과 /health는 뜸)."""
    global _engine
    url = normalize_db_url(get_settings().database_url)
    if not url:
        return None
    if _engine is None:
        _engine = create_engine(url, pool_pre_ping=True, connect_args=connect_args_for(url))
        SessionLocal.configure(bind=_engine)
    return _engine


def db_is_ready() -> bool:
    """/health/ready 용: DB에 SELECT 1이 되는지."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False


def get_db():
    """FastAPI 의존성: 요청마다 세션 하나."""
    get_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
