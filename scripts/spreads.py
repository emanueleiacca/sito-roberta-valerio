"""Rilevamento dei dittici: immagini con due foto affiancate (margine bianco o giuntura netta)."""
import numpy as np
from PIL import Image

WHITE = 244


def _runs(mask):
    runs, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            runs.append((start, i)); start = None
    if start is not None:
        runs.append((start, len(mask)))
    return runs


def find_split(im):
    """Ritorna la coordinata x di taglio (in pixel dell'immagine) o None."""
    w, h = im.size
    if w / h < 1.7:
        return None
    sc = 4 if w > 800 else 2
    g = np.asarray(im.convert("L").resize((max(w // sc, 8), max(h // sc, 8))), dtype=np.int16)
    gh, gw = g.shape
    # 1) gutter bianco: colonne quasi tutte bianche
    white_col = (g >= WHITE).mean(axis=0) >= 0.985
    lo, hi = int(gw * .22), int(gw * .78)
    cands = [(a, b) for a, b in _runs(white_col) if a >= lo - 2 and b <= hi + 2 and (b - a) >= max(2, gw * .012)]
    best = None
    for a, b in cands:
        left, right = g[:, :a], g[:, b:]
        if left.size == 0 or right.size == 0:
            continue
        if (left < WHITE).mean() < .12 or (right < WHITE).mean() < .12:
            continue
        c = (a + b) / 2
        score = abs(c - gw / 2) - (b - a)          # preferisce gutter larghi e vicini al centro
        if best is None or score < best[0]:
            best = (score, c)
    if best:
        return int(best[1] * sc)
    # 2) giuntura senza margine: massimo salto tra colonne adiacenti vicino al centro
    d = np.abs(np.diff(g, axis=1)).mean(axis=0)
    a, b = int(gw * .3), int(gw * .7)
    seg = d[a:b]
    if seg.size == 0:
        return None
    k = int(seg.argmax()); peak = seg[k]; med = np.median(d)
    if peak >= 22 and peak >= 4 * max(med, 1):
        return int((a + k + 1) * sc)
    return None


def trim(part, pad=0.012):
    g = np.asarray(part.convert("L"), dtype=np.int16)
    ys, xs = np.where(g < WHITE)
    if len(xs) == 0:
        return part
    h, w = g.shape
    px, py = int(w * pad), int(h * pad)
    box = (max(xs.min() - px, 0), max(ys.min() - py, 0), min(xs.max() + 1 + px, w), min(ys.max() + 1 + py, h))
    return part.crop(box)


def split(im):
    x = find_split(im)
    if x is None:
        return None
    w, h = im.size
    m = max(2, int(w * 0.004))     # margine di sicurezza sulla giuntura
    parts = [trim(im.crop((0, 0, max(x - m, 1), h))), trim(im.crop((min(x + m, w - 1), 0, w, h)))]
    if any(p.size[0] < 120 or p.size[1] < 120 for p in parts):
        return None
    return parts
