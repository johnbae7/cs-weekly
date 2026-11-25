# 앱 ↔ 인프라 약속값

인프라 배포가 이 문서의 값에 맞춰 설정됩니다.
**이 문서를 바꾸는 PR은 박준우 님을 리뷰어로 지정**합니다 (`.github/CODEOWNERS`).
바꾸는 순서: 이 문서 → 앱 코드 → 인프라 저장소 설정.

## 1. 저장소 역할

| 저장소 | 담는 것 | 담당 |
|---|---|---|
| 앱 저장소 (이 저장소) | 백엔드·프론트 코드, Dockerfile, 이미지 빌드·레지스트리 업로드 워크플로(`.github/workflows/`) | 김선·유시웅 (빌드 워크플로는 박준우) |
| 인프라 저장소 (별도) | Kubernetes 배포 설정, 모니터링·알림 설정, 운영 문서 | 박준우 |

흐름: 앱 저장소에 push → 앱 저장소 워크플로가 이미지 빌드 → 레지스트리 업로드 → 인프라 저장소 설정으로 배포

## 2. 이미지

| 이미지 | Dockerfile (빌드 폴더) | 포트 | 실행 사용자 |
|---|---|---|---|
| backend | `backend/Dockerfile` (`backend/`) | 8000 | UID 10001 (root 아님) |
| frontend | `frontend/Dockerfile` (`frontend/`) | 8080 | UID 101 (root 아님, nginx-unprivileged) |

- 두 포트 모두 1024 이상입니다.
- 실행 사용자를 숫자 UID로 지정해, Kubernetes `runAsNonRoot: true` 검사를 통과할 수 있게 했습니다.

## 3. 경로

| 경로 | 받는 곳 | 용도 | 외부 공개 |
|---|---|---|---|
| `/api/...` | backend:8000 | 업무 API. Ingress는 경로를 바꾸지 않고 그대로 전달 | 공개 |
| `/` | frontend:8080 | 화면 | 공개 |
| `/health` | backend | **프로세스 상태만** 확인, DB 확인 안 함 → 항상 200 (liveness) | 비공개 |
| `/health/ready` | backend | **DB 연결 확인** → 정상 200, 실패 503 (readiness) | 비공개 |
| `/metrics` | backend | Prometheus 지표 | 클러스터 내부만 |
| `/` | frontend | 프론트 상태 확인 → 200 | 비공개 |

- 프론트는 백엔드를 **상대 경로 `/api`**로만 호출합니다. 도메인이나 포트를 코드에 쓰지 않습니다.
- 개발 중에는 Vite 프록시가, 배포 후에는 Ingress가 `/api`를 백엔드로 보냅니다.

## 4. 환경 변수 (backend)

🔒 = 비밀값 → Kubernetes Secret·GitHub Secrets에만 둡니다. 저장소·로그·이미지에 넣지 않습니다.
나머지는 ConfigMap에 둡니다.

| 변수 | 비밀값 | 예시·기본값 | 설명 |
|---|---|---|---|
| `DATABASE_URL` | 🔒 | `postgresql+psycopg://<user>:<pw>@<host>:5432/<db>` | DB 연결 문자열 (비밀번호 포함). 개발 Supabase, 배포 RDS 앱 전용 계정 |
| `JWT_SECRET` | 🔒 | (임의 문자열) | 로그인 토큰 서명 키 |
| `ANTHROPIC_API_KEY` | 🔒 | | Claude API 키 |
| `GEMINI_API_KEY` | 🔒 | | Gemini API 키 |
| `GROQ_API_KEY` | 🔒 | | Groq API 키 |
| `SMTP_USER`, `SMTP_PASSWORD` | 🔒 | | Gmail SMTP 대체 시에만 |
| `LLM_PROVIDER_ORDER` | | `claude,gemini,groq` | LLM 실패 전환 순서 |
| `CLAUDE_MODEL`, `GEMINI_MODEL`, `GROQ_MODEL` | | (Q-5 결정) | 업체별 모델 이름 |
| `LLM_TIMEOUT` | | `60` | LLM 호출 시간 제한(초) |
| `MAIL_PROVIDER` | | `ses` | `ses` 또는 `smtp` |
| `MAIL_FROM` | | | SES 인증 발신 주소 |
| `AWS_REGION` | | `ap-northeast-2` | SES·RDS 리전 |
| `APP_BASE_URL` | | (Ingress 주소) | 메일 맨 아래 서비스 링크 |

