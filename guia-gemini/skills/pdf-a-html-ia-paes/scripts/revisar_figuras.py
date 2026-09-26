"""Revisión visual de figuras: comprueba que se extrajeron TODAS y que están bien recortadas.

Uso:
  python revisar_figuras.py libro.pdf --fragmentos fragmentos --secciones secciones.json \
      --seccion 1 [--salida revision] [--sin-ajuste]

Genera en la carpeta de salida:
  paginas_NNNN-MMMM.png  4 páginas por hoja, con cada recorte dibujado encima (rectángulo
                         numerado). Sirve para ver figuras SIN marcar o mal ubicadas.
  recortes_NN.png        todos los recortes tal como quedarán en el HTML (ya ajustados),
                         numerados igual. Sirve para ver figuras cortadas o con texto de más.
Imprime un JSON con, por página: figuras marcadas, figuras que el PDF declara y no están
marcadas (solo PDFs con texto) y recortes que el ajuste automático movió.
"""
import argparse
import glob
import json
import os
import sys as _sys

_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import (abrir_pdf, ajustar_caja, figuras_detectadas, figuras_en_fragmentos,  # noqa: E402
                   imprimir_json, pymupdf, recortar_png, renderizar)

COLORES = [(0.86, 0.15, 0.15), (0.1, 0.45, 0.9), (0.1, 0.6, 0.25), (0.85, 0.45, 0.0), (0.55, 0.2, 0.75)]


