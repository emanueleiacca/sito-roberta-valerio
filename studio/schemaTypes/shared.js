import { defineField, defineType } from 'sanity';

export const THEMES = [
  { value: 'youth', title: 'Jeunesse' },
  { value: 'women', title: 'Femmes' },
  { value: 'conflict', title: 'Conflits et après-guerre' },
  { value: 'exile', title: 'Exil et migrations' },
  { value: 'borders', title: 'Frontières et divisions' },
  { value: 'environment', title: 'Territoires et environnement' },
  { value: 'education', title: 'Éducation' },
  { value: 'inclusion', title: 'Handicap et inclusion' },
  { value: 'culture', title: 'Cultures et traditions' },
  { value: 'daily', title: 'Vie quotidienne' },
];

// Elenco paesi (codice ISO) con nome in francese, ordinato alfabeticamente.
const fr = new Intl.DisplayNames(['fr'], { type: 'region' });
const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
export const PLACES = [];
for (const a of A) for (const b of A) {
  const code = a + b;
  let name;
  try { name = fr.of(code); } catch { continue; }
  if (!name || name === code || /inconnue|indéterminée|\bZZ\b/i.test(name) || ['EU', 'UN', 'QO', 'EZ', 'AC', 'CP', 'DG', 'EA', 'IC', 'TA', 'XA', 'XB'].includes(code)) continue;
  PLACES.push({ value: code, title: name });
}
PLACES.sort((x, y) => x.title.localeCompare(y.title, 'fr'));

export const themesField = defineField({
  name: 'themes', title: 'Thèmes', type: 'array', of: [{ type: 'string' }],
  options: { list: THEMES, layout: 'tags' },
  description: 'Facultatif. Permet de regrouper les reportages (filtres du site).',
});
export const placesField = defineField({
  name: 'places', title: 'Pays', type: 'array', of: [{ type: 'string' }],
  options: { list: PLACES, layout: 'tags' },
  description: 'Facultatif.',
});

export const photo = defineType({
  name: 'photo', title: 'Photo', type: 'object',
  fields: [
    defineField({ name: 'image', title: 'Photo', type: 'image', validation: (r) => r.required() }),
    defineField({ name: 'caption', title: 'Légende (facultatif)', type: 'string', description: 'Lieu, date, nom de la personne…' }),
    defineField({ name: 'diptych', title: 'Deux photos côte à côte (diptyque)', type: 'boolean', initialValue: false,
      description: 'À cocher si l’image contient deux photos juxtaposées : sur téléphone elles seront affichées l’une sous l’autre.' }),
    defineField({ name: 'splitAt', title: 'Position de la séparation (0 = gauche, 1 = droite)', type: 'number', initialValue: 0.5,
      hidden: ({ parent }) => !parent?.diptych, validation: (r) => r.min(0.2).max(0.8) }),
  ],
  preview: { select: { title: 'caption', media: 'image' }, prepare: ({ title, media }) => ({ title: title || 'Photo', media }) },
});

export const imagesField = defineField({
  name: 'images', title: 'Photos', type: 'array', of: [{ type: 'photo' }],
  description: 'Glissez-déposez pour changer l’ordre. La première photo sert de couverture.',
});
