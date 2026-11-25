# 백엔드 이미지 (docs/contract.md 2·6·7·8절)
# - root가 아닌 숫자 UID로 실행 (runAsNonRoot 검사 통과), 포트 8000
# - 로그는 표준 출력, SIGTERM 시 처리 중 요청 마무리(최대 20초)
# - 마이그레이션: 같은 이미지에서 `alembic upgrade head`
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic.ini ./
COPY migrations ./migrations

RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser
USER 10001

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "20"]
