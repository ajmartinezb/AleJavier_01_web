"""Utilidades base para dibujar diagramas SVG del libro (textos, líneas, flechas y el archivo final).

Uso: cambia OUT por la carpeta img/ del capítulo, define una función por figura que arme una lista
de elementos con t(), ln(), flecha() y llame a svg(nombre, ancho, alto, texto_alt, cuerpo).
Ver ejemplo-figuras-cap13.py."""
import math
import os

OUT = "fisica/capitulos/capNN-slug/img"  # cambia a la carpeta img/ del capítulo
FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
AZ, RO, GR, NE, VE, NA, AM = "#1c7ed6", "#c92a2a", "#4a5568", "#1a202c", "#2f9e44", "#e67700", "#f59f00"


def svg(nombre, w, h, alt, cuerpo, fondo="#ffffff"):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
         f'aria-label="{alt}" font-family="{FONT}">\n<title>{alt}</title>\n'
         f'<rect width="{w}" height="{h}" fill="{fondo}"/>\n<defs>'
         + "".join(f'<marker id="m{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                   for n, c in (("g", GR), ("r", RO), ("a", AZ), ("n", NA), ("v", VE)))
         + '</defs>\n' + cuerpo + '\n</svg>\n')
    open(os.path.join(OUT, nombre), "w", encoding="utf-8").write(s)


def t(x, y, txt, size=13, color=NE, anchor="middle", weight="normal", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
            f'font-weight="{weight}"{st}>{txt}</text>')


def ln(x1, y1, x2, y2, color=GR, w=1.5, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" {extra}/>'


def flecha(x1, y1, x2, y2, color=RO, w=2.2, m="r", extra=""):
    """Línea con punta de flecha a mitad de camino (para rayos)."""
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
    return (ln(x1, y1, x2, y2, color, w, extra) +
            ln(x1, y1, xm, ym, color, w, f'marker-end="url(#m{m})" {extra}'))


PUNT = 'stroke-dasharray="5 4"'
