#!/usr/bin/env python3
"""Inventario Indexhibit -> contenuti del nuovo sito (content.json) + immagini WebP ottimizzate.

Include tutto cio' che era raggiungibile pubblicamente sul vecchio sito (verificato con un crawl):
reportage, ritratti, commissioni (Savoir Faire, Interior Design, Travels), pubblicazioni, bio, immagini della home.
I dittici (due foto affiancate) vengono anche separati in due immagini per la visualizzazione su telefono.

Riprendibile: se supera il budget di tempo esce con codice 2; rilanciarlo continua da dove era.
Variabili: RV_BASE (cartella 'Sito Roberta'), RV_BUDGET (secondi, default 95).
"""
import json, os, re, sys, time, glob, unicodedata
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spreads import split as split_spread

BASE = os.environ.get("RV_BASE", os.path.expanduser("~/mnt/Sito Roberta"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUDGET = float(os.environ.get("RV_BUDGET", "95"))
T0 = time.time()

INV = json.load(open(f"{BASE}/inventario/inventario.json", encoding="utf-8"))
BY = {x["id"]: x for x in INV}
SEC_PROJECT, SEC_STORIES, SEC_PORTRAIT, SEC_PUBLICATIONS = 12, 2, 5, 8
COMMISSIONS = [(7, "savoir-faire"), (6, "interior-design"), (4, "travels")]   # id pagina di sezione -> slug
FEATURED_IDS = [146, 143, 21, 91, 41, 82]
VIDEO_MERGE = {147: 146}
TITLE_FIX = {91: "Miner Hill"}
SITE = {"name": "Roberta Valerio", "instagram": "https://www.instagram.com/robertavalerio.photo/",
        "email": "photo@robertavalerio.com", "phone": "+33 6 10 12 25 56"}
# Pagine raggiungibili pubblicamente sul vecchio sito (crawl del 2026-11-06)
REACHABLE = set(map(int, "1,90,147,146,143,21,91,42,41,20,2,84,82,73,74,120,72,89,63,18,23,5,7,6,4,8,12,145,123,141,140,100,124,114,105,113,112,101,106,109,130,135,99,110,117,104,131,111,96,95,128,98,119,102,127,118,103,136,137,115,107,138,97,122,125,129,133,108,121,132,134".split(",")))


class Budget(Exception):
    pass


def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "senza-titolo"


def page_dimgs(eid):
    f = glob.glob(f"{BASE}/backup/pagine/{eid}_*.html")
    if not f:
        return []
    h = open(f[0], encoding="utf-8").read()
    return list(dict.fromkeys(re.findall(r"/files/dimgs/([^'\"?]+)", h)))


def best_sources(x):
    """Per ogni posizione sceglie il file con piu' pixel tra gimgs (admin) e dimgs (formato horizontal)."""
    g = [f"{BASE}/backup/immagini/{n}" for n in x["images"]]
    d = page_dimgs(x["id"])
    d = [f"{BASE}/backup/sito/files/dimgs/{n}" for n in d] if len(d) == len(g) else [None] * len(g)
    out = []
    for gp, dp in zip(g, d):
        cands = [p for p in (gp, dp) if p and os.path.exists(p)]
        if not cands:
            continue
        def area(p):
            try:
                with Image.open(p) as im:
                    return im.size[0] * im.size[1]
            except Exception:
                return 0
        out.append(max(cands, key=area))
    return out


def tick():
    if time.time() - T0 > BUDGET:
        raise Budget()


def make_image(src, slug, nn, allow_split=True):
    tick()
    d = f"{ROOT}/public/img/{slug}"
    os.makedirs(d, exist_ok=True)
    big, small, mark = f"{d}/{nn:02d}-l.webp", f"{d}/{nn:02d}-s.webp", f"{d}/{nn:02d}.nosplit"
    p1, p2 = f"{d}/{nn:02d}-p1.webp", f"{d}/{nn:02d}-p2.webp"
    need_big = not os.path.exists(big)
    need_split = allow_split and not (os.path.exists(p1) or os.path.exists(mark))
    if need_big or need_split:
        with Image.open(src) as im0:
            im = ImageOps.exif_transpose(im0).convert("RGB")
        if need_big:
            full = im if im.width <= 1600 else im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            full.save(big, "WEBP", quality=82, method=4)
            if full.width >= 900:
                full.resize((640, round(full.height * 640 / full.width)), Image.LANCZOS).save(small, "WEBP", quality=80, method=4)
        if need_split:
            parts = split_spread(im)
            if parts:
                for q, path in zip(parts, (p1, p2)):
                    if q.width > 1100:
                        q = q.resize((1100, round(q.height * 1100 / q.width)), Image.LANCZOS)
                    q.save(path, "WEBP", quality=82, method=4)
            else:
                open(mark, "w").close()
    with Image.open(big) as b:
        w, h = b.size
    url = f"/img/{slug}/{nn:02d}"
    out = {"s": f"{url}-l.webp", "sw": w, "l": f"{url}-l.webp", "lw": w, "w": w, "h": h}
    if os.path.exists(small):
        with Image.open(small) as s:
            out["s"], out["sw"] = f"{url}-s.webp", s.size[0]
    if os.path.exists(p1) and os.path.exists(p2):
        out["parts"] = []
        for path, u in ((p1, f"{url}-p1.webp"), (p2, f"{url}-p2.webp")):
            with Image.open(path) as q:
                out["parts"].append({"l": u, "w": q.size[0], "h": q.size[1]})
    return out


def gallery(x, slug, split=True):
    return [make_image(p, slug, i + 1, split) for i, p in enumerate(best_sources(x))]


def clean(raw):
    s = re.sub(r"<media:[^>]*/?>", "", raw or "")
    s = re.sub(r"(?is)<video.*?</video>", "", s)
    s = re.sub(r"(?is)<a [^>]*>(.*?)</a>", r"\1", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</?(?!strong\b|em\b|b\b|i\b)[a-z][^>]*>", "", s)
    s = s.replace("\r", "").replace("&nbsp;", " ")
    paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", s)]
    paras = [p for p in paras if re.sub(r"<[^>]+>", "", p).strip()]
    if paras:
        first = re.sub(r"<[^>]+>", "", paras[0]).strip()
        if first == first.upper() and len(first) < 110:
            paras = paras[1:]
    return paras


def detect_lang(paras):
    t = " " + re.sub(r"<[^>]+>", "", " ".join(paras)).lower() + " "
    score = {
        "fr": sum(t.count(w) for w in (" le ", " la ", " les ", " des ", " est ", " une ", " dans ", " qui ", " et ", " du ")),
        "en": sum(t.count(w) for w in (" the ", " and ", " of ", " is ", " with ", " in ", " to ", " her ", " they ")),
        "it": sum(t.count(w) for w in (" il ", " che ", " della ", " di ", " per ", " con ", " sono ", " una ")),
    }
    return max(score, key=score.get) if max(score.values()) else "fr"


def build():
    projects, redirects = [], []
    exs = [x for x in INV if x["kind"] == "exhibit" and x["status"] == "public" and x["section"]["id"] in (SEC_PROJECT, SEC_STORIES)]
    exs.sort(key=lambda x: (0 if x["section"]["id"] == SEC_PROJECT else 1, x["order"]))
    used = set()
    for x in exs:
        if x["id"] in VIDEO_MERGE:
            continue
        slug = slugify(TITLE_FIX.get(x["id"], x["title"]))
        while slug in used:
            slug += "-2"
        used.add(slug)
        imgs = gallery(x, slug)
        video = (x["videos"] or [None])[0]
        for vid, tgt in VIDEO_MERGE.items():
            if tgt == x["id"] and BY.get(vid) and BY[vid]["videos"]:
                video = BY[vid]["videos"][0]
        paras = clean(x["text"]) if not x["videos"] or x["id"] in VIDEO_MERGE.values() else []
        text = {"lang": detect_lang(paras), "paras": paras} if paras else None
        projects.append({"id": x["id"], "slug": slug, "title": TITLE_FIX.get(x["id"], x["title"]), "cover": imgs[0] if imgs else None,
                         "images": imgs, "text": text, "video": video.replace("https://robertavalerio.com", "https://www.robertavalerio.com") if video else None})
        if x.get("publicUrl"):
            redirects.append(("/index.php" + x["publicUrl"], f"/fr/work/{slug}/"))
    for vid, tgt in VIDEO_MERGE.items():
        u = BY[vid].get("publicUrl")
        if u:
            redirects.append(("/index.php" + u, f"/fr/work/{next(p['slug'] for p in projects if p['id'] == tgt)}/"))
    portraits = {"images": gallery(BY[SEC_PORTRAIT], "portraits")}
    commissions = []
    for sid, slug in COMMISSIONS:
        commissions.append({"id": sid, "slug": slug, "images": gallery(BY[sid], f"commissions/{slug}")})
    about = {"images": gallery(BY[12], "about")}
    frames = gallery(BY[1], "home", split=False)
    # pubblicazioni
    links = {}
    for m in re.finditer(r"href='[^']*?/index\.php/((?:tearsheets/)?([^/']+))/'[^>]*title='([^']*)'", BY[SEC_PUBLICATIONS]["text"]):
        links[m.group(3).strip()] = (m.group(1), slugify(m.group(2)))
    pubs, seen = [], set()
    pex = [x for x in INV if x["kind"] == "exhibit" and x["section"]["id"] == SEC_PUBLICATIONS and x["images"]]
    pex.sort(key=lambda x: x["order"])
    for x in pex:
        if x["title"].strip().lower() in seen:
            continue
        seen.add(x["title"].strip().lower())
        old, slug = links.get(x["title"].strip(), (None, slugify(x["title"])))
        imgs = gallery(x, f"pub/{slug}", split=False)
        pubs.append({"id": x["id"], "slug": slug, "title": x["title"].strip(), "outlet": (x["captions"] or [x["title"]])[0].strip(), "cover": imgs[0], "images": imgs})
        if old:
            redirects.append((f"/index.php/{old}/", f"/fr/publications/{slug}/"))
    notpub = [{"id": x["id"], "title": x["title"], "section": x["section"]["title"], "images": len(x["images"]), "status": x["status"]}
              for x in INV if x["id"] not in REACHABLE]
    slugs = {p["id"]: p["slug"] for p in projects}
    content = {"site": SITE, "featured": [slugs[i] for i in FEATURED_IDS if i in slugs], "projects": projects, "portraits": portraits,
               "commissions": commissions, "about": about, "frames": frames, "publications": pubs, "notPublished": notpub}
    os.makedirs(f"{ROOT}/src/data", exist_ok=True)
    json.dump(content, open(f"{ROOT}/src/data/content.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sec = {"/index.php/project/": "/fr/work/", "/index.php/stories/": "/fr/work/", "/index.php/portrait/": "/fr/portraits/",
           "/index.php/tearsheets/": "/fr/publications/", "/index.php/bio/": "/fr/about/", "/index.php/corporate/": "/fr/commissions/savoir-faire/",
           "/index.php/lifestile/": "/fr/commissions/interior-design/", "/index.php/traveldestinations/": "/fr/commissions/travels/"}
    allr = {**sec, **dict(redirects)}
    lines = [f"{a} {b} 301" for a, b in allr.items()] + [f"{a.rstrip('/')} {b} 301" for a, b in allr.items()]
    open(f"{ROOT}/public/_redirects", "w").write("\n".join(lines) + "\n")
    open(f"{ROOT}/public/robots.txt", "w").write("User-agent: *\nDisallow: /\n")   # BOZZA: togliere al lancio
    n = lambda l: sum(len(i["images"]) for i in l)
    nparts = sum(1 for p in projects for i in p["images"] if "parts" in i) + sum(1 for c in commissions for i in c["images"] if "parts" in i)
    print(f"OK progetti={len(projects)} ({n(projects)} img, {nparts} dittici separati) ritratti={len(portraits['images'])} commissioni={n(commissions)} "
          f"pubblicazioni={len(pubs)} ({n(pubs)} img) bio={len(about['images'])} home={len(frames)} non-pubblicati={len(notpub)}")


try:
    build()
except Budget:
    print("Budget di tempo esaurito: rilanciare per continuare.")
    sys.exit(2)
