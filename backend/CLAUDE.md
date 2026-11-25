# backend/ — 풀스택 백엔드 (담당: 유시웅)

루트 `CLAUDE.md`를 먼저 읽은 뒤 이 파일을 따릅니다.

## 1. 맡는 범위

| 업무 ID | 내용 | 연결 요구사항 |
|---|---|---|
| W1-03 | 개발용 Supabase 프로젝트 생성, 팀원 초대 (DB 연결만 사용) | F-2 |
| W1-04 | DB 설계(테이블 6개), API 초안 | F-2 |
| W1-07 | 가상 상담 데이터 생성 스크립트(`scripts/generate_consults.py`) | F-8 |
| W2-02 | 백엔드 골격, 테이블 생성 스크립트(Supabase·RDS 공용), `.env.example`, `/health`·`/health/ready` | F-9 |
| W2-03 | `scripts/seed.py`: 테스트 계정 6개, 수신 그룹·메일 주소 | F-8 |
| W2-04 | 로그인·역할 권한 | F-6 |
| W2-05 | CSV·엑셀 업로드, 업로드 목록 | F-3 |
| W2-06 | 보고서 생성 요청·상태 조회, Swagger | F-4 |
| W3-01 | SQL 집계 + LLM 요약·보고서 생성 | F-4 |
| W3-02 | 검토 필요 판정 R1~R4, 승인 요청 메일 | F-5 |
| W3-03 | 승인·반려, 메일 발송, 전달 이력, 재전달 | F-5 |
| W3-10 | 가드레일 (김찬규와 공동, `services/guardrails.py`) | S-5 |
| W4-02 | 핵심 API 테스트 | F-11 |
| W4-03 | 보안 리포트 취약점 1건 이상 개선·재검증 | F-10 |

`app/templates/mail/`은 김선 담당(W3-04)입니다. 템플릿에 넘기는 변수 이름을 바꾸면 김선에게 알립니다.

## 2. 폴더 구조 (시트 「풀스택아키텍처」 백엔드 모듈 구성과 동일)

```
backend/
├── app/
│   ├── main.py              FastAPI 앱, 라우터 등록, 시작 시 AD-2 처리
│   ├── core/
│   │   ├── config.py        환경 변수 읽기 (pydantic-settings)
│   │   ├── database.py      SQLAlchemy 엔진·세션
│   │   ├── security.py      JWT 발급·확인, 비밀번호 해시
│   │   └── permissions.py   권한 검사 함수 1개: 401 → 403 역할 → 403 소유·그룹 → 409 상태
│   ├── routers/             요청을 받아 services 호출 (로직은 services에)
│   │   ├── auth.py          API-01
│   │   ├── uploads.py       API-02, 03, 14
│   │   ├── reports.py       API-04 ~ 09
│   │   ├── deliveries.py    API-10, 15
│   │   ├── recipients.py    API-11
│   │   └── health.py        API-12, 13, 16
│   ├── services/
│   │   ├── upload_parser.py CSV 인코딩 판별(UTF-8·BOM·CP949), 엑셀 첫 시트, 15개 열 검증, = 시작 셀은 문자열
│   │   ├── aggregator.py    숫자 절(2·3·5) SQL 집계
│   │   ├── llm_client.py    Claude → Gemini → Groq 실패 전환, 업체당 1회 시도, 시간 제한
│   │   ├── guardrails.py    입력·출력·전달 가드레일 (김찬규 공동)
│   │   ├── review_rules.py  R1~R4 판정, 사유 저장
│   │   ├── report_builder.py Jinja2 HTML(autoescape), 메일·화면 같은 템플릿
│   │   ├── mailer.py        SES 또는 SMTP 발송, deliveries 기록
│   │   └── security_log.py  security_events 저장, 지표 카운터 증가
│   ├── models/              SQLAlchemy 모델 (테이블 6개)
│   ├── schemas/             Pydantic 요청·응답 형식
│   └── templates/mail/      메일 HTML (김선)
├── scripts/                 seed.py, generate_consults.py
├── tests/                   pytest
├── Dockerfile
└── requirements*.txt
```

## 3. API 목록 (모두 `/api` 접두사, 상태 확인·지표만 접두사 없음)

| ID | 메소드·경로 | 역할 | 상태코드 |
|---|---|---|---|
| API-01 | POST `/api/auth/login` | 미인증 | 200/401 |
| API-02 | POST `/api/uploads` | 작성자 | 201/400/403/413 |
| API-03 | GET `/api/uploads/{id}/consults` | 작성자·검토자 | 200/403 |
| API-04 | POST `/api/reports` | 작성자 | 202/403 |
| API-05 | GET `/api/reports` | 전체(역할별 결과 다름) | 200 |
| API-06 | GET `/api/reports/{id}` | 역할·그룹 일치 | 200/403/404 |
| API-07 | PATCH `/api/reports/{id}` | 검토자(PENDING_APPROVAL, 문장 절만) | 200/403/409 |
| API-08 | POST `/api/reports/{id}/approve` | 검토자 | 200/403/409 |
| API-09 | POST `/api/reports/{id}/reject` | 검토자(사유 필수) | 200/403/409 |
| API-10 | POST `/api/reports/{id}/deliveries` | 검토자(상태 재확인) | 202/403/409 |
| API-11 | GET·PUT `/api/recipients` | 검토자(허용 목록) | 200/403 |
| API-12 | GET `/health` | 미인증, 생존 여부만 | 200 |
| API-13 | GET `/metrics` | 클러스터 내부 | 200 |
| API-14 | GET `/api/uploads` | 작성자(본인 것만)·검토자 | 200/403 |
| API-15 | GET `/api/reports/{id}/deliveries` | 검토자 | 200/403/404 |
| API-16 | GET `/health/ready` | 미인증, DB 연결 포함 | 200/503 |

