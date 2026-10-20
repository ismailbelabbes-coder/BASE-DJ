# BaseDJ: arreglo de rutas y velocidad (para aplicar en una copia del tema)

Todo se hace sobre una **copia del tema** (Tienda online > Temas > ... > Duplicar). La tienda publicada no se toca hasta revisarlo.

## 1. Rutas (miga de pan)

1. En la copia: Editar código > Snippets > Añadir snippet `breadcrumbs` y pegar `snippets/breadcrumbs.liquid`.
2. En la sección de la cabecera de colección y en la de producto (en el tema Ride suelen ser `sections/main-collection-banner.liquid` y `sections/main-product.liquid`), sustituir la ruta actual por:
   `{% render 'breadcrumbs' %}`
3. Comprobar varias colecciones de 1, 2 y 3 niveles y varios productos.

### Más de 3 niveles (árbol de PrestaShop)

1. Configuración > Datos personalizados > Colecciones > Añadir definición:
   nombre `Colección padre`, clave `custom.padre`, tipo **Colección** (referencia a una sola).
2. Rellenar el padre de cada colección. Hay una propuesta automática en `padres_propuestos.csv`, sacada de la ruta que se ve hoy; revisarla antes de cargarla.
3. Si una colección tiene `custom.padre`, la ruta sube por esa cadena; si no, usa el menú principal.

## 2. Velocidad en el móvil (medido el 19/10/2026 con Lighthouse, móvil simulado)

| Qué frena | Medida | Cambio propuesto |
|---|---|---|
| Barra de cookies (app Avada) | 147 KB, unos 400 ms de bloqueo; es el último elemento en pintarse de la portada | Sustituir por el aviso de cookies nativo de Shopify (Configuración > Privacidad de clientes) y desactivar la app |
| App notify-me («avísame cuando haya stock») | 94 KB, unos 120 ms de bloqueo en todas las páginas | Limitar su incrustación a las fichas de producto (Personalizar > Incrustaciones de apps) |
| Scripts del checkout en portada y colecciones | unos 350 KB | Revisar qué los carga (botones de pago dinámico, carrito lateral) y dejarlos solo en ficha y carrito |
| Google Fonts externas | 1 conexión extra antes de pintar texto | Usar la fuente desde la biblioteca de Shopify en la configuración del tema |

Medir antes y después con la misma herramienta y en las mismas páginas (portada, una colección, una ficha).

## 3. Colecciones

- Colecciones vacías: ocultar o rellenar (lista en el informe).
- Erratas en títulos: «Targetas De Sonido», «Micròfonos Usb», «Con  Tarjeta de Sonido», «Adaptadores  convertidores».
- Direcciones larguísimas: no cambiarlas sin crear redirecciones (Navegación > Redirecciones de URL), para no perder posiciones en Google.
