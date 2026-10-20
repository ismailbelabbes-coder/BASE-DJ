"""Genera dist/informe.html: diagnóstico de rutas, colecciones y velocidad de basedj.es (datos medidos el 19/10/2026)."""
import csv, html, json, shutil
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

rows = list(csv.DictReader((ROOT / 'auditoria_migas.csv').open(encoding='utf-8-sig'), delimiter=';'))
aud = json.loads((ROOT / 'auditoria_colecciones.json').read_text(encoding='utf-8'))
mal = [r for r in rows if r['problemas'] != 'ok']
tipos = Counter(p for r in mal for p in r['problemas'].split('; '))
shutil.copy(ROOT / 'auditoria_migas.csv', DIST / 'colecciones_rutas.csv')

# Ejemplos claros: los de más productos primero
ej = sorted(mal, key=lambda r: -int(r['productos'] or 0))[:8]
e = html.escape

def fila(r):
    return (f'<tr><td><a href="{e(r["url"])}" target="_blank" rel="noopener">{e(r["coleccion"])}</a><span>{e(r["productos"])} productos</span></td>'
            f'<td>{e(r["ruta_actual"] or "(no se ve)")}</td><td>{e(r["problemas"])}</td></tr>')

VEL = [  # medido con Lighthouse 12.6 en móvil simulado, 19/10/2026
    ('Barra de cookies (app Avada)', '147 KB y unos 400 ms bloqueando el móvil. En nuestras dos pruebas (portada y una colección, sin cookies aceptadas) fue el elemento principal en aparecer; en otras pruebas puede serlo una imagen de producto.',
     'Probar el aviso de cookies propio de Shopify, comprobando que los rastreadores siguen bloqueados hasta que el cliente acepta. Te paso el informe de cada página con su elemento principal identificado.'),
    ('App de «avísame cuando haya stock» (notify-me)', '94 KB y unos 120 ms de bloqueo en todas las páginas.',
     'Revisar cómo se carga sin perder la lista de deseos ni los avisos de stock.'),
    ('Scripts del pago rápido de Shopify', 'Unos 350 KB de código del checkout en la portada y en las colecciones.',
     'Revisar qué los carga en cada página; no todos se pueden quitar y el pago no se toca.'),
    ('Fuentes de Google externas', 'Una conexión más a otro servidor antes de pintar el texto.',
     'Usar la misma fuente desde la biblioteca de fuentes de Shopify.'),
]

css = (ROOT / 'dist' / 'index.html').read_text(encoding='utf-8')
style = css[css.index('<style>') + 7:css.index('</style>')]  # mismo diseño que la propuesta

