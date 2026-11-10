import { defineField, defineType } from 'sanity';
import { imagesField } from './shared.js';

export const gallery = defineType({
  name: 'gallery', title: 'Galerie (Portraits, Commandes)', type: 'document',
  fields: [
    defineField({ name: 'title', title: 'Nom', type: 'string', readOnly: true }),
    defineField({ name: 'key', title: 'Section', type: 'string', readOnly: true,
      options: { list: [{ value: 'portraits', title: 'Portraits' }, { value: 'savoir-faire', title: 'Savoir-faire' }, { value: 'interior-design', title: 'Interior design' }, { value: 'travels', title: 'Travels' }] } }),
    imagesField,
  ],
  preview: { select: { title: 'title', media: 'images.0.image' } },
});
