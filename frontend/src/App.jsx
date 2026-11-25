import { Navigate, Route, Routes } from "react-router-dom";
import { useAuthStore } from "./store/authStore.js";
import Login from "./pages/Login.jsx";
import ReportList from "./pages/ReportList.jsx";
import UploadCreate from "./pages/UploadCreate.jsx";
import ReportDetail from "./pages/ReportDetail.jsx";

// 로그인 안 됐으면 /login 으로. 권한 검사는 백엔드가 하고, 여기서는 화면 이동만.
function RequireLogin({ children }) {
  const token = useAuthStore((s) => s.token);
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<RequireLogin><ReportList /></RequireLogin>} />
      <Route path="/upload" element={<RequireLogin><UploadCreate /></RequireLogin>} />
      <Route path="/reports/:id" element={<RequireLogin><ReportDetail /></RequireLogin>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
