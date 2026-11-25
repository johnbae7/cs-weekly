// 전달 이력 표 (시각·주소·성공/실패) — GET /api/reports/{id}/deliveries
// TODO(김선): 실패 행 표시, [재전달] 버튼은 ReportDetail 에서
export default function DeliveryTable({ rows = [] }) {
  return (
    <table>
      <thead>
        <tr><th>시각</th><th>주소</th><th>결과</th></tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id}><td>{r.sent_at}</td><td>{r.email}</td><td>{r.status}</td></tr>
        ))}
      </tbody>
    </table>
  );
}
