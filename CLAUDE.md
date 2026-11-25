# CS 위클리 (존배 CS 주간리포트) — 저장소 공통 규칙

이 파일은 저장소 전체에 적용됩니다. 각 폴더의 `CLAUDE.md`가 분야별 규칙을 더합니다.
작업 전에 **이 파일 + 내 분야 폴더의 CLAUDE.md**를 먼저 읽습니다.

- 계획의 원본은 팀 스프레드시트(「CS위클리 5주 계획 v2」)입니다.
- 시트와 이 문서가 다르면 **시트가 기준**이고, 이 문서를 시트에 맞게 고칩니다.
- 약속값(상태 이름, 역할 키, 환경 변수 이름, API 경로)을 바꾸려면 시트 → CLAUDE.md → 코드 순서로 고치고 전원에게 알립니다.

## 1. 서비스 한 줄

쇼핑몰 CS팀이 상담기록 파일(CSV·엑셀)을 올리면 AI가 요약·분석해 주간리포트를 만들고,
CS팀장이 검토·승인하면 수신자에게 메일로 보낸다. 이슈가 있는 주는 '검토 필요'로 표시한다.

업무 흐름: 업로드(CSV·엑셀) → 형식·열 검증 → DB 저장 → SQL 집계 + AI 요약 → 보고서 생성
→ 검토 필요 판정(R1~R4) → 팀장 검토·승인 → 수신자 메일 전달 → 전달 이력 저장

## 2. MVP 범위 (넘지 않기)

| 항목 | 범위 |
|---|---|
| 보고서 | 1종, 6개 절 (숫자 절 2·3·5는 SQL, 문장 절 1·4·6은 LLM) |
| 역할 | 3개: 작성자 `uploader`, 검토자 `reviewer`, 수신자 `recipient` |
| 수신 그룹 | 3개: `cs`(CS팀), `ops`(상품·물류), `exec`(경영진, 검토 필요 주만) |
| 검토 필요 조건 | 4개: R1 민감정보, R2 상품 불량 집중, R3 유형 급증, R4 수동 요청 |
| 전달 경로 | 1개: **승인 후 메일**만 (자동 전달 없음) |
| 화면 | 4개: 로그인, 보고서 목록, 업로드·생성, 보고서 상세 |
| API | 16개: API-01 ~ API-16 (`backend/CLAUDE.md` 3절) |
| 테이블 | 6개: users, uploads, consults, reports, deliveries, security_events |

범위 밖 기능은 만들기 전에 이슈 로그(시트)에 올리고 팀 결정을 받습니다.
Q-7 권한 기반 RAG는 12/4 결정 전까지 구현하지 않습니다.

## 3. 팀과 폴더 담당

| 폴더·파일 | 담당 | 직군 |
|---|---|---|
| `frontend/` | 김선 | 풀스택(팀장) |
| `backend/` | 유시웅 | 풀스택 |
| `backend/app/templates/mail/` | 김선 | 메일 HTML 템플릿 (W3-04) |
| `backend/app/services/guardrails.py` | 김찬규 + 유시웅 | 가드레일 (W3-10) |
| `backend/Dockerfile`, `frontend/Dockerfile` | 유시웅·김선 (바꿀 때 박준우 리뷰) | 이미지 빌드에 쓰는 파일 |
| `docs/contract.md` | 김선·박준우 | 앱 ↔ 인프라 약속값 (바꿀 때 박준우 리뷰) |
| `.github/workflows/` 이미지 빌드 워크플로 | 박준우 | 인프라 |
| `security/`, `.github/workflows/secret-scan.yml` | 김찬규 | 보안 |
| `docs/`, 루트 문서 | 김선 | 공통 |
| `data/` | 유시웅 | 가상 상담 데이터 (W1-07) |

**배포 설정은 이 저장소에 없습니다.** 이 저장소에 push하면 이 저장소의 워크플로가 이미지를 빌드해 레지스트리에 올리고, Kubernetes 배포·모니터링 설정은 박준우 님이 만드는 **별도 인프라 저장소**에 둡니다.

