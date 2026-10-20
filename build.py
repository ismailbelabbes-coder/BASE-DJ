"""Monta dist/: rellena productos y canales, incrusta iconos y compila Tailwind."""
import math, re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / 'src', ROOT / 'dist'
SHOP = 'https://www.basedj.es'

# Productos reales de basedj.es (nombre, subtítulo, precio, foto, enlace)
P = {
    'flx2':   ('Pioneer DJ DDJ-FLX2', 'Controlador DJ de dos canales', 179, 'p0_0', 'ficha.html'),
    'rp5000': ('Reloop RP-5000 MK4', 'Giradiscos DJ de tracción directa', 384, 'p1_0', '/products/reloop-rp-5000-mk4-giradiscos-dj-traccion-directa'),
    'warm2':  ('Ecler WARM2', 'Mezclador DJ de dos canales', 645, 'p2_0', '/products/10291-ecler-warm2-mezclador-dj-2-canales'),
    'krk8':   ('KRK Kreate 8', 'Monitor de estudio con Bluetooth', 199, 'p3_0', '/products/krk-kreate-8-monitor-estudio-8-bluetooth-eq'),
    'edge':   ('BeamZ ShowBar GO Edge', 'Barra LED con cabezas móviles', 629, 'p4_0', '/products/beamz-showbar-go-edge-barra-con-4-cabezas-moviles-y-barra-led-estroboscopica'),
    'glow':   ('BeamZ ShowBar GO Glow', 'Sistema de iluminación multiefectos DMX', 529, 'p5_0', '/products/beamz-showbar-go-glow-moving-heads-derby-par-strobo'),
    'pack':   ('Pack Halloween UV y humo', 'Pack de iluminación y humo', 129, 'p6_0', '/products/pack-halloween-uv-humo-liquido-1l-strobo-st60'),
    'dbf105': ('Vonyx DBF105', 'Cabina DJ plegable con fundas', 195, 'p7_0', '/products/vonyx-dbf105-cabina-dj-plegable-pro-quick-1m-licra'),
    'hc200':  ('Behringer HC 200', 'Auriculares DJ cerrados', '19,90', 'p8_0', '/products/behringer-hc-200-auriculares-dj-over-ear-cerrados-64ω'),
    'pack90': ('Pack Halloween', 'Foco UV, máquina de humo y líquido', 90, 'p10_0', '/products/pack-halloween-foco-uv-maquina-humo-liquido-1l'),
    'pack208': ('Pack Halloween humo 900 W', 'Humo, strobo y 2 focos UV', 208, 'p9_0', '/products/pack-halloween-humo-900w-strobo-60w-2-focos-uv'),
}
SETS = {
    'sonido': ['flx2', 'rp5000', 'warm2', 'krk8'],
    'luz': ['edge', 'glow', 'pack', 'dbf105'],
    'completa': ['hc200', 'krk8', 'dbf105'],
    'temporada': ['pack90', 'pack208'],
}
# Canales: colección real y nº de productos publicado en la tienda
CHANNELS = [
    ('Controladoras', 'audio-y-sonido-audio-controladores-dj', 119),
    ('Altavoces', 'altavoces-activos-amplificados', 92),
    ('Micrófonos', 'audio-y-sonido-audio-microfonos', 354),
    ('Cabezas móviles', 'iluminacion-iluminacion-cabezas-moviles', 36),
    ('Humo y FX', 'maquinas-de-humo-y-efectos', 46),
    ('Cabinas', 'cabinas-dj-plegables-mesas-portatiles-eventos', 14),
]


def url(href):
    return href if href.endswith('.html') else SHOP + href


def card(key, lazy=True, compact=False):
    name, sub, price, img, href = P[key]
    ext = '' if href.endswith('.html') else ' target="_blank" rel="noopener"'
    if compact:
        return f'''<li>
  <a href="{url(href)}"{ext} class="group flex items-center gap-4 md:block">
    <div class="plate aspect-square w-28 shrink-0 rounded-[6px] md:aspect-[4/5] md:w-auto md:rounded-[6px]"><img src="img/{img}.webp" alt="{name}" width="640" height="640" loading="lazy" class="h-full w-full object-contain p-[12%]"></div>
    <div class="min-w-0 flex-1 md:mt-4 md:flex md:items-start md:justify-between md:gap-3">
      <div class="min-w-0"><p class="text-[15px] font-bold leading-snug">{name}</p><p class="mt-1 text-[14px] text-mute">{sub}</p></div>
      <p class="mt-2 font-display text-[20px] italic leading-none md:mt-0 md:shrink-0">{price}&nbsp;€</p>
    </div>
  </a>
</li>'''
    li = 'w-[68%] shrink-0 snap-start sm:w-[44%] md:w-auto'
    return f'''<li class="{li}">
  <a href="{url(href)}"{ext} class="group block">
    <div class="plate aspect-[4/5] rounded-[6px]"><img src="img/{img}.webp" alt="{name}" width="640" height="640"{' loading="lazy"' if lazy else ''} class="h-full w-full object-contain p-[12%]"></div>
    <div class="mt-4 flex items-start justify-between gap-3">
      <div class="min-w-0"><p class="text-[15px] font-bold leading-snug">{name}</p><p class="mt-1 text-[14px] text-mute">{sub}</p></div>
      <p class="shrink-0 font-display text-[20px] italic leading-none">{price}&nbsp;€</p>
    </div>
  </a>
</li>'''


