// 루트 CLAUDE.md 5절과 같은 값. 바꾸려면 시트 → CLAUDE.md → 코드 순서로.
export const REPORT_STATUS = {
  GENERATING: "생성 중",
  GENERATION_FAILED: "생성 실패",
  PENDING_APPROVAL: "승인 대기",
  APPROVED: "승인됨",
  REJECTED: "반려",
  DELIVERED: "전달 완료",
  DELIVERY_FAILED: "전달 실패",
};

export const ROLES = {
  uploader: "작성자",
  reviewer: "검토자",
  recipient: "수신자",
};

export const RECIPIENT_GROUPS = {
  cs: "CS팀",
  ops: "상품·물류",
  exec: "경영진",
};

// 생성 중 상태 다시 조회 간격 (3초)
export const POLL_INTERVAL_MS = 3000;
