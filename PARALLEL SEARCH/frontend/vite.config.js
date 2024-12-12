import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import dotenv from "dotenv";

// Load environment variables from .env file
dotenv.config();

// https://vite.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		host: "0.0.0.0",
		port: parseInt(process.env.VITE_PORT) || 5173, // Use BACKEND_PORT or fallback to 5173
		proxy: {
			"/api": {
				target: process.env.VITE_APP_BACKEND_HOST,
				secure: false,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ""),
			},
		},
	},
});
