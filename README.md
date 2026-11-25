# CS 위클리 (존배 CS 주간리포트)

쇼핑몰 CS팀이 상담기록 파일(CSV·엑셀)을 올리면 AI가 요약·분석해 주간리포트를 만들고,
CS팀장이 검토·승인하면 수신자에게 메일로 보내는 서비스입니다.

3차 합반 프로젝트 · 팀 존배 (2026-11-24 ~ 2026-12-28)

| 이름 | 직군 | 폴더 |
|---|---|---|
| 김선 | 풀스택(팀장) · 프론트엔드 | `frontend/`, `docs/` |
| 유시웅 | 풀스택 · 백엔드 | `backend/`, `data/` |
| 박준우 | 인프라 | 별도 인프라 저장소 |
| 김찬규 | 보안 | `security/` |

## 처음 시작하는 팀원

1. `CLAUDE.md`(공통 규칙)와 내 폴더의 `CLAUDE.md`를 읽습니다.
2. `docs/CONTRIBUTING.md`의 순서대로 저장소를 내려받고 브랜치를 만듭니다.
3. 작업 → PR → CI 통과 → 본인 머지 → 시트 「주차별 업무」 갱신.

## 폴더 구조

```
.
├── CLAUDE.md               공통 규칙 (약속값, 금지 사항, Git 규칙)
├── .env.example            환경 변수 키 목록 (값은 각자 .env에, 커밋 금지)
├── .github/                PR·이슈 템플릿, CODEOWNERS, CI 워크플로
├── docs/                   협업 가이드
├── data/                   가상 상담 데이터 (W47 CSV, W48 엑셀)
├── backend/                FastAPI 백엔드 (유시웅)
├── frontend/               React + Vite 프론트엔드 (김선)
└── security/               위협 모델·공격 시나리오·리포트 (김찬규)
```

이미지 빌드는 이 저장소의 GitHub Actions(박준우 작성)가, 배포 설정(Kubernetes·모니터링)은 박준우 님이 관리하는 **별도 인프라 저장소**가 맡습니다. 둘 사이의 약속값은 `docs/contract.md`에 있습니다.

## 로컬 실행

```bash
# 1) 환경 변수
cp .env.example .env        # 값 채우기 (커밋 금지)
# DB: 개발 중에는 팀 공용 Supabase 연결 문자열 사용 (배포는 Amazon RDS, 클러스터에서만 접속 가능)

# 2) 백엔드 (터미널 1)
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3) 프론트엔드 (터미널 2)
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

## 환경 변수

이름, 비밀값 여부, 예시는 `docs/contract.md` 4절을 봅니다. 값은 `.env`(개발)와 Kubernetes Secret(배포)에만 넣고 커밋하지 않습니다.

## DB 마이그레이션

```bash
cd backend
alembic upgrade head      # DATABASE_URL에 연결된 DB에 테이블 적용
```
