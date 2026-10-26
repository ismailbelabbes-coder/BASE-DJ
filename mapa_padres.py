"""Deduce la colección padre de las colecciones que no están en el menú principal.
Regla: el handle guarda la jerarquía de PrestaShop, así que el padre es la colección con el prefijo más largo.
Las de handle corto van en MANUAL. Salida: shopify/snippets/rutas-basedj-mapa.liquid (mapa dentro del tema)
y shopify/padres_por_handle.csv (para revisar)."""
import csv
from pathlib import Path
ROOT = Path(__file__).parent
A = list(csv.DictReader((ROOT / 'auditoria_migas.csv').open(encoding='utf-8-sig'), delimiter=';'))
D = {r['coleccion']: r['ruta_despues'] for r in csv.DictReader((ROOT / 'migas_despues.csv').open(encoding='utf-8-sig'), delimiter=';')}
T = {r['url'].rsplit('/', 1)[-1]: r['coleccion'] for r in A}
EN_MENU = {h for h, t in T.items() if D.get(t, '').count('»') > 1}  # la miga ya sale bien desde el menú

E = 'electricidad-electronica-varios-electronica'
HERR = E + '-varios-electronica-herramientas'
MANUAL = {
    'accesorios-microfonos-inalambricos': 'audio-y-sonido-audio-microfonos-microfonos-inalambricos',
    'altavoces-activos-amplificados': 'audio-y-sonido-audio-altavoces',
    'altavoces-activos-15-pulgadas': 'altavoces-activos-amplificados',
    'altavoces-repuesto-6-pulgadas': 'altavoces-repuesto-12-pulgadas-30cm',
    'altavoces-pasivos-10-pulgadas-25cm': 'audio-y-sonido-audio-altavoces-audio-altavoces-pasivos',
    'altavoces-pasivos-12-pulgadas-30cm': 'audio-y-sonido-audio-altavoces-audio-altavoces-pasivos',
    'subwoofers-pasivos': 'audio-y-sonido-audio-altavoces-audio-altavoces-subwoofer',
    'autotransformadores-inversores-corriente': 'electricidad',
    'baterias-plomo': 'pilas-baterias-porta-pilas',
    'pilas-de-boton': 'pilas-baterias-porta-pilas',
    'cargadores-baterias': 'pilas-baterias-porta-pilas',
    'cabinas-dj-plegables-mesas-portatiles-eventos': 'audio-y-sonido-audio-accesorios-dj',
    'condensadores-arranque': 'condensadores-electronicos',
    'controladores-dj-sin-tarjeta-sonido': 'audio-y-sonido-audio-controladores-dj',
    'controladores-midi': 'audio-y-sonido-audio-controladores-dj',
    'controladores-dj-inicio-controladores-dj-targetas-de-sonido': 'audio-y-sonido-audio-controladores-dj',
    'destornilladores': HERR,
    'soldadores': HERR,
    'disipador-de-calor-aluminio': E,
    'led-5mm': E,
    'resistencia-ntc': 'resistencias',
    'fusibles-cristal': 'fusibles-termicos-cristal',
    'fusibles-termicos': 'fusibles-termicos-cristal',
    'porta-fusibles': 'fusibles-termicos-cristal',
    'laser-dj-inicio-laser-dj-focos': 'iluminacion',
    'grabadores-digitales': 'audio-y-sonido-home-studio',
    'loop-stations': 'audio-y-sonido-home-studio',
    'repuestos-krk-monitores-estudio': 'audio-y-sonido-home-studio-audio-altavoces-monitores-de-estudio',
    'ventiladores-5v': E + '-ventiladores-5v-12v-220v-y-24v',
    'ventiladores-12v': E + '-ventiladores-5v-12v-220v-y-24v',
    'ventiladores-24v': E + '-ventiladores-5v-12v-220v-y-24v',
    'ventiladores-220v': E + '-ventiladores-5v-12v-220v-y-24v',
    'electricidad-electronica': None,  # «Electricidad y Electrónica» es de primer nivel
}
# De primer nivel: su miga «Inicio » X» ya es correcta
ARRIBA = {'alquiler', 'iluminacion', 'inicio', 'novedades', 'frontpage', 'base-dj-regalos', 'figuras-y-coleccionismo',
          'complementos-halloween-inicio-complementos-halloween-decoracion', 'repuestos-amplificadores',
          'audio-y-sonido-audio-altavoces-audio-altavoces-repuestos-altavoces'}  # en el menú está arriba
# Trozos del handle que señalan un padre más preciso que el prefijo (en orden)
CLAVES = [('baja-y-media-frecuencia', 'altavoces-repuesto-12-pulgadas-30cm'),
          ('altavoces-activos-amplificados-', 'altavoces-activos-amplificados'),
          ('pilas-baterias-porta-pilas-', 'pilas-baterias-porta-pilas'),
          ('-condensadores-', 'condensadores-electronicos'),
          ('alimentadores-fuentes-alimentacion-', 'fuentes-alimentacion'),
          ('-resistencias-', 'resistencias')]

def padre(h):
    if h in MANUAL: return MANUAL[h]
    if h in ARRIBA: return None
    for k, v in CLAVES:
        if k in h and v != h and v in T: return v
    if 'destornilladores-' in h and 'destornilladores' in T: return 'destornilladores'
    c = [o for o in T if o != h and h.startswith(o + '-')]
    return max(c, key=len) if c else None

for h, p in MANUAL.items():
    assert p is None or p in T, (h, p)

filas, entradas = [], []
for h in sorted(T):
    if h in EN_MENU: continue
    extras, cur, seen = [], h, {h}
    while True:
        p = padre(cur)
        if not p or p in seen: anchor = ''; break
        seen.add(p)
        if p in EN_MENU: anchor = p; break
        extras.insert(0, p); cur = p
    base = D.get(T[anchor], '') if anchor else 'Inicio'
    niveles = [x.strip() for x in base.split('»')]
    for x in extras + [h]:
        if T[x].strip().lower() != niveles[-1].lower(): niveles.append(T[x].strip())
    filas.append({'coleccion': T[h], 'handle': h, 'ancla_menu': anchor, 'intermedias': ','.join(extras),
                  'ruta_esperada': ' » '.join(niveles)})
    if anchor: entradas.append(f'|a:{h}={anchor}')
    if extras: entradas.append(f'|m:{h}={",".join(extras)}')

# Niveles medidos de cada colección (migas_final.csv): la ficha elige la colección más concreta
fin = ROOT / 'shopify' / 'migas_final.csv'
if fin.exists():
    for r in csv.DictReader(fin.open(encoding='utf-8-sig'), delimiter=';'):
        if int(r['niveles'] or 0) > 2: entradas.append(f"|d:{r['handle']}={r['niveles']}")
with (ROOT / 'shopify' / 'padres_por_handle.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0]), delimiter=';'); w.writeheader(); w.writerows(filas)
snip = ('{%- comment -%}Generado por mapa_padres.py: |a:handle=colección del menú| y |m:handle=intermedias|. '
        'Lo usa rutas-basedj para las colecciones que no están en el menú.{%- endcomment -%}\n'
        + ''.join(entradas) + '|')
(ROOT / 'shopify' / 'snippets' / 'rutas-basedj-mapa.liquid').write_text(snip, encoding='utf-8')
print('sin menú:', len(filas), '| con padre:', sum(1 for f in filas if f['ancla_menu'] or f['intermedias']), '| de primer nivel:', len(filas) - sum(1 for f in filas if f['ancla_menu'] or f['intermedias']))
