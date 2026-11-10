#!/usr/bin/env python3
"""Calcola la posizione (0..1) della separazione dei dittici sulle immagini gia' elaborate -> src/data/splits.json (serve all'import in Sanity)."""
import json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spreads import find_split
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(f"{ROOT}/src/data/content.json", encoding="utf-8"))
groups = [p["images"] for p in c["projects"]] + [x["images"] for x in c["commissions"]] + [c["portraits"]["images"]] + [p["images"] for p in c["publications"]]
out, n = {}, 0
for imgs in groups:
    for im in imgs:
        if "parts" not in im: continue
        n += 1
        with Image.open(f"{ROOT}/public{im['l']}") as i:
            i = i.convert("RGB"); x = find_split(i)
        if x: out[im["l"]] = round(x / i.size[0], 4)
json.dump(out, open(f"{ROOT}/src/data/splits.json", "w"))
print("dittici", n, "posizioni trovate", len(out))
