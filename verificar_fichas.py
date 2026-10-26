"""Abre fichas de producto directamente (sin colección en la URL) en la copia del tema y muestra su miga.
Toma el primer producto de cada N colecciones. Salida: shopify/fichas_muestra.csv"""
import csv, time, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).parent
TEMA = '210436718930'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
F = list(csv.DictReader((ROOT / 'shopify' / 'migas_final.csv').open(encoding='utf-8-sig'), delimiter=';'))
paso = int(sys.argv[1]) if len(sys.argv) > 1 else 8
out = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(user_agent=UA)
    lista = F[::paso]
    for i, r in enumerate(lista):
        print(f'PROGRESO {i + 1}/{len(lista)}', flush=True)
        if int(r['niveles'] or 0) < 3: continue
        try:
            pg.goto(f"https://www.basedj.es/collections/{r['handle']}?preview_theme_id={TEMA}", wait_until='domcontentloaded', timeout=45000)
            href = pg.eval_on_selector('main a[href*="/products/"]', 'a=>a.getAttribute("href")')
            prod = '/products/' + href.split('/products/')[1].split('?')[0]
            pg.goto(f'https://www.basedj.es{prod}?preview_theme_id={TEMA}', wait_until='domcontentloaded', timeout=45000)
            migas = pg.eval_on_selector_all('nav.breadcrumbs li', 'e=>e.map(x=>x.innerText.trim())')
            ld = pg.evaluate('''[...document.querySelectorAll('script[type="application/ld+json"]')].every(s=>{try{JSON.parse(s.textContent);return true}catch(e){return false}})''')
        except Exception as ex:
            continue
        n = len(migas) - 1
        rep = any(migas[k].lower() == migas[k + 1].lower() for k in range(len(migas) - 1))
        out.append({'producto': prod, 'desde_coleccion': r['coleccion'], 'miga': ' » '.join(migas), 'niveles': len(migas),
                    'problema': ('corta' if n < 3 else '') + (' repetido' if rep else '') + ('' if ld else ' json-ld'), })
        time.sleep(1.5)
    b.close()
with (ROOT / 'shopify' / 'fichas_muestra.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter=';'); w.writeheader(); w.writerows(out)
print('fichas:', len(out), '| cortas (Inicio » 1 colección » producto):', sum('corta' in o['problema'] for o in out),
      '| repetidas:', sum('repetido' in o['problema'] for o in out), '| JSON-LD roto:', sum('json-ld' in o['problema'] for o in out))
for o in out[:12]: print(' ', o['miga'][:130])
