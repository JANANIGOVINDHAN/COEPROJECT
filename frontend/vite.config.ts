import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/auth': 'http://localhost:8000',
      '/dashboard': 'http://localhost:8000',
      '/drift': 'http://localhost:8000',
      '/sites': 'http://localhost:8000',
      '/devices': 'http://localhost:8000',
      '/configurations': 'http://localhost:8000',
      '/baselines': 'http://localhost:8000',
      '/compliance': 'http://localhost:8000',
      '/tickets': 'http://localhost:8000',
      '/remediation': 'http://localhost:8000',
      '/reports': 'http://localhost:8000',
      '/audit': 'http://localhost:8000'
    }
  }
});
