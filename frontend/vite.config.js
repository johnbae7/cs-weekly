import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 개발 중 /api 요청을 로컬 백엔드(8000)로 넘김. 배포 후에는 Ingress가 같은 역할.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
