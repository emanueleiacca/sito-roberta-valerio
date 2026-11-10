// Legge i contenuti da Sanity al momento della build. Se le variabili non sono impostate restituisce null (si usa content.json).
const E = import.meta.env || {};
const PID = E.SANITY_PROJECT_ID || process.env.SANITY_PROJECT_ID;
const DS = E.SANITY_DATASET || process.env.SANITY_DATASET || 'production';
const TOKEN = E.SANITY_TOKEN || process.env.SANITY_TOKEN;

const IMG = `images[]{caption,diptych,splitAt,"ref":image.asset._ref}`;
const QUERY = `{
  "reportages": *[_type=="reportage" && defined(slug.current)]|order(coalesce(position,0) asc, _createdAt desc){_id,title,"slug":slug.current,places,year,themes,text,textLang,video,featured,${IMG}},
  "galleries": *[_type=="gallery"]{key,${IMG}},
  "publications": *[_type=="publication" && defined(slug.current)]|order(coalesce(position,0) asc, _createdAt desc){_id,title,outlet,"slug":slug.current,places,themes,${IMG}}
}`;

function parseRef(ref) {
  const m = /^image-([a-f0-9]+)-(\d+)x(\d+)-(\w+)$/.exec(ref || '');
  return m ? { id: m[1], w: +m[2], h: +m[3], ext: m[4] } : null;
}
function toImage(ph) {
  const r = parseRef(ph.ref); if (!r) return null;
  const b = `https://cdn.sanity.io/images/${PID}/${DS}/${r.id}-${r.w}x${r.h}.${r.ext}`;
  const lw = Math.min(1600, r.w), lh = Math.round((r.h * lw) / r.w);
  const l = `${b}?w=${lw}&fit=max&auto=format&q=82`;
  const big = r.w >= 900;
  const out = { l, lw, w: lw, h: lh, s: big ? `${b}?w=640&fit=max&auto=format&q=80` : l, sw: big ? 640 : lw, caption: ph.caption || null };
  if (ph.diptych && ph.splitAt) {
    const x = Math.round(ph.splitAt * r.w), m = Math.max(2, Math.round(r.w * 0.004));
    const mk = (rx, rw) => { const pw = Math.min(rw, 1100); return { l: `${b}?rect=${rx},0,${rw},${r.h}&w=${pw}&fit=max&auto=format&q=82`, w: pw, h: Math.round((r.h * pw) / rw) }; };
    out.parts = [mk(0, x - m), mk(x + m, r.w - x - m)];
  }
  return out;
}
const imgs = (a) => (a || []).map(toImage).filter(Boolean);
const paras = (t) => (t || '').split(/\n\s*\n/).map((s) => s.trim()).filter(Boolean)
  .map((s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br />'));

export async function loadCms() {
  if (!PID) return null;
  const url = `https://${PID}.apicdn.sanity.io/v2024-01-01/data/query/${DS}?query=${encodeURIComponent(QUERY)}`;
  const res = await fetch(url, TOKEN ? { headers: { Authorization: `Bearer ${TOKEN}` } } : undefined);
  if (!res.ok) throw new Error(`Sanity: ${res.status} ${await res.text()}`);
  const { result } = await res.json();
  const projects = result.reportages.map((r) => {
    const images = imgs(r.images), p = paras(r.text);
    return { id: r._id, slug: r.slug, title: r.title, cover: images[0] || null, images, text: p.length ? { lang: r.textLang || 'fr', paras: p } : null,
      video: r.video || null, themes: r.themes || [], places: r.places || [], year: r.year ?? null, featured: !!r.featured };
  });
  const gal = Object.fromEntries(result.galleries.map((g) => [g.key, imgs(g.images)]));
  const seen = {};
  const publications = result.publications.map((p) => {
    let slug = p.slug; if (seen[slug]) slug = `${slug}-${++seen[p.slug]}`; else seen[slug] = 1;
    const images = imgs(p.images);
    return { id: p._id, slug, title: p.title, outlet: p.outlet || p.title, cover: images[0] || null, images, themes: p.themes || [], places: p.places || [] };
  });
  return {
    projects, featured: projects.filter((p) => p.featured).map((p) => p.slug),
    portraits: { images: gal.portraits || [] },
    commissions: ['savoir-faire', 'interior-design', 'travels'].map((slug) => ({ slug, images: gal[slug] || [] })),
    publications,
  };
}
