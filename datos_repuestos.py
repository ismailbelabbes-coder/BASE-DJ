"""Descarga datos y fotos reales de repuestos de basedj.es para la demo (img/r_*.webp y repuestos.json)."""
import io, json, re, sys, urllib.request as u
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0'}
SHOP = 'https://www.basedj.es'

def get(url):
    return u.urlopen(u.Request(url, headers=H), timeout=40).read()

def foto(src, nombre, w=560):
    I = Image.open(io.BytesIO(get(src.split('?')[0] + f'?width={w}'))).convert('RGBA')
    bg = Image.new('RGBA', I.size, (255, 255, 255, 255)); bg.alpha_composite(I)
    bg.convert('RGB').save(f'img/{nombre}.webp', 'WEBP', quality=78)
    return f'img/{nombre}.webp'

# Secciones de repuestos (colección real, nombre corto para el cliente)
CATS = [
    ('audio-y-sonido-audio-altavoces-audio-altavoces-repuestos-altavoces', 'Altavoces y woofers'),
    ('repuestos-altavoces-membranas-y-tweeters-membranas', 'Membranas y tweeters'),
    ('audio-y-sonido-audio-auriculares-audio-auriculares-repuestos-auriculares', 'Almohadillas y auriculares'),
    ('repuestos-mezcladores', 'Faders y mezcladores'),
    ('audio-y-sonido-audio-giradiscos-audio-giradiscos-capsulas-agujas-accesorios', 'Agujas y cápsulas'),
    ('fuentes-alimentacion', 'Alimentadores'),
    ('cables-audio-hechos-a-mano-a-medida', 'Cables a medida'),
    ('correa-repuesto-giradiscos', 'Correas de giradiscos'),
]
out = {'cats': [], 'destacados': [], 'ficha': None}
for i, (h, nombre) in enumerate(CATS):
    col = json.loads(get(f'{SHOP}/collections/{h}.json'))['collection']
    prods = json.loads(get(f'{SHOP}/collections/{h}/products.json?limit=12'))['products']
    p = next(x for x in prods if x['images'])
    out['cats'].append({'handle': h, 'name': nombre, 'count': col.get('products_count'), 'img': foto(p['images'][0]['src'], f'r_cat{i}', 480), 'from': p['title']})
    print('cat', nombre, col.get('products_count'), '|', p['title'][:60])

ps = {p['handle']: p for p in json.load(open('products_raw.json', encoding='utf-8'))}
DEST = [
    ('pioneer-x5-repuesto-almohadillas', 'Almohadillas Pioneer HDJ-X5', 'Cuero sintético, 85 mm'),
    ('pioneer-dj-dcv1035-fader-ddj-rev1-rev5-flx4-flx6-flx10', 'Fader Pioneer DJ DCV1035', 'Para DDJ-FLX4, FLX6, REV1...'),
    ('almohadillas-de-repuesto-compatibles-con-pioneer-hdj-cx', 'Almohadillas Pioneer HDJ-CX', 'Compatibles, par'),
    ('4261-membrana-beyma-cp-21-22-25', 'Membrana Beyma CP-21/22/25', 'Para driver de compresión'),
    ('pioneer-dj-dcv1023-crossfader', 'Crossfader Pioneer DCV1023', 'Repuesto original'),
    ('aguja-tocadiscos-fox-540-dst-w', 'Aguja FOX 540 DST-W', 'Compatible con Dual D-201'),
    ('almohadillas-repuesto-sennheiser-hd598-hd558-hd518-hd599-hd569-40mm', 'Almohadillas Sennheiser HD598', 'También HD558, HD518, HD599...'),
    ('1-pieza-diafragma-de-tweeter-de-25-4-mm-1-pulgada-para-bocina-de-agudo', 'Diafragma de tweeter 1"', '25,4 mm, para bocina de agudos'),
]
for i, (h, nombre, sub) in enumerate(DEST):
    h = next(k for k in ps if k.startswith(h))  # admite identificadores recortados
    p = ps[h]
    v = p['variants'][0]
    out['destacados'].append({'handle': h, 'name': nombre, 'sub': sub, 'price': v['price'], 'available': v['available'], 'img': foto(p['images'][0]['src'], f'r_p{i}')})
    print('dest', nombre, v['price'], v['available'])

f = ps['pioneer-dj-dcv1035-fader-ddj-rev1-rev5-flx4-flx6-flx10']
desc = re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', f['body_html'] or '')).strip()
out['ficha'] = {'title': f['title'], 'vendor': f['vendor'], 'price': f['variants'][0]['price'], 'available': f['variants'][0]['available'],
                'sku': f['variants'][0].get('sku'), 'variant': f['variants'][0]['id'],
                'imgs': [foto(im['src'], f'r_f{j}', 900) for j, im in enumerate(f['images'][:4])], 'desc': desc}
json.dump(out, open('repuestos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ficha', f['title'], f['variants'][0]['price'], len(out['ficha']['imgs']), 'imgs')
print(desc[:1400])
