import { defineConfig } from 'sanity';
import { structureTool } from 'sanity/structure';
import { schemaTypes } from './schemaTypes';

export default defineConfig({
  name: 'default',
  title: 'Roberta Valerio — Administration',
  projectId: process.env.SANITY_STUDIO_PROJECT_ID || '34i4bq1s',
  dataset: process.env.SANITY_STUDIO_DATASET || 'production',
  plugins: [structureTool()],
  schema: { types: schemaTypes },
});
