import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.robertavalerio.com',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  compressHTML: true,
});