| 구분 | 이 저장소(앱) | 인프라 저장소(별도) |
|---|---|---|
| 담는 것 | 백엔드·프론트 코드, Dockerfile, 이미지 빌드·레지스트리 업로드 워크플로(박준우 작성), 테스트, 보안 자료, 문서 | Kubernetes 배포 설정, 모니터링·알림 설정, 운영 문서 |
| 담당 | 김선·유시웅·김찬규 (빌드 워크플로는 박준우) | 박준우 |
| 이 저장소에 넣지 않는 것 | Kubernetes yaml, 클러스터 접속 정보 | - |

인프라와 맞춘 약속값(이미지·포트·경로·환경 변수·지표·로그·종료 처리·마이그레이션)은 **`docs/contract.md`**에 있습니다. 이 문서를 바꾸는 PR은 박준우 님을 리뷰어로 지정합니다.

다른 사람 폴더의 파일을 고쳐야 하면 PR 설명에 이유를 적고 그 담당자를 리뷰어로 지정합니다.
담당자가 승인하기 전에는 머지하지 않습니다.

## 4. 기술 스택

| 구분 | 기술 |
|---|---|
| 백엔드 | Python 3.11, FastAPI, SQLAlchemy, pandas·openpyxl, Jinja2, boto3(SES) 또는 smtplib, pytest |
| 프론트엔드 | React + Vite, zustand(로그인 정보만), fetch |
| DB | PostgreSQL. **개발 중에는 Supabase(공용 개발 DB), 배포는 Amazon RDS**(클러스터 밖·같은 VPC, 퍼블릭 접근 끔). 백엔드만 SQLAlchemy로 직접 연결. 옮길 때는 `DATABASE_URL`만 바꿈 |
| LLM | 외부 LLM API 실패 전환: Claude → Gemini → Groq (앞 업체 실패 시 다음 업체). 클러스터에 모델을 띄우지 않음 |
| 인프라 | 이미지 빌드: 이 저장소의 GitHub Actions / 배포: 별도 인프라 저장소 — Kubernetes(AWS) 2개 배포(백엔드·프론트), Ingress, Prometheus·Grafana·Alertmanager |
| 보안 | 정규식 기반 입력·출력·전달 가드레일, security_events + Grafana 패널 |

## 5. 공통 약속값 (임의로 바꾸지 않기)

**보고서 상태**
`GENERATING` → `PENDING_APPROVAL` / `GENERATION_FAILED`
`PENDING_APPROVAL` → `APPROVED` / `REJECTED`
`APPROVED` → `DELIVERED` / `DELIVERY_FAILED` (실패 시 재전달)

**권한 검사 순서**: 401 인증 → 403 역할 → 403 소유·수신 그룹 → 409 상태

**경로·포트·환경 변수·지표 → `docs/contract.md`** (인프라와 맞춘 값, 바꾸면 박준우 리뷰)

| 항목 | 요약 |
|---|---|
| 업무 API | `/api/...` — 프론트는 항상 상대 경로로 호출 |
| 상태 확인 | `/health`(프로세스만), `/health/ready`(DB 연결 확인) |
| 지표 | `/metrics` — 요청 수·응답 시간·오류 수, LLM 응답 시간·실패 수 |
| 포트 | 백엔드 8000, 프론트 8080 (둘 다 root가 아닌 사용자로 실행) / 개발 5173 |
> LLM 실패 전환: 업체당 1회 시도, 시간 제한 초과·오류 시 다음 업체. 3곳 모두 실패하면 `GENERATION_FAILED`.

**환경 변수**: 이름과 비밀값 여부는 `docs/contract.md` 4절. 값은 `.env`·Kubernetes Secret에만, 저장소에는 `.env.example`의 키만 둡니다.

## 6. 설계 결정 (바꾸려면 팀 회의)

| 번호 | 결정 | 이유 |
|---|---|---|
| AD-1 | LLM은 업체별 호출 함수 + 실패 전환 순서를 환경 변수(`LLM_PROVIDER_ORDER`)로 관리 | 한 업체 장애·사용량 한도 초과에도 보고서 생성 유지 |
| AD-2 | 백엔드 시작 시 오래된 `GENERATING`을 `GENERATION_FAILED`로 변경 | 파드 종료 후 멈춘 보고서 방지(D-4) |
| AD-3 | 보고서 HTML은 Jinja2 autoescape + iframe sandbox | 상담 내용 속 스크립트 실행 차단(U-2) |
| AD-4 | LLM 호출 전 개인정보 마스킹 | 외부 LLM 업체 3곳으로 개인정보 유출 방지(공격 ③) |
| AD-5 | 숫자 절은 SQL 집계, 문장 절만 LLM | 수치 조작 차단, 검토자도 숫자 수정 불가 |
| AD-6 | DB(RDS)는 백엔드만 접속, 프론트·외부에서 직접 접속 불가 | 퍼블릭 접근 끔 + 보안 그룹으로 이중 차단(A1-3) |