- SES 호출 권한: IAM 역할로 주면 키가 필요 없습니다. 액세스 키로 주면 `AWS_ACCESS_KEY_ID`·`AWS_SECRET_ACCESS_KEY`를 🔒로 추가합니다. 어느 쪽인지는 박준우 님이 정합니다.
- frontend 컨테이너는 환경 변수가 없습니다 (빌드 결과 정적 파일만).

## 5. `/metrics` 지표

| 지표 | 종류 | 라벨 | 뜻 |
|---|---|---|---|
| `cs_http_requests_total` | Counter | `method`, `route`, `status` | 요청 수 |
| `cs_http_request_duration_seconds` | Histogram | `method`, `route` | 응답 시간(초) |
| `cs_http_errors_total` | Counter | `method`, `route` | 오류 수 (5xx) |
| `cs_llm_request_duration_seconds` | Histogram | `provider` | LLM 호출 응답 시간(초) |
| `cs_llm_requests_total` | Counter | `provider`, `result` | LLM 호출 수 (`result`: `success`/`failure`) |
| `cs_llm_failures_total` | Counter | `provider`, `reason` | LLM 실패 수 (`reason`: `timeout`/`error`/`invalid_output`/`no_key`) |
| `cs_llm_fallbacks_total` | Counter | `from_provider` | 다음 업체로 넘어간 횟수 |
| `cs_security_events_total` | Counter | `action`, `result` | 보안 이벤트 (`result`: `allowed`/`blocked`) |

- `route`는 실제 주소가 아니라 경로 틀(예: `/api/reports/{report_id}`)이라 라벨 종류가 늘어나지 않습니다.
- `/health`, `/health/ready`, `/metrics` 호출은 요청 수에 넣지 않습니다.
- 403·409 같은 권한·상태 거부는 `status` 라벨과 `cs_security_events_total`로 봅니다.
- 이 밖에 `prometheus_client` 기본 지표(프로세스 CPU·메모리 등)가 함께 나옵니다.

## 6. 로그

- 파일로 남기지 않고 컨테이너 표준 출력으로 내보냅니다.
- **backend:** 접속 로그는 stdout, 오류 로그는 stderr(uvicorn 기본)이며 둘 다 컨테이너 로그로 수집됩니다. `PYTHONUNBUFFERED=1`로 바로 출력됩니다.
- **frontend:** nginx 접속·오류 로그를 stdout·stderr로 내보냅니다.
- 로그에 개인정보, API 키, 연결 문자열을 남기지 않습니다.

## 7. 종료 처리 (SIGTERM)

- **backend:** uvicorn이 SIGTERM을 받으면 새 요청을 받지 않고, 처리 중인 요청을 마친 뒤 종료합니다. 최대 20초를 기다립니다(`--timeout-graceful-shutdown 20`).
  → Kubernetes `terminationGracePeriodSeconds`는 30초 이상으로 둡니다.
- **생성 중이던 보고서:** 백그라운드 작업이 종료로 끊기면, 재시작 때 `GENERATION_FAILED`로 바뀝니다(AD-2). 작성자가 다시 생성합니다.
- **frontend:** nginx 이미지의 기본 정상 종료 신호로 처리 중 연결을 마칩니다.

## 8. DB 마이그레이션

| 항목 | 값 |
|---|---|
| 도구 | Alembic |
| 실행 명령 | `alembic upgrade head` |
| 실행 위치 | backend 이미지 안 `/app` 폴더 (`DATABASE_URL` 필요) |
| 실행 시점 | 새 버전을 배포하기 전 1회. 같은 backend 이미지로 Kubernetes Job 또는 initContainer에서 실행 |
| 개발 중 | 로컬 `backend/` 폴더에서 같은 명령으로 개발 Supabase에 적용 |
| 새 마이그레이션 만들기 (유시웅) | `alembic revision --autogenerate -m "설명"` |

## 9. 변경 기록

| 날짜 | 변경 | 작성 |
|---|---|---|
| 2026-11-25 | 최초 작성 (박준우 요청 반영: health 분리, 비밀값 표시, 지표, 상대 경로, 로그·비루트·포트, SIGTERM, 마이그레이션) | 김선 |
