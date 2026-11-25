"""Alembic 실행 환경. DATABASE_URL 환경 변수로 접속합니다 (개발 Supabase, 배포 RDS 공통)."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

import app.models  # noqa: F401  모델을 불러와 metadata에 등록
from app.core.config import get_settings
from app.core.database import normalize_db_url
from app.models.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _url() -> str:
    url = normalize_db_url(get_settings().database_url)
    if not url:
        raise RuntimeError("DATABASE_URL 환경 변수가 없습니다.")
    return url


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
