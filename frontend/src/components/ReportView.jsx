// 백엔드가 만든 보고서 HTML 표시 (AD-3, U-2, Q-10)
// - iframe sandbox + srcdoc 로만 표시. dangerouslySetInnerHTML 사용 금지
// - sandbox 에 allow-scripts 를 넣지 않음
export default function ReportView({ html }) {
  return (
    <iframe
      title="보고서"
      sandbox=""
      srcDoc={html ?? ""}
      style={{ width: "100%", minHeight: 600, border: "1px solid #ddd" }}
    />
  );
}
