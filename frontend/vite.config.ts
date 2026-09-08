import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The app calls relative /api/... paths; the dev server forwards them to Django,
// so there is no CORS setup and no API base URL to configure.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
