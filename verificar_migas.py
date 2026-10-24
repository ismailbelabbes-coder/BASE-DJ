"""Recorre las 313 colecciones en la copia del tema y comprueba la miga de pan.
Salida: shopify/migas_final.csv (antes, después, niveles y problemas)."""
import csv, time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).parent
TEMA = '210436718930'
A = list(csv.DictReader((ROOT / 'auditoria_migas.csv').open(encoding='utf-8-sig'), delimiter=';'))
ESP = {r['handle']: r['ruta_esperada'] for r in csv.DictReader((ROOT / 'shopify' / 'padres_por_handle.csv').open(encoding='utf-8-sig'), delimiter=';')}
HANDLES = {r['url'].rsplit('/', 1)[-1] for r in A}
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
out = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(user_agent=UA)
    for i, r in enumerate(A):
        h = r['url'].rsplit('/', 1)[-1]
        for intento in range(3):
            try:
                pg.goto(f'https://www.basedj.es/collections/{h}?preview_theme_id={TEMA}', wait_until='domcontentloaded', timeout=45000)
                items = pg.eval_on_selector_all('nav.breadcrumbs li', 'els=>els.map(e=>{const a=e.querySelector("a");return [e.innerText.trim(), a?a.getAttribute("href"):""]})')
                break
            except Exception as ex:
                items = None; time.sleep(10)
        if items is None:
            out.append({'coleccion': r['coleccion'], 'handle': h, 'ruta_antes': r['ruta_actual'], 'ruta_despues': '', 'niveles': 0, 'problemas': 'no cargó'}); continue
        textos = [t for t, _ in items]
        prob = []
        if not textos or ' '.join(textos[-1].lower().split()) != ' '.join(r['coleccion'].lower().split()): prob.append('no termina en la colección')
        if any(textos[k].lower() == textos[k + 1].lower() for k in range(len(textos) - 1)): prob.append('nivel repetido')
        for t, href in items[1:-1]:
            hh = (href or '').split('?')[0].rstrip('/')
            if '/collections/' not in hh or hh.rsplit('/', 1)[-1] not in HANDLES: prob.append(f'enlace raro: {t}')
        ruta = ' » '.join(textos)
        if h in ESP and ruta != ESP[h]: prob.append('distinta de la esperada: ' + ESP[h])
        out.append({'coleccion': r['coleccion'], 'handle': h, 'ruta_antes': r['ruta_actual'], 'ruta_despues': ruta,
                    'niveles': len(textos), 'problemas': '; '.join(prob) or 'ok'})
        if i % 25 == 0: print(i, ruta[:90], flush=True)
        time.sleep(1.5)
    b.close()
with (ROOT / 'shopify' / 'migas_final.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter=';'); w.writeheader(); w.writerows(out)
from collections import Counter
print('ok:', sum(o['problemas'] == 'ok' for o in out), 'de', len(out))
print(Counter(p.split(':')[0] for o in out for p in o['problemas'].split('; ') if o['problemas'] != 'ok'))
print('solo Inicio » colección:', sum(o['niveles'] == 2 for o in out))
