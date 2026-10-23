# Mediciones en la copia del tema (23/10/2026)

Lighthouse 12.8 en móvil simulado. Mediana de 3 pasadas por página. Mismas URL en el tema publicado (Ride) y en la copia.

| Página | Tema | Nota | LCP | TBT |
|---|---|---|---|---|
| Portada | publicado | 55 | 4,4 s | 658 ms |
| Portada | copia | 53 | 4,8 s | 353 ms |
| Colección (electricidad) | publicado | 84 | 1,8 s | 526 ms |
| Colección (electricidad) | copia | 85 | 1,9 s | 466 ms |
| Ficha | publicado | 69 | 3,2 s | 962 ms |
| Ficha | copia | 71 | 2,8 s | 1085 ms |

Elemento LCP: portada, imagen de la primera tarjeta de producto; colección, un texto (`<p>`); ficha, la imagen principal del producto.

Qué pesa (portada): Google Tag Manager 154 KB, Avada (cookies) 108 KB, notify-me 98 KB y scripts de Shopify/pagos unos 500 KB. HTML de 82 KB comprimido y 2.455 elementos, por el menú completo.

Cambios en la copia: miga de pan nueva (`snippets/breadcrumbs-basedj.liquid`) y prioridad alta para la imagen principal de la ficha (`snippets/product-thumbnail.liquid`). La prioridad en las tarjetas de portada no mejoró y se deshizo.