## 4. 반드시 지킬 것

- **DB는 개발 Supabase → 배포 RDS.** SQLAlchemy 표준 기능만 씁니다. Supabase 전용 기능(Data API·Auth·Storage·RLS 정책 의존)은 쓰지 않습니다. 테이블 생성은 스크립트 하나로 두 DB에 똑같이 적용합니다.
- **개발 Supabase 테이블도 RLS를 켭니다**(정책 없이). 켜지 않으면 anon 키로 Data API에서 테이블이 보입니다.
- **권한 검사는 `core/permissions.py`의 함수 하나로만.** 라우터마다 따로 만들지 않습니다. 실패 시 `security_log`에 기록합니다.
- **숫자 절(2·3·5)은 SQL 집계값만.** LLM 출력에서 숫자를 가져오지 않습니다. PATCH는 문장 절(1·4·6)만 받습니다.
- **LLM 실패 전환.** `LLM_PROVIDER_ORDER` 순서(claude → gemini → groq)로 업체당 1회 시도, 시간 제한 초과·오류 시 다음 업체. 키가 비어 있는 업체는 건너뜀. 3곳 모두 실패하면 `GENERATION_FAILED`(E-2). 어느 업체가 답했는지 로그·지표에 남김(박준우 W3-06 패널).
- **업체가 바뀌어도 같은 출력 형식.** 세 업체 모두 같은 프롬프트·같은 출력 형식(JSON)을 쓰고, 형식이 깨진 응답은 실패로 보고 다음 업체로 넘깁니다.
- **LLM 호출 전 마스킹.** LLM에는 문의유형·상품명·문의내용·처리내용만 보냅니다. 고객명·전화·이메일·주소·주문번호·상담원은 보내지 않습니다.
- **프롬프트에서 상담 내용은 구분자 안의 데이터로만.** 지시문과 섞지 않습니다.
- **근거 상담ID 확인.** LLM이 낸 ID가 실제 해당 업로드에 있는지 코드로 확인합니다.
- **전달 API에서 상태를 다시 확인.** `APPROVED`가 아니면 409. 수신 주소는 recipients 테이블에서만 가져옵니다.
- **AD-2.** 앱 시작 시 오래된 `GENERATING`을 `GENERATION_FAILED`로 바꿉니다 (`main.py` lifespan).
- **엑셀·CSV의 `=`로 시작하는 셀은 문자열로 저장** (U-2, 수식 인젝션).
- **업로드 제한**: 5MB, 첫 시트, 15개 열, 확장자와 실제 형식 둘 다 확인 (U-1).
- R2·R3 기준값은 `services/review_rules.py` 맨 위 상수에 모아 둡니다 (Q-6 결정 대기).

## 5. 인프라 인계 체크리스트 (W2-02 비고와 동일, 자세한 값은 `docs/contract.md`)

1. 모든 설정값은 환경 변수 (`.env.example`에 키만)
2. `0.0.0.0`으로 바인딩 (localhost 금지)
3. `/health`(생존 여부만), `/health/ready`(DB 연결 포함) 제공
4. 로컬 파일 저장 금지 (업로드 내용은 DB에만, 임시 파일은 메모리에서 처리)
5. 프론트가 상대 경로 `/api`로 호출할 수 있게 라우터 접두사 `/api`
6. 파드 재시작 시 오래된 GENERATING 처리 (AD-2, E-3)
7. README에 환경 변수 목록 명시 (`docs/contract.md` 4절)
8. `/metrics`에 요청 수·응답 시간·오류 수, LLM 응답 시간·실패 수 (`app/core/metrics.py`, 이름 바꾸지 않기)
9. root가 아닌 사용자(UID 10001)로 실행, 로그는 표준 출력, SIGTERM 시 처리 중 요청 마무리(최대 20초)
10. 테이블 변경은 Alembic 마이그레이션으로만 (`alembic revision --autogenerate`, 적용은 `alembic upgrade head`)

## 6. 로컬 실행·테스트

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp ../.env.example ../.env   # 값 채우기 (커밋 금지)
# DB는 팀 공용 Supabase (DATABASE_URL을 팀 채널에서 받기). RDS는 클러스터에서만 접속 가능
alembic upgrade head       # 개발 Supabase에 테이블 적용
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pytest
```

Swagger: http://localhost:8000/docs

## 7. 테스트 기준 (W4-02, F-11)

핵심 API마다 세 가지를 확인합니다: 정상 / 권한 오류(401·403) / 상태 오류(409).
보안 시나리오(시트 「시나리오」 C)의 기대 결과와 같은 상태코드를 돌려주는지 확인합니다.
