# 협업 가이드 — GitHub에 연결해서 PR하고 머지하기

규칙 한 줄: **main에 직접 push하지 않고, 브랜치 → PR → CI 통과 → 본인 머지.**

---

## 0. 저장소 관리자가 처음 한 번 할 일 (김선)

1. GitHub 조직 `johnbae7`에 저장소 `cs-weekly` 생성 (빈 저장소, README 없이)
2. 이 폴더를 올리기
   ```bash
   cd cs-weekly
   git init -b main
   git add .
   git commit -m "[W1-14] 저장소 골격과 분야별 CLAUDE.md"
   git remote add origin https://github.com/johnbae7/cs-weekly.git
   git push -u origin main
   ```
3. 팀원 3명을 저장소에 **Write** 권한으로 초대 (Settings → Collaborators and teams)
4. main 보호 규칙 (Settings → Branches → Add branch ruleset 또는 Add rule, 대상 `main`)
   - Require a pull request before merging: 켬
   - Required approvals: **0** (본인 머지 규칙이므로)
   - Require status checks to pass: 켬 → `test`(backend-ci), `build`(frontend-ci), `gitleaks`(secret-scan) 선택
     (체크 이름은 워크플로가 한 번 실행된 뒤 목록에 나타납니다)
   - Do not allow bypassing the above settings: 켬
5. Settings → General → Pull Requests: **Allow squash merging만 켜기**, Automatically delete head branches 켜기
6. `.github/CODEOWNERS`의 `<...>` 자리를 팀원 GitHub 아이디로 바꾸고 `#` 지우기 (선택)

---

## 1. 팀원이 처음 한 번 할 일

```bash
git clone https://github.com/johnbae7/cs-weekly.git
cd cs-weekly
cp .env.example .env      # 값은 팀 채널에서 받아 채우기. .env는 커밋되지 않음
```

Git 사용자 정보가 없다면:
```bash
git config --global user.name "홍길동"
git config --global user.email "GitHub에 등록한 메일"
```

---

## 2. 매번 작업할 때 (업무 하나 = 브랜치 하나 = PR 하나)

### ① 최신 main 받기
```bash
git switch main
git pull
```

### ② 브랜치 만들기
이름: `<분야>/<업무ID>-<짧은설명>` — 분야 키 `fe` `be` `sec` `docs` (인프라 작업은 별도 인프라 저장소에서)
```bash
git switch -c be/W2-05-upload
```

### ③ 작업하고 커밋하기
```bash
git status                      # 바뀐 파일 확인 (.env가 보이면 안 됨)
git add backend/app/routers/uploads.py backend/app/services/upload_parser.py
git commit -m "[W2-05] CSV·엑셀 업로드 15개 열 검증"
```
`git add .`보다 파일 이름을 적는 쪽이 안전합니다.

### ④ 올리기
```bash
git push -u origin be/W2-05-upload
```

### ⑤ PR 만들기
GitHub 저장소 화면에 뜨는 **Compare & pull request** 버튼 → 제목 `[W2-05] CSV·엑셀 업로드 API` → 템플릿 체크리스트 채우기 → Create pull request

### ⑥ 머지하기
- CI(초록 체크)가 모두 통과하면 **Squash and merge** → Confirm
- 다른 분야 파일을 고친 PR이면 해당 담당자 승인(Approve) 후 머지
- CI가 빨간색이면: Details를 눌러 오류를 보고 같은 브랜치에서 고쳐 다시 push (PR은 자동 갱신)

### ⑦ 정리
```bash
git switch main
git pull
git branch -d be/W2-05-upload
```
그리고 시트 「주차별 업무」의 상태·진전도를 갱신합니다.

---

## 3. 자주 생기는 상황

**작업 중에 main이 바뀌었을 때 (다른 사람이 먼저 머지)**
```bash
git switch main && git pull
git switch be/W2-05-upload
git merge main
# 충돌이 나면 표시된 파일을 열어 <<<<<<< ======= >>>>>>> 부분을 정리
git add <정리한 파일>
git commit
git push
```

**실수로 .env나 키를 커밋했을 때**
push 전이면 `git reset HEAD~1`로 되돌리고 다시 커밋합니다.
이미 push했다면 **바로 팀 채널에 알리고 그 키를 폐기·재발급**합니다. 기록에서 지우는 것만으로는 안전하지 않습니다.

**다른 분야와 맞춰야 하는 변경 (API 응답 필드, 환경 변수 추가 등)**
PR 설명의 「다른 분야에 알릴 것」에 적고, 해당 담당자를 리뷰어로 지정합니다.
약속값을 바꾸는 경우 시트 → 루트 `CLAUDE.md` → 코드 순서로 고칩니다.

---

## 4. 분야 간 연결 지점 (PR 리뷰어 지정 기준)

| 바꾸는 것 | 알릴 사람 |
|---|---|
| API 경로·응답 필드 | 김선(프론트), 김찬규(공격 시나리오 상태코드) |
| 메일 템플릿 변수 이름 | 김선 ↔ 유시웅 |
| 환경 변수 추가·이름 변경 | 박준우 (인프라 저장소의 ConfigMap·Secret) |
| `docs/contract.md`, `/health`·`/health/ready`·`/metrics`, 포트, Dockerfile, 마이그레이션 | 박준우 (리뷰어 필수 지정) |
| 가드레일 패턴 (`guardrails.py`) | 김찬규 ↔ 유시웅 |
| security_events 필드, 지표 이름 | 박준우 (Grafana 패널) |
| 상태 이름·역할 키 | 전원 |
