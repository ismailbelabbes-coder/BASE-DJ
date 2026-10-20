"""Auditoría rápida de las colecciones de basedj.es: migas de pan, colecciones vacías, URLs largas y títulos raros."""
import json, re, sys, urllib.request as u, collections as C
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0'}
SHOP = 'https://www.basedj.es'

def get(url):
    return u.urlopen(u.Request(url, headers=H), timeout=40).read().decode('utf8', 'ignore')

cols = []
for page in range(1, 6):
    batch = json.loads(get(f'{SHOP}/collections.json?limit=250&page={page}'))['collections']
    cols += batch
    if len(batch) < 250:
        break

def check(c):
    try:
        h = get(f"{SHOP}/collections/{c['handle']}")
    except Exception as e:
        return c['handle'], None, str(e)[:40]
    has = bool(re.search(r'breadcrumb|BreadcrumbList|aria-label="(Ruta|Breadcrumb)', h, re.I))
    return c['handle'], has, ''

with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(check, cols))

sin = [h for h, ok, _ in res if ok is False]
err = [(h, e) for h, ok, e in res if ok is None]
vacias = [c['handle'] for c in cols if c.get('products_count') == 0]
largas = [c['handle'] for c in cols if len(c['handle']) > 60]
titulos = C.Counter(c['title'].strip().lower() for c in cols)
dup = [t for t, n in titulos.items() if n > 1]
raras = [c['title'] for c in cols if re.search(r'(?i)targeta|micròfono|ò|  |^\s|\s$', c['title'])]

out = {'total': len(cols), 'sin_migas': len(sin), 'con_migas': sum(1 for _, ok, _ in res if ok), 'errores': err,
       'vacias': vacias, 'urls_largas': len(largas), 'titulos_duplicados': dup, 'titulos_raros': raras,
       'ej_sin_migas': sin[:8], 'ej_largas': largas[:3]}
json.dump(out, open('auditoria_colecciones.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, ':', v if not isinstance(v, list) else (len(v), v[:6]))