## 7. 절대 하지 않을 것

- `main`에 직접 push
- `.env`, API 키, DB 연결 문자열, SES·SMTP 비밀번호, 실제 개인정보를 커밋
- 프론트에서 DB 직접 접속, 프론트 코드에 키 넣기
- Supabase 전용 기능(Data API·Auth·Storage·Edge Functions) 사용 — RDS로 옮길 때 깨짐
- 숫자 절을 LLM으로 만들기
- 승인(`APPROVED`) 전에 메일이 나가는 경로 추가
- 요청 본문으로 받은 임의 메일 주소로 발송 (수신 주소는 recipients 허용 목록만)
- 공격 시나리오 정답표를 DB·프론트에 넣기

## 8. Git 작업 방식 (요약 — 자세한 절차는 `docs/CONTRIBUTING.md`)

- 브랜치: `<분야>/<업무ID>-<짧은설명>`
  분야 키: `fe` 프론트, `be` 백엔드, `sec` 보안, `docs` 문서 (인프라 작업은 인프라 저장소에서)
  예: `be/W2-05-upload`, `fe/W2-07-login`, `sec/W2-12-attack-set`
- 커밋 메시지: `[W2-05] 업로드 15개 열 검증 추가`
- PR 하나 = 업무 ID 하나. 크면 나눕니다.
- PR 제목: `[W2-05] CSV·엑셀 업로드 API`. 템플릿의 체크리스트를 채웁니다.
- CI가 통과하면 **본인이 Squash and merge**. 다른 분야 파일을 고친 PR은 해당 담당 승인 후 머지.
- 머지 후 시트 「주차별 업무」의 상태·진전도를 갱신합니다.

## 9. 일정 핵심 날짜

| 날짜 | 일정 |
|---|---|
| 11/27(금) | 기획 발표 |
| 12/4(금) | 점검: 기본 API 제공·1차 배포 |
| 12/11(금) | 중간 발표 |
| 12/16(수) | **기능 동결** (이후 버그 수정·테스트·문서만) |
| 12/28(월) | 최종 발표 |

## 10. 아직 결정 안 된 것 (결정 전에는 바꾸기 쉬운 형태로 작성)

| 번호 | 내용 | 코드에서 대응 |
|---|---|---|
| Q-5 | 업체별 LLM 모델 | `CLAUDE_MODEL`·`GEMINI_MODEL`·`GROQ_MODEL` 환경 변수 |
| Q-6 | R2(5건)·R3(30%·10건) 기준값 | `backend/app/services/review_rules.py` 상단 상수 한 곳 |
| Q-7 | 권한 기반 RAG 포함 여부 | 결정 전 구현 금지 |
| Q-8 | SES 또는 Gmail SMTP | `MAIL_PROVIDER` 환경 변수 |
| Q-9 | Ingress 또는 LoadBalancer | 인프라 저장소에서 결정 (앱은 상대 경로 `/api`만 지키면 변경 없음) |
| Q-10 | iframe sandbox·이스케이프 기준 | `frontend/src/components/ReportView.jsx` 한 곳 |

## 11. Claude(AI 도구) 사용 규칙

- 작업 전에 이 파일과 해당 폴더의 CLAUDE.md를 읽습니다.
- 내 분야 폴더 밖의 파일은 수정하지 말고 제안만 합니다.
- 5절의 약속값은 임의로 바꾸지 않습니다.
- 예시 비밀값도 실제처럼 보이게 쓰지 않습니다. (`changeme`, `<YOUR_KEY>` 형태)
- 시나리오·공격 ID(A-1, D-3, A1-1, ATK-001, E-3 등)와 업무 ID(W2-05 등)는 시트 표기를 그대로 씁니다.
