// Unisce i contenuti (Sanity se configurato, altrimenti content.json importato) con i metadati opzionali (meta.json).
import legacy from '../data/content.json';
import meta from '../data/meta.json';
import { loadCms } from './cms.js';

const cms = await loadCms();           // null se Sanity non e' configurato
export const content = cms ? { ...legacy, ...cms } : legacy;
export const FROM_CMS = !!cms;

export const THEMES = meta.themes;
const capMap = (key, slug) => (meta.captions && meta.captions[key] && (slug ? meta.captions[key][slug] : meta.captions[key])) || {};
export function withCaptions(images, map) { return images.map((im, k) => ({ ...im, caption: im.caption ?? (map && map[String(k + 1)]) ?? null })); }
export const portraitCaptions = () => capMap('portraits');

export function projects() {
  return content.projects.map((p, i) => {
    const m = meta.projects[p.slug] || {};
    return { ...p, order: i, num: String(i + 1).padStart(2, '0'), themes: p.themes ?? m.themes ?? [], places: p.places ?? m.places ?? [], year: p.year ?? m.year ?? null,
      featured: p.featured ?? content.featured.includes(p.slug), images: withCaptions(p.images, capMap('projects', p.slug)) };
  });
}
const OUTLETS = [[/parisien/i, 'Le Parisien Weekend'], [/air france|^afm/i, 'Air France Madame'], [/yo dona/i, 'Yo Dona'], [/^la vie$/i, 'La Vie'],
  [/ccfd|faim et dev/i, 'CCFD'], [/monde/i, 'Le Monde'], [/conde nast/i, 'Condé Nast'], [/badanti donna|donna moderna/i, 'Donna Moderna']];
export function outletName(raw) {
  const s = (raw || '').trim();
  for (const [re, name] of OUTLETS) if (re.test(s)) return name;
  return s.toLowerCase().replace(/\b\p{L}/gu, (c) => c.toUpperCase());
}
export function publications() {
  const seen = {};
  return content.publications.map((p) => {
    let slug = p.slug;
    if (seen[slug]) slug = `${slug}-${++seen[p.slug]}`; else seen[slug] = 1;
    const m = meta.publications[slug] || {};
    return { ...p, slug, outletName: outletName(p.outlet), themes: p.themes ?? m.themes ?? [], places: p.places ?? m.places ?? [] };
  });
}
export function placeName(code, lang) {
  try { return new Intl.DisplayNames([lang], { type: 'region' }).of(code) || code; } catch { return code; }
}
export function countBy(items, key) {
  const c = {};
  for (const it of items) for (const v of it[key]) c[v] = (c[v] || 0) + 1;
  return c;
}
