// 화면 3. 보고서 상세 (W3-05)
// GET·PATCH /api/reports/{id}, approve, reject, POST·GET /api/reports/{id}/deliveries
// TODO(김선)
// - ReportView 로 보고서 표시 + 판정 사유
// - 검토자만: [문장 수정](절 1·4·6만) [승인] [반려(사유 필수)] [재전달] + DeliveryTable
// - '검토 필요'는 사유 확인 체크 후에만 [승인] 활성화
// - 수신자는 읽기 전용
export default function ReportDetail() {
  return <h1>보고서 상세</h1>;
}
