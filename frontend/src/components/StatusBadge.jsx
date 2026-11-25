import { REPORT_STATUS } from "../constants/status.js";

export default function StatusBadge({ status }) {
  return <span className={`badge badge-${status}`}>{REPORT_STATUS[status] ?? status}</span>;
}
