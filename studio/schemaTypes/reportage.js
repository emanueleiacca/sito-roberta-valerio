import { defineField, defineType } from 'sanity';
import { themesField, placesField, imagesField } from './shared.js';

export const reportage = defineType({
  name: 'reportage', title: 'Reportage', type: 'document',
  fields: [
    defineField({ name: 'title', title: 'Titre', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'slug', title: 'Adresse web', type: 'slug', options: { source: 'title', maxLength: 80 }, validation: (r) => r.required(),
      description: 'Cliquer sur « Generate ». Ne plus la changer après publication.' }),
    placesField,
    defineField({ name: 'year', title: 'Année', type: 'number', validation: (r) => r.min(1990).max(2100).integer() }),
    themesField,
    defineField({ name: 'text', title: 'Texte', type: 'text', rows: 12, description: 'Paragraphes séparés par une ligne vide. Facultatif.' }),
    defineField({ name: 'textLang', title: 'Langue du texte', type: 'string', initialValue: 'fr', options: { list: [{ value: 'fr', title: 'Français' }, { value: 'en', title: 'English' }, { value: 'it', title: 'Italiano' }] } }),
    defineField({ name: 'video', title: 'Vidéo (adresse du fichier, facultatif)', type: 'url' }),
    imagesField,
    defineField({ name: 'featured', title: 'À la une', type: 'boolean', initialValue: false }),
    defineField({ name: 'position', title: 'Position dans la liste (facultatif)', type: 'number',
      description: 'Laisser vide : le nouveau reportage apparaît en premier. 1 = tout en haut parmi les anciens.' }),
  ],
  orderings: [{ title: 'Ordre du site', name: 'site', by: [{ field: 'position', direction: 'asc' }] }],
  preview: { select: { title: 'title', subtitle: 'year', media: 'images.0.image' } },
});
