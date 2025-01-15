import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Markdown from 'vite-plugin-md';
import markdownItKatex from 'markdown-it-katex';
import path from 'path';

export default defineConfig({
  plugins: [
    vue({
      include: [/\.vue$/, /\.md$/]
    }),
    Markdown({
      markdownItSetup(md) {
        md.use(markdownItKatex);
      }
    })
  ],
  optimizeDeps: {
    include: ['vue', 'katex', 'markdown-it', 'markdown-it-katex']
  },
  server: {
    port: 4000
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
});