def se_solapan(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area_b = max(1, (b[2] - b[0]) * (b[3] - b[1]))
    return ix * iy / area_b > 0.3


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--fragmentos", required=True)
    ap.add_argument("--secciones", required=True)
    ap.add_argument("--seccion", type=int, required=True, help="número de sección (1, 2, …)")
    ap.add_argument("--salida", default="revision")
    ap.add_argument("--sin-ajuste", action="store_true")
    a = ap.parse_args()

    with open(a.secciones, encoding="utf-8") as f:
        conf = json.load(f)
    secs = conf["secciones"] if isinstance(conf, dict) else conf
    sec = secs[a.seccion - 1]
    archivos = sorted(glob.glob(os.path.join(a.fragmentos, f"{a.seccion:02d}-*.html")) +
                      glob.glob(os.path.join(a.fragmentos, f"{a.seccion:02d}.html")))
    textos = [open(r, encoding="utf-8").read() for r in archivos]
    figs = figuras_en_fragmentos(textos)
    doc = abrir_pdf(a.pdf)
    os.makedirs(a.salida, exist_ok=True)
    for viejo in glob.glob(os.path.join(a.salida, "*.png")):
        os.remove(viejo)

    # Numerar y ajustar
    lista = []
    for n, (p, caja, leyenda) in enumerate(figs, start=1):
        final, movida = (caja, False) if a.sin_ajuste else ajustar_caja(doc[p - 1], caja)
        lista.append({"n": n, "pagina": p, "caja": caja, "final": final, "movida": movida, "leyenda": leyenda[:90]})

    paginas = list(range(sec["desde"], sec["hasta"] + 1))
    informe = []
    # Hojas de páginas (2 x 2)
    ancho_pag = 620
    for i in range(0, len(paginas), 4):
        grupo = paginas[i:i + 4]
        pixs = [renderizar(doc[p - 1], 900) for p in grupo]
        alto_pag = max(int(px.height * ancho_pag / px.width) for px in pixs)
        hoja = pymupdf.open()
        pg = hoja.new_page(width=ancho_pag * 2 + 30, height=(alto_pag + 34) * 2 + 10)
        for k, (p, px) in enumerate(zip(grupo, pixs)):
            ox, oy = 10 + (k % 2) * (ancho_pag + 10), 10 + (k // 2) * (alto_pag + 34)
            h = px.height * ancho_pag / px.width
            pg.insert_image(pymupdf.Rect(ox, oy + 24, ox + ancho_pag, oy + 24 + h), pixmap=px)
            marcadas = [f for f in lista if f["pagina"] == p]
            detectadas = [d["recorte"] for d in figuras_detectadas(doc[p - 1])]
            sin_marcar = [d for d in detectadas if not any(se_solapan(f["final"], d) for f in marcadas)]
            pg.insert_text((ox, oy + 16), f"PAGINA {p}  -  {len(marcadas)} figura(s) marcada(s)"
                           + (f"  -  {len(sin_marcar)} SIN MARCAR" if sin_marcar else ""), fontsize=13,
                           color=(0.8, 0.1, 0.1) if sin_marcar else (0.1, 0.1, 0.1))
            for f in marcadas:
                c = COLORES[f["n"] % len(COLORES)]
                x0, y0, x1, y1 = f["final"]
                rr = pymupdf.Rect(ox + x0 * ancho_pag / 1000, oy + 24 + y0 * h / 1000,
                                  ox + x1 * ancho_pag / 1000, oy + 24 + y1 * h / 1000)
                pg.draw_rect(rr, color=c, width=2.5)
                pg.draw_rect(pymupdf.Rect(rr.x0, rr.y0, rr.x0 + 26, rr.y0 + 18), color=c, fill=c)
                pg.insert_text((rr.x0 + 3, rr.y0 + 14), str(f["n"]), fontsize=13, color=(1, 1, 1))
            for d in sin_marcar:
                x0, y0, x1, y1 = d
                pg.draw_rect(pymupdf.Rect(ox + x0 * ancho_pag / 1000, oy + 24 + y0 * h / 1000,
                                          ox + x1 * ancho_pag / 1000, oy + 24 + y1 * h / 1000),
                             color=(0.9, 0.1, 0.1), width=2, dashes="[6 4] 0")
            informe.append({"pagina": p, "figuras": [f["n"] for f in marcadas], "detectadas_sin_marcar": sin_marcar})
        ruta = os.path.join(a.salida, f"paginas_{grupo[0]:04d}-{grupo[-1]:04d}.png")
        pg.get_pixmap(alpha=False).save(ruta)

    # Hojas de recortes (12 por hoja)
    for i in range(0, len(lista), 12):
        grupo = lista[i:i + 12]
        cw, ch, cols = 400, 300, 3
        filas = (len(grupo) + cols - 1) // cols
        hoja = pymupdf.open()
        pg = hoja.new_page(width=cw * cols + 20, height=filas * (ch + 30) + 10)
        for k, f in enumerate(grupo):
            ox, oy = 10 + (k % cols) * cw, 10 + (k // cols) * (ch + 30)
            px = recortar_png(doc[f["pagina"] - 1], f["final"], 1400)
            esc = min((cw - 12) / px.width, (ch - 6) / px.height)
            pg.insert_image(pymupdf.Rect(ox, oy + 22, ox + px.width * esc, oy + 22 + px.height * esc), pixmap=px)
            pg.draw_rect(pymupdf.Rect(ox, oy + 22, ox + px.width * esc, oy + 22 + px.height * esc), color=(0.6, 0.6, 0.6), width=0.8)
            pg.insert_text((ox, oy + 15), f"#{f['n']}  p.{f['pagina']}" + ("  (ajustado)" if f["movida"] else ""),
                           fontsize=12, color=(0.1, 0.1, 0.1))
        pg.get_pixmap(alpha=False).save(os.path.join(a.salida, f"recortes_{i // 12 + 1:02d}.png"))

    imprimir_json({
        "seccion": a.seccion,
        "figuras_marcadas": len(lista),
        "hojas": sorted(os.path.relpath(r) for r in glob.glob(os.path.join(a.salida, "*.png"))),
        "ajustadas_automaticamente": [{"n": f["n"], "pagina": f["pagina"], "antes": f["caja"], "despues": f["final"]}
                                      for f in lista if f["movida"]],
        "paginas_con_figuras_pdf_sin_marcar": [x for x in informe if x["detectadas_sin_marcar"]],
        "instrucciones": "Mira cada hoja paginas_*.png: toda foto, dibujo, gráfico, esquema o mapa debe tener un "
                         "rectángulo numerado que lo contenga completo (sin cortar y sin el pie «Figura N»). "
                         "Luego mira recortes_*.png: ninguna figura debe verse cortada ni con texto de párrafos. "
                         "Corrige data-recorte en los fragmentos y vuelve a ejecutar hasta que todo esté bien.",
    })


if __name__ == "__main__":
    main()
