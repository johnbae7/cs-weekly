# frontend/ — 풀스택 프론트엔드 (담당: 김선)

루트 `CLAUDE.md`를 먼저 읽은 뒤 이 파일을 따릅니다.

## 1. 맡는 범위

| 업무 ID | 내용 | 연결 요구사항 |
|---|---|---|
| W1-05 | 화면 설계(4개 화면 와이어프레임) | F-7 |
| W2-07 | 프론트 골격, 화면 4(로그인)·1(목록)·2(업로드) | F-7 |
| W3-04 | 메일 HTML 템플릿 (`backend/app/templates/mail/`) | F-5 |
| W3-05 | 화면 3(보고서 상세: 검토·승인·전달 이력), 역할별 버튼 | F-5, F-7 |
| W4-01, W5-01 | 오류 처리 보완, 최종 버그 수정 (유시웅과 공동) | F-11 |

## 2. 폴더 구조 (시트 「풀스택아키텍처」 프론트엔드 구성과 동일)

```
frontend/
├── src/
│   ├── main.jsx
│   ├── App.jsx              라우팅, 로그인 안 됐으면 /login으로
│   ├── api/client.js        fetch 래퍼: 토큰 자동 첨부, 401이면 로그인 화면으로
│   ├── store/authStore.js   zustand: 토큰·역할·그룹만 저장
│   ├── constants/status.js  보고서 상태·역할 이름 (루트 CLAUDE.md 5절과 동일하게)
│   ├── pages/
│   │   ├── Login.jsx        화면 4
│   │   ├── ReportList.jsx   화면 1
│   │   ├── UploadCreate.jsx 화면 2
│   │   └── ReportDetail.jsx 화면 3
│   └── components/
│       ├── ReportView.jsx   보고서 HTML을 iframe sandbox(srcdoc)로 표시
│       ├── StatusBadge.jsx  상태 배지
│       └── DeliveryTable.jsx 전달 이력 표
├── vite.config.js           개발 중 /api → http://localhost:8000 프록시
├── nginx.conf               배포용 (비루트 nginx, 8080, SPA 새로고침 대응)
└── Dockerfile
```

## 3. 화면 4개 (시트 「보고서·화면」)

| 화면 | 사용자 | 구성 | API |
|---|---|---|---|
| 1. 보고서 목록 | 전체 | 작성자: 내 보고서 + [새 보고서] / 검토자: 전체 + '승인 대기'·'검토 필요' 필터 / 수신자: 내 그룹에 전달된 것만. 상태 배지 | GET /api/reports |
| 2. 업로드·생성 | 작성자 | 주차 선택, 파일(CSV·엑셀), 업로드 결과(행 수·오류 행), 추가 요청(200자), '팀장 검토 요청' 체크, [생성] | POST·GET /api/uploads, POST /api/reports |
| 3. 보고서 상세 | 전체 | 메일과 같은 모양의 보고서, 판정 사유. 검토자에게만 [문장 수정] [승인] [반려] [재전달] + 전달 이력 표. 수신자는 읽기 전용 | GET·PATCH /api/reports/{id}, approve, reject, deliveries |
| 4. 로그인 | 전체 | 이메일·비밀번호. 토큰·역할을 zustand에 저장 | POST /api/auth/login |

- 같은 화면을 역할에 따라 **버튼만 다르게** 보여 줍니다.
- 생성 중(`GENERATING`)이면 **3초마다** 다시 조회합니다.
- '검토 필요' 보고서는 사유 확인 체크를 해야 [승인] 버튼이 켜집니다.

## 4. 반드시 지킬 것

- **API는 항상 상대 경로 `/api/...`로 호출.** `http://localhost:8000` 같은 주소를 코드에 쓰지 않습니다. (개발 중에는 Vite 프록시, 배포 후에는 Ingress가 연결)
- **DB에 직접 접속하지 않습니다.** DB 주소·키·DB 라이브러리를 넣지 않습니다 (AD-6).
- **zustand에는 토큰·역할·그룹만.** 상담 내용·보고서 본문은 저장하지 않습니다.
- **보고서 HTML은 `ReportView`의 iframe sandbox(srcdoc)로만 표시.** `dangerouslySetInnerHTML`을 쓰지 않습니다 (AD-3, U-2). sandbox 속성에 `allow-scripts`를 넣지 않습니다.
- 버튼 숨김은 편의 기능일 뿐, 권한 검사는 백엔드가 합니다. 403·409 응답을 받으면 메시지를 보여 줍니다.
- 숫자 절(2·3·5)은 수정 입력칸을 만들지 않습니다.

## 5. 메일 템플릿 (W3-04)

- 위치: `backend/app/templates/mail/report.html.j2`, `approval_request.html.j2`
- 메일 클라이언트용이라 **인라인 스타일 표**로 작성 (외부 CSS·스크립트 금지)
- Jinja2 autoescape가 켜져 있으므로 `|safe`를 쓰지 않습니다.
- Gmail·Outlook에서 표시를 확인합니다.
- 제목 형식: `[존배몰 CS 주간리포트] 2026-W48 (11/23~11/29) · 검토 승인`
- 맨 아래: 서비스에서 보기 링크(`APP_BASE_URL`), 발송 시각, 승인자

## 6. 로컬 실행

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173 (백엔드는 8000번에서 실행 중이어야 함)
npm run build      # 배포용 빌드 확인
```
