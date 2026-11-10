// Importa in Sanity i contenuti gia' migrati (reportage, ritratti, commissioni, pubblicazioni).
// Usa createIfNotExists: rilanciarlo NON sovrascrive modifiche fatte da Roberta. Riprendibile (cache in .import-cache.json).
// Uso:  SANITY_PROJECT_ID=... SANITY_TOKEN=... node scripts/import.mjs      (token con permesso Editor, da NON salvare in file)
import { createClient } from '@sanity/client';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(root, 'src/data', f), 'utf-8'));
const content = rd('content.json'), meta = rd('meta.json');
const splits = fs.existsSync(path.join(root, 'src/data/splits.json')) ? rd('splits.json') : {};
const { SANITY_PROJECT_ID: projectId, SANITY_DATASET: dataset = 'production', SANITY_TOKEN: token } = process.env;
if (!projectId || !token) { console.error('Servono SANITY_PROJECT_ID e SANITY_TOKEN'); process.exit(1); }
const client = createClient({ projectId, dataset, token, apiVersion: '2024-01-01', useCdn: false });

const cacheFile = path.join(here, '.import-cache.json');
const cache = fs.existsSync(cacheFile) ? JSON.parse(fs.readFileSync(cacheFile, 'utf-8')) : {};
const save = () => fs.writeFileSync(cacheFile, JSON.stringify(cache));

async function asset(url) {
  if (cache[url]) return cache[url];
  const file = path.join(root, 'public', url);
  const a = await client.assets.upload('image', fs.createReadStream(file), { filename: path.basename(file) });
  cache[url] = a._id; save();
  return a._id;
}
const ent = (s) => s.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#0?39;|&rsquo;/g, '’').replace(/&lt;/g, '<').replace(/&gt;/g, '>');

async function photos(images) {
  const out = [];
  for (let i = 0; i < images.length; i += 4) {
    const batch = await Promise.all(images.slice(i, i + 4).map(async (im, k) => {
      const ref = await asset(im.l);
      const sp = splits[im.l] ?? (im.parts ? im.parts[0].w / (im.parts[0].w + im.parts[1].w) : null);
      return { _type: 'photo', _key: `p${i + k + 1}`, image: { _type: 'image', asset: { _type: 'reference', _ref: ref } },
        ...(sp ? { diptych: true, splitAt: Math.round(sp * 1000) / 1000 } : {}) };
    }));
    out.push(...batch);
    process.stdout.write(`\r  foto ${out.length}/${images.length}   `);
  }
  process.stdout.write('\n');
  return out;
}
const slug = (s) => ({ _type: 'slug', current: s });
const put = (doc) => client.createIfNotExists(doc);

console.log('Reportage…');
let pos = 0;
for (const p of content.projects) {
  const m = meta.projects[p.slug] || {};
  console.log(' •', p.title);
  await put({ _id: `reportage-${p.slug}`, _type: 'reportage', title: p.title, slug: slug(p.slug), places: m.places || [], themes: m.themes || [],
    ...(m.year ? { year: m.year } : {}), featured: content.featured.includes(p.slug), position: ++pos,
    text: p.text ? p.text.paras.map(ent).join('\n\n') : undefined, textLang: p.text?.lang || 'fr', video: p.video || undefined, images: await photos(p.images) });
}
console.log('Galerie…');
const galleries = [['portraits', 'Portraits', content.portraits.images], ...content.commissions.map((c) => [c.slug, { 'savoir-faire': 'Savoir-faire', 'interior-design': 'Interior design', travels: 'Travels' }[c.slug], c.images])];
for (const [key, title, images] of galleries) {
  console.log(' •', title);
  await put({ _id: `gallery-${key}`, _type: 'gallery', title, key, images: await photos(images) });
}
console.log('Publications…');
const seen = {}; pos = 0;
for (const p of content.publications) {
  let s = p.slug; if (seen[s]) s = `${s}-${++seen[p.slug]}`; else seen[s] = 1;
  const m = meta.publications[s] || {};
  console.log(' •', p.title);
  await put({ _id: `publication-${s}`, _type: 'publication', title: p.title, outlet: p.outlet, slug: slug(s), places: m.places || [], themes: m.themes || [], position: ++pos, images: await photos(p.images) });
}
console.log('Fatto. Ora: Studio -> controllare i contenuti.');
