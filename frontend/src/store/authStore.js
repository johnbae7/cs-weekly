import { create } from "zustand";

// 토큰·역할·그룹만 저장 (상담 내용·보고서 본문은 저장하지 않음)
export const useAuthStore = create((set) => ({
  token: null,
  role: null, // uploader | reviewer | recipient
  group: null, // cs | ops | exec (수신자만)
  login: ({ token, role, group }) => set({ token, role, group: group ?? null }),
  logout: () => set({ token: null, role: null, group: null }),
}));
