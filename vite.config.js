import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    target: 'es2020',
    cssCodeSplit: true,
    assetsInlineLimit: 4096,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router')) {
            return 'vendor'
          }
        }
      }
    }
  },
  server: {
    port: 5173,
    allowedHosts: ['rings-atelier.ru'],
    cors: {
      origin: 'https://rings-atelier.ru'
    }
  }
})
