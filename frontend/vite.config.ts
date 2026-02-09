import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Output to a 'dist' directory at the root of the project
    outDir: "../dist",
  },
});
