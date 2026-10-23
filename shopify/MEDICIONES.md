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

## Tras aligerar el menú del móvil (mediana de 3 pasadas)

| Página | Publicado | Copia final |
|---|---|---|
| Portada | 55 · LCP 4,4 s · TBT 658 ms | 56 · LCP 3,7 s · TBT 390 ms |
| Colección | 84 · LCP 1,8 s · TBT 526 ms | 85 · LCP 1,7 s · TBT 458 ms |
| Ficha | 69 · LCP 3,2 s · TBT 962 ms | 73 · LCP 2,3 s · TBT 848 ms |

Elementos en la portada: 2.567 → 1.700. El menú del móvil se monta al abrirlo (probado: abre, submenús, volver y cerrar, sin errores).
La nota apenas sube porque el bloqueo restante viene de las apps (GTM, Avada, notify-me) y de los scripts de pago, que no se han tocado.

Cambios en la copia: miga de pan nueva (`snippets/breadcrumbs-basedj.liquid`) y prioridad alta para la imagen principal de la ficha (`snippets/product-thumbnail.liquid`). La prioridad en las tarjetas de portada no mejoró y se deshizo. Menú del móvil diferido (`snippets/header-drawer.liquid`). Diferencias completas en `cambios_tema.patch`.
