"""Recorre todas las colecciones de basedj.es despacio y anota la miga de pan que se ve y si está mal.
Salida: auditoria_migas.csv (se abre en Excel). Uso: python auditoria_migas.py"""
import csv, json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
U = 'https://www.basedj.es'
OUT = Path(__file__).with_name('auditoria_migas.csv')

JS_RUTA = r'''(() => {
  const c = [...document.querySelectorAll('nav,ol,ul,div,p')].filter(e => /breadcrumb/i.test(e.className + ' ' + (e.getAttribute('aria-label') || '')) && e.offsetParent !== null);
  return c.length ? c[0].innerText.replace(/\s+/g, ' ').trim() : '';
})()'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    cols = []
    for page in range(1, 6):
        pg.goto(f'{U}/collections.json?limit=250&page={page}')
        batch = json.loads(pg.inner_text('body'))['collections']
        cols += batch
        if len(batch) < 250:
            break
        time.sleep(3)
    rows = []
    for i, c in enumerate(cols, 1):
        ruta, titulo, estado = '', c['title'].strip(), 'ok'
        for intento in range(3):
            try:
                r = pg.goto(f"{U}/collections/{c['handle']}", wait_until='domcontentloaded', timeout=45000)
                if r and r.status == 429:
                    time.sleep(20); continue
                pg.wait_for_timeout(1200)
                ruta = pg.evaluate(JS_RUTA)
                break
            except Exception:
                time.sleep(10)
        partes = [x.strip() for x in ruta.split('»') if x.strip()]
        problemas = []
        if not partes:
            problemas.append('no se ve la ruta')
        else:
            if partes[-1].lower() != titulo.lower():
                problemas.append('no termina en la propia colección')
            if len(partes) != len(set(x.lower() for x in partes)):
                problemas.append('nivel repetido')
        rows.append({'coleccion': titulo, 'url': f"{U}/collections/{c['handle']}", 'productos': c.get('products_count'),
                     'ruta_actual': ruta, 'problemas': '; '.join(problemas) or 'ok'})
        if i % 20 == 0:
            print(i, '/', len(cols), flush=True)
        time.sleep(2.5)  # ritmo lento para no cargar su tienda
    b.close()

with OUT.open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
    w.writeheader(); w.writerows(rows)
mal = [r for r in rows if r['problemas'] != 'ok']
print('total', len(rows), '| con problemas', len(mal))
from collections import Counter
print(Counter(p for r in mal for p in r['problemas'].split('; ')).most_common())
