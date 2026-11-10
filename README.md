# Sito Roberta Valerio — bozza (Astro, statico)

Bozza del nuovo sito, costruita dall'inventario del vecchio Indexhibit (`../inventario/`) e dal backup (`../backup/`).

## Avvio
```
npm install
npm run dev          # sviluppo su http://localhost:4321
npm run build        # genera dist/
npm run preview      # anteprima di dist/
```
Anteprima senza Node: apri `../anteprima/` con un server statico qualsiasi, ad esempio `python -m http.server 8080` dentro `anteprima/` e vai su http://localhost:8080/ (serve un server, non basta aprire il file).

## Rigenerare i contenuti
`npm run content` (richiede Python 3 + Pillow) rilegge `../inventario/inventario.json` e `../backup/`, sceglie la sorgente migliore per ogni immagine (gimgs o dimgs), genera WebP in `public/img/` e scrive `src/data/content.json` e `public/_redirects`. E' riprendibile: se esce con codice 2 va rilanciato.

## Struttura
- `src/i18n.js` lingue (fr, it, en, ar) e testi dell'interfaccia e della bio
- `src/pages/[lang]/...` pagine (home, work, portraits, publications, about)
- `src/data/content.json` contenuti generati (in futuro: letti dal CMS)
- `public/_redirects` 301 dalle vecchie URL `/index.php/...`
- Le sezioni commerciali (Savoir Faire, Interior Design, Travels) NON sono pubblicate nella bozza: vedi `notPublished` in content.json.

## Prima del lancio
- `PUBLIC_DRAFT=false` per togliere il noindex; sostituire `public/robots.txt`.
- Servire i video da hosting proprio (ora puntano al vecchio sito).