def channel(name, handle, count, n=0):
    level = max(2, round(math.log(count) / math.log(400) * 10))
    segs = ''.join(  # --i: orden de encendido de abajo arriba en la prueba de sonido
        f'<i class="{"on" if i < level else ""}{" hot" if i < level and i >= level - 2 else ""}" style="--i:{i + n * 2}"></i>'
        for i in range(10))
    segs = ''.join(reversed(re.findall(r'<i[^>]*></i>', segs)))  # el más alto arriba
    return f'''<li class="w-[112px] shrink-0 md:w-auto">
  <a href="{SHOP}/collections/{handle}" target="_blank" rel="noopener" class="channel flex h-full flex-col items-center gap-4 rounded-[6px] px-2 py-4 text-center transition hover:bg-white/[0.04]">
    <span class="flex h-[150px] items-end gap-3" aria-hidden="true">
      <span class="meter grid w-2.5 gap-[3px]">{segs}</span>
      <span class="relative h-full w-1.5 rounded-[6px] bg-black/50"><span style="--n:{n}" class="cap absolute -left-[13px] bottom-1 h-6 w-8 rounded-[5px] border border-white/15 bg-gradient-to-b from-[#3a343c] to-[#221e24] shadow-[0_6px_12px_rgba(0,0,0,.5)]"><span class="absolute inset-x-1 top-1/2 h-px bg-volt"></span></span></span>
    </span>
    <span class="text-[14px] font-bold leading-tight [text-wrap:balance]">{name}</span>
    <span class="-mt-3 text-[13px] text-mute">{count} productos</span>
  </a>
</li>'''


def icons(html):
    def rep(m):
        name, cls = m.group(1), m.group(2)
        svg = (ROOT / 'icons' / f'{name}.svg').read_text(encoding='utf-8')
        svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S).strip()
        svg = re.sub(r'\s(class|width|height)="[^"]*"', '', svg)
        if 'stroke=' not in svg:  # simple-icons: rellenos
            svg = svg.replace('<svg', '<svg fill="currentColor"', 1)
        svg = re.sub(r'<title>.*?</title>', '', svg)
        return svg.replace('<svg', f'<svg class="{cls}" aria-hidden="true" focusable="false"', 1)
    return re.sub(r'<i data-i="([\w-]+)" class="([^"]*)"></i>', rep, html)


# ---------- Versión repuestos (datos de repuestos.json, sacados de basedj.es) ----------
import json
R = json.loads((ROOT / 'repuestos.json').read_text(encoding='utf-8'))
CHIPS = ['HDJ-X5', 'HDJ-CX', 'DDJ-FLX4', 'HD598', 'Beyma CP-22', 'DCV1035']
REL = [  # repuestos relacionados con el fader (nombre, precio, foto, enlace)
    ('Crossfader DCV1023', 'Crossfader de repuesto', 35, 'r_p4', '/products/pioneer-dj-dcv1023-crossfader'),
    ('Pitch fader DCV1009', 'Pitch fader de repuesto', 35, 'r_cat3', '/products/pioneer-dj-dcv1009-pitch-fader'),
    ('Almohadillas Pioneer HDJ-X5', 'Cuero sintético, 85 mm', 10, 'r_p0', '/products/pioneer-x5-repuesto-almohadillas'),
]


def price(v):
    v = float(v)
    return (f'{v:.2f}'.replace('.', ',') if v % 1 else f'{v:.0f}') + '&nbsp;€'


def rcard(name, sub, pr, img, href):
    link = href if href.endswith('.html') else SHOP + href
    return f'''<li class="w-[64%] shrink-0 snap-start sm:w-[40%] md:w-auto">
  <a href="{link}" class="group block">
    <div class="plate aspect-square rounded-[6px]"><img src="{img}" alt="{name}" width="560" height="560" loading="lazy" class="h-full w-full object-contain p-[12%]"></div>
    <p class="mt-4 text-[15px] font-bold leading-snug group-hover:text-volt">{name}</p>
    <p class="mt-1 text-[14px] text-mute">{sub}</p>
    <p class="mt-2 font-display text-[20px] italic leading-none">{price(pr)}</p>
  </a>
</li>'''


