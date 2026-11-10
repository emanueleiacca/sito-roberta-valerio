import { defineField, defineType } from 'sanity';
import { themesField, placesField, imagesField } from './shared.js';

export const publication = defineType({
  name: 'publication', title: 'Publication (presse)', type: 'document',
  fields: [
    defineField({ name: 'title', title: 'Titre', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'outlet', title: 'Magazine ou journal', type: 'string' }),
    defineField({ name: 'slug', title: 'Adresse web', type: 'slug', options: { source: 'title', maxLength: 80 }, validation: (r) => r.required() }),
    placesField,
    themesField,
    imagesField,
    defineField({ name: 'position', title: 'Position dans la liste (facultatif)', type: 'number', description: 'Laisser vide : apparaît en premier.' }),
  ],
  preview: { select: { title: 'title', subtitle: 'outlet', media: 'images.0.image' } },
});
