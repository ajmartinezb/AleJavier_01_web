"""Convierte páginas del PDF en imágenes (para leerlas con visión) y extrae su texto si lo tienen.

Uso:
  python renderizar_paginas.py libro.pdf --paginas 17-19 [--salida paginas] [--lado 1600] [--texto]

Crea paginas/p0017.png ... y, con --texto, paginas/p0017.txt con la capa de texto del PDF
(vacío en PDFs escaneados). Imprime un JSON con las rutas generadas y, en PDFs con texto,
"figuras_detectadas": las coordenadas exactas de las imágenes y dibujos de cada página.
"""
import argparse
import os

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from comun import abrir_pdf, figuras_detectadas, imprimir_json, rango_paginas, renderizar


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--paginas", required=True, help="ej. 5-8 o 3,7,10-12 (numeración del PDF, desde 1)")
    ap.add_argument("--salida", default="paginas")
    ap.add_argument("--lado", type=int, default=1600, help="píxeles del lado mayor (1400-2000 recomendado)")
    ap.add_argument("--texto", action="store_true", help="guardar también la capa de texto")
    a = ap.parse_args()

    doc = abrir_pdf(a.pdf)
    paginas = rango_paginas(a.paginas, doc.page_count)
    os.makedirs(a.salida, exist_ok=True)
    salida = []
    for p in paginas:
        pag = doc[p - 1]
        img = os.path.join(a.salida, f"p{p:04d}.png")
        renderizar(pag, a.lado).save(img)
        item = {"pagina": p, "imagen": img}
        detectadas = figuras_detectadas(pag)
        if detectadas:
            # Coordenadas exactas (0-1000) de imágenes/dibujos que trae el PDF: úsalas en data-recorte.
            item["figuras_detectadas"] = detectadas
        if a.texto:
            txt = os.path.join(a.salida, f"p{p:04d}.txt")
            texto = pag.get_text("text")
            with open(txt, "w", encoding="utf-8") as f:
                f.write(texto)
            item["texto"] = txt
            item["caracteres_texto"] = len(texto.strip())
        salida.append(item)
    imprimir_json({"paginas": salida})


if __name__ == "__main__":
    main()
