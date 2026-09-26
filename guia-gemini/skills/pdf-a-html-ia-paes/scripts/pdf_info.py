"""Resumen de un PDF: páginas, si tiene texto o es escaneado, y marcadores.

Uso:  python pdf_info.py libro.pdf
"""
import sys

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from comun import abrir_pdf, imprimir_json


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    doc = abrir_pdf(sys.argv[1])
    n = doc.page_count
    muestras = sorted({p for p in (1, 2, 3, n // 4, n // 2, 3 * n // 4, n - 1) if 1 <= p <= n})
    con_texto = [p for p in muestras if len(doc[p - 1].get_text("text").strip()) > 80]
    marcadores = [
        {"nivel": nivel, "titulo": titulo.strip(), "pagina": pagina}
        for nivel, titulo, pagina, *_ in doc.get_toc(simple=False)
        if pagina >= 1
    ]
    r = doc[0].rect
    imprimir_json({
        "archivo": sys.argv[1],
        "paginas": n,
        "tipo": "con_texto" if len(con_texto) >= max(1, len(muestras) // 2) else
                ("mixto" if con_texto else "escaneado"),
        "paginas_muestra_con_texto": con_texto,
        "tamano_pagina_pt": [round(r.width), round(r.height)],
        "marcadores": marcadores[:300],
        "total_marcadores": len(marcadores),
        "titulo_metadatos": (doc.metadata or {}).get("title") or None,
    })


if __name__ == "__main__":
    main()