def repuestos_html(html):
    chips = ''.join(f'<a class="rounded-[6px] border border-white/15 px-3.5 py-2.5 transition hover:border-volt hover:text-volt" href="{SHOP}/search?q={c.replace(" ", "+")}&amp;type=product">{c}</a>' for c in CHIPS)
    cats = '\n'.join(f'''<li>
  <a href="{SHOP}/collections/{c['handle']}" class="tile group flex h-full flex-col rounded-[6px] border border-white/[0.08] bg-ink/70 p-3 hover:border-volt/60">
    <div class="plate aspect-[4/3] rounded-[6px]"><img src="{c['img']}" alt="" width="480" height="480" loading="lazy" class="h-full w-full object-contain p-[10%]"></div>
    <p class="mt-4 px-1 text-[16px] font-bold leading-snug group-hover:text-volt">{c['name']}</p>
    <div class="mt-1 flex items-center justify-between gap-2 px-1 pb-1"><p class="whitespace-nowrap text-[13px] text-mute sm:text-[14px]">{c['count']} productos</p><span class="go grid h-7 w-7 shrink-0 place-items-center rounded-full bg-white/[0.06] text-cream"><i data-i="chevron-right" class="ico"></i></span></div>
  </a>
</li>''' for c in R['cats'])
    dest = '\n'.join(rcard(d['name'], d['sub'], d['price'], d['img'], '/products/' + d['handle']) for d in R['destacados'] if d['available'])
    rel = '\n'.join(rcard(n, s, p, f'img/{i}.webp', h) for n, s, p, i, h in REL)
    models = ''.join(f'<li class="model-chip inline-flex items-center gap-1.5 rounded-[6px] bg-volt/10 px-3 py-1.5 text-[14px] font-medium"><i data-i="check" class="ico !h-3.5 !w-3.5 text-volt"></i>{m}</li>'
                     for m in ['DDJ-REV1', 'DDJ-REV5', 'DDJ-FLX4', 'DDJ-FLX6', 'DDJ-FLX6-GT', 'DDJ-FLX10'])
    for k, v in {'<!--CHIPS-->': chips, '<!--CATS-->': cats, '<!--PRODUCTS:repuestos-->': dest, '<!--PRODUCTS:rel-->': rel, '<!--MODELS-->': models}.items():
        html = html.replace(k, v)
    return html


def eq_bars(n=28):
    """Barras del ecualizador: graves altos a la izquierda, agudos más bajos y rápidos."""
    out = []
    for i in range(n):
        f = i / (n - 1)
        h = 0.35 + 0.6 * (1 - f) * (0.6 + 0.4 * math.sin(i * 1.7) ** 2)
        d = 0.42 + 0.5 * (1 - f) + 0.12 * math.cos(i * 2.3)
        out.append(f'<i style="--h:{h:.2f};--d:{d:.2f}s;--dl:-{(i * 0.37) % 1:.2f}s"></i>')
    return ''.join(out)


def wave_svg(w=360, h=14):
    """Forma de onda que se repite bajo la cabecera."""
    bars = []
    for x in range(0, w, 3):
        a = abs(math.sin(x * 0.05) * 0.55 + math.sin(x * 0.013 + 1) * 0.35 + math.sin(x * 0.21) * 0.1)
        bh = max(2, round(a * h))
        bars.append(f'<rect x="{x}" y="{(h - bh) / 2:.1f}" width="2" height="{bh}" rx="1"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(bars)}</svg>'


def main():
    (DIST / 'img').mkdir(parents=True, exist_ok=True)
    (DIST / 'img' / 'wave.svg').write_text(wave_svg(), encoding='utf-8')
    for f in (ROOT / 'img').glob('*.webp'):
        shutil.copy(f, DIST / 'img' / f.name)
    shutil.copytree(ROOT / 'fonts', DIST / 'fonts', dirs_exist_ok=True)
    for f in (ROOT / 'archive').glob('*.html'):  # versión con ambiente DJ, ya compilada
        shutil.copy(f, DIST / f.name)
    pages = {}
    for page in ('index.html', 'ficha.html'):
        html = (SRC / page).read_text(encoding='utf-8')
        for s, keys in SETS.items():
            html = html.replace(f'<!--PRODUCTS:{s}-->', '\n'.join(card(k, compact=(s == 'temporada')) for k in keys))
        html = html.replace('<!--HEADER-->', (SRC / 'header.html').read_text(encoding='utf-8'))
        html = html.replace('<!--CHANNELS-->', '\n'.join(channel(*c, n=k) for k, c in enumerate(CHANNELS)))
        html = html.replace('<!--EQ-->', eq_bars())
        html = repuestos_html(html)
        (SRC / f'_{page}').write_text(html, encoding='utf-8')  # para que Tailwind vea las clases generadas
        pages[page] = icons(html)
    subprocess.run('npx -y tailwindcss@3.4.17 -c tailwind.config.js -i src/input.css -o dist/app.css --minify',
                   cwd=ROOT, shell=True, check=True)
    for f in SRC.glob('_*.html'):
        f.unlink()
    # CSS incrustado: una petición bloqueante menos en móvil
    css = (DIST / 'app.css').read_text(encoding='utf-8')
    for page, html in pages.items():
        html = html.replace('<link rel="stylesheet" href="app.css">', f'<style>{css}</style>')
        (DIST / page).write_text(html, encoding='utf-8')
    kb = sum(f.stat().st_size for f in DIST.rglob('*') if f.is_file()) // 1024
    print('dist listo,', kb, 'KB')


if __name__ == '__main__':
    main()
