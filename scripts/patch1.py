import re,os
R=os.path.expanduser("~/rv-sito")
# i18n_gen: unisce testi extra
p=R+"/scripts/i18n_gen.py"; s=open(p,encoding="utf-8").read()
if "i18n_extra" not in s:
    s=s.replace("UI = {}\nfor code, vals in T.items():","from i18n_extra import EX, EXK, TH, THK\nUI = {}\nfor code, vals in T.items():")
    s=s.replace("UI[code]['langNames'] = LN[code]","UI[code]['langNames'] = LN[code]; UI[code].update(dict(zip(EXK, EX[code]))); UI[code]['themes'] = dict(zip(THK, TH[code]))")
    open(p,"w",encoding="utf-8").write(s)
# Base: didascalia nella lightbox
p=R+"/src/layouts/Base.astro"; s=open(p,encoding="utf-8").read()
if "lb-cap" not in s:
    s=s.replace('<p class="lb-count" id="lb-count"></p>','<p class="lb-cap" id="lb-cap" hidden></p>\n    <p class="lb-count" id="lb-count"></p>')
    s=s.replace("const count = document.getElementById('lb-count');","const count = document.getElementById('lb-count');\n    const cap = document.getElementById('lb-cap');")
    s=s.replace("count.textContent = `${idx + 1} / ${items.length}`;","count.textContent = `${idx + 1} / ${items.length}`;\n      cap.textContent = b.dataset.caption || ''; cap.hidden = !b.dataset.caption;")
    open(p,"w",encoding="utf-8").write(s)
# CSS
p=R+"/src/styles/global.css"; s=open(p,encoding="utf-8").read()
if ".filters" not in s:
    s+='''
/* ---- filtri, chip, didascalie ---- */
.filters { margin: 26px 0 28px; display: grid; gap: 14px; }
.fgroup { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.flabel { font: 800 12px/1 var(--ui); font-stretch: 85%; text-transform: uppercase; letter-spacing: .14em; margin-inline-end: 6px; min-width: 7.5em; }
.chip { font: 600 14px/1 var(--ui); border: 2px solid var(--ink); border-radius: 999px; padding: 9px 14px; background: var(--paper); color: var(--ink); cursor: pointer; text-decoration: none; display: inline-flex; gap: 8px; align-items: center; }
.chip i { font-style: normal; font-weight: 500; font-size: 12px; opacity: .6; }
.chip:hover { background: var(--tint); color: var(--ink); }
.chip[aria-pressed="true"] { background: var(--ink); color: var(--paper); }
.chip.reset { border-color: var(--red); color: var(--red); }
.chip.plain { border-style: dashed; cursor: default; }
a.chip:hover { border-color: var(--red); color: var(--red); }
.ftools select { font: 600 14px/1 var(--ui); padding: 8px 10px; border: 2px solid var(--ink); border-radius: 999px; background: var(--paper); margin-inline-start: 6px; }
.fcount { font: 600 13px/1 var(--ui); color: var(--mute); }
.tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 0; }
.noresult { font: 600 18px/1.4 var(--ui); color: var(--mute); }
.item[hidden], .chip[hidden] { display: none !important; }
.gal figcaption { font: italic 400 15px/1.4 var(--text); color: var(--mute); margin-top: 6px; max-width: 70ch; }
.lb-cap { position: absolute; bottom: 40px; inset-inline: 60px; margin: 0; text-align: center; font: italic 400 16px/1.4 var(--text); }
@media (max-width: 700px) { .flabel { min-width: 100%; } .lb-cap { bottom: 58px; inset-inline: 12px; } }
'''
    open(p,"w",encoding="utf-8").write(s)
# build_content: slug pubblicazioni unici non necessario (gestito in lib/data.js)
print("patch ok")