page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Informe para BaseDJ | Rutas y velocidad</title><meta name="robots" content="noindex"><meta name="theme-color" content="#121013">
<meta property="og:title" content="Informe para BaseDJ: rutas y velocidad en el móvil"><meta property="og:image" content="https://propuesta-basedj.pages.dev/img/og.jpg">
<link rel="icon" href="img/logo.webp"><style>{style}
.rep {{ max-width: 1040px; margin: 0 auto; padding: 32px 16px 80px; }}
.rep h2 {{ font-family: "Playfair Display", Georgia, serif; font-weight: 700; font-size: clamp(1.8rem, 4vw, 2.6rem); line-height: 1.1; margin: 64px 0 16px; }}
.rep p, .rep li {{ color: #A9A1A8; font-size: 16px; line-height: 1.6; }}
.rep b {{ color: #F3EEE6; }}
.kpis {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-top: 28px; }}
.kpi {{ border: 1px solid rgba(255,255,255,.09); border-radius: 6px; padding: 20px; background: rgba(27,23,28,.7); }}
.kpi .n {{ font-family: "Playfair Display", Georgia, serif; font-style: italic; font-size: 44px; color: #F2E205; line-height: 1; }}
.kpi .l {{ margin-top: 8px; color: #F3EEE6; font-weight: 700; }}
.kpi .s {{ margin-top: 4px; font-size: 14px; color: #A9A1A8; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 18px; font-size: 14px; }}
th, td {{ text-align: left; padding: 12px 10px; border-top: 1px solid rgba(255,255,255,.08); vertical-align: top; }}
th {{ color: #A9A1A8; font-weight: 500; }}
td a {{ color: #F3EEE6; font-weight: 700; text-decoration: none; display: block; }} td span {{ color: #A9A1A8; font-size: 13px; }}
.wrap {{ overflow-x: auto; }}
.cause {{ border-left: 2px solid #F2E205; padding: 4px 0 4px 16px; margin: 18px 0; }}
.cause b {{ display: block; font-size: 17px; }}
.fix {{ color: #F3EEE6 !important; }}
.steps li {{ margin: 8px 0; }}
.cta {{ margin-top: 48px; display: inline-flex; gap: 10px; align-items: center; background: #F2E205; color: #121013; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; font-size: 12px; padding: 16px 26px; border-radius: 6px; text-decoration: none; }}
.dl {{ color: #F2E205; font-weight: 700; }}
</style></head><body class="text-cream antialiased">
<div class="rep">
  <img src="img/logo-t.webp" alt="BaseDJ" width="360" height="184" style="height:44px;width:auto">
  <h1 style="font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:600;font-size:clamp(2.4rem,6vw,4.2rem);line-height:1.05;margin-top:28px">Rutas y velocidad de tu tienda</h1>
  <p style="margin-top:14px">Revisión de basedj.es hecha el 19 de octubre de 2026, sin tocar nada de tu tienda. Preparado por Ismail Belabbes.</p>

  <div class="kpis">
    <div class="kpi"><div class="n">{len(mal)}</div><div class="l">de {len(rows)} colecciones</div><div class="s">tienen la ruta (miga de pan) mal o incompleta</div></div>
    <div class="kpi"><div class="n">8-10 s</div><div class="l">en mostrarse en el móvil</div><div class="s">portada 27-57/100 y colecciones ~43/100</div></div>
    <div class="kpi"><div class="n">1</div><div class="l">arreglo para todas las rutas</div><div class="s">se corrige en el tema, no colección por colección</div></div>
  </div>

  <h2>1. La miga de pan</h2>
  <p>He recorrido tus {len(rows)} colecciones una a una. Estos son los fallos que se repiten:</p>
  <ul>{''.join(f'<li><b>{e(k)}</b>: {v} colecciones</li>' for k, v in tipos.most_common())}</ul>
  <div class="wrap"><table><tr><th>Colección</th><th>Ruta que se ve ahora</th><th>Problema</th></tr>{''.join(fila(r) for r in ej)}</table></div>
  <p style="margin-top:14px"><a class="dl" href="colecciones_rutas.csv" download>Descargar la lista completa (Excel)</a></p>
  <p class="cause"><b>Por qué pasa</b>En casi todas la ruta no termina en la colección en la que estás (eso puede ser una opción del tema, pero tú quieres la ruta completa) y en 22 se repiten niveles porque el menú tiene nombres iguales. Corregirlas una a una con la IA tapa el síntoma, pero la siguiente colección vuelve a salir mal.</p>
  <p class="cause fix"><b>Cómo lo arreglo</b>Un solo bloque en el tema que construye la ruta desde tu menú, termina siempre en la página actual y quita los niveles repetidos. Además añade los datos que Google usa para mostrar la ruta en los resultados de búsqueda. Ya lo tengo escrito y validado con la herramienta oficial de Shopify.</p>
  <p class="cause fix"><b>Y los más de 3 niveles de PrestaShop</b>El menú de Shopify solo admite 3 niveles, por eso tus subcategorías más profundas (como las de altavoces) se quedaron sin ruta al migrar. Cada colección puede indicar cuál es su colección «padre» con un campo propio de Shopify, y la ruta sube por esa cadena hasta el inicio, tenga los niveles que tenga. Así recuperas tu árbol de categorías sin depender del menú.</p>

  <h2>2. Velocidad en el móvil</h2>
  <p>Medido con Lighthouse (la herramienta de Google) en un móvil simulado. Lo que más frena tu web:</p>
  {''.join(f'<div class="cause"><b>{e(t)}</b>{e(d)}<br><span class="fix">{e(s)}</span></div>' for t, d, s in VEL)}

  <h2>3. Otros detalles de las colecciones</h2>
  <ul>
    <li><b>{len(aud["vacias"])} colecciones vacías</b>, sin productos: conviene ocultarlas o rellenarlas.</li>
    <li><b>Títulos con erratas</b>: {e(", ".join(aud["titulos_raros"]))}.</li>
    <li><b>{aud["urls_largas"]} direcciones larguísimas</b> heredadas de la migración. No las tocaría sin redirecciones, para no perder posiciones en Google.</li>
  </ul>

  <h2>Cómo trabajaría</h2>
  <ol class="steps">
    <li><b>Sobre una copia de tu tema.</b> La tienda publicada sigue igual mientras trabajo.</li>
    <li><b>Sin tocar productos, stock, precios ni enlaces.</b></li>
    <li><b>Mido antes y después</b> con la misma herramienta, para que veas la diferencia con números.</li>
    <li><b>Publicas tú</b> cuando lo hayas revisado y te convenza.</li>
  </ol>
  <a class="cta" href="#whatsapp" data-wa="Hola Ismail, he visto el informe de BaseDJ.">Hablamos por WhatsApp</a>
</div>
<script>document.querySelectorAll('[data-wa]').forEach(a=>{{a.href='https://wa.me/34672572546?text='+encodeURIComponent(a.dataset.wa);a.target='_blank';a.rel='noopener'}});</script>
</body></html>'''
(DIST / 'informe.html').write_text(page, encoding='utf-8')
print('informe listo:', len(mal), 'de', len(rows), dict(tipos))
