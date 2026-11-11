import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// In dev, /api is proxied to the FastAPI backend on :8000.
// In production (Docker/nginx) the nginx config does the same proxying,
// so the frontend never needs a hard-coded backend host.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
