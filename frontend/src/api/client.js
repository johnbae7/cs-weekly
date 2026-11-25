import { useAuthStore } from "../store/authStore.js";

// 항상 상대 경로 /api 로 호출 (개발: Vite 프록시, 배포: Ingress)
const API_PREFIX = "/api";

export async function api(path, { method = "GET", body, headers = {} } = {}) {
  const { token, logout } = useAuthStore.getState();
  const isForm = body instanceof FormData;

  const res = await fetch(`${API_PREFIX}${path}`, {
    method,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(body && !isForm ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  });

  if (res.status === 401) {
    logout();
    window.location.assign("/login");
    throw new Error("로그인이 필요합니다");
  }

  const data = res.headers.get("content-type")?.includes("application/json") ? await res.json() : null;
  if (!res.ok) {
    // 403 권한 없음, 409 상태 오류 등은 화면에서 메시지로 표시
    const err = new Error(data?.detail ?? `요청 실패 (${res.status})`);
    err.status = res.status;
    throw err;
  }
  return data;
}
