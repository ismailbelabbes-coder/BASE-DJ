"""Propone la colección padre de cada colección a partir de la ruta que se ve hoy (auditoria_migas.csv).
La ruta actual termina justo antes de la colección, así que su último nivel suele ser el padre real.
Salida: shopify/padres_propuestos.csv (para revisar antes de cargar el metacampo custom.padre)."""
import csv
from pathlib import Path
ROOT = Path(__file__).parent
rows = list(csv.DictReader((ROOT / 'auditoria_migas.csv').open(encoding='utf-8-sig'), delimiter=';'))
por_titulo = {}
for r in rows:
    por_titulo.setdefault(r['coleccion'].strip().lower(), r['url'].rsplit('/', 1)[-1])

out, sin = [], 0
for r in rows:
    partes = [x.strip() for x in r['ruta_actual'].split('»') if x.strip()]
    propio = r['coleccion'].strip().lower()
    cand = [p for p in partes[1:] if p.lower() != propio]  # sin «Inicio» ni la propia
    padre_t = cand[-1] if cand else ''
    padre_h = por_titulo.get(padre_t.lower(), '')
    nota = '' if padre_h else ('sin padre en la ruta' if not padre_t else 'el padre es un nivel del menú sin colección propia')
    sin += not padre_h
    out.append({'coleccion': r['coleccion'], 'handle': r['url'].rsplit('/', 1)[-1], 'padre_propuesto': padre_t,
                'padre_handle': padre_h, 'nota': nota})

dest = ROOT / 'shopify' / 'padres_propuestos.csv'
with dest.open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter=';'); w.writeheader(); w.writerows(out)
print('propuestas:', len(out) - sin, 'de', len(out), '| a revisar a mano:', sin)
