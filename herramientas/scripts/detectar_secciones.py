"""Busca dónde empieza cada capítulo / unidad / tema de un PDF.

Uso:
  python detectar_secciones.py libro.pdf --tipo capitulo [--desde 1 --hasta 400] [--hojas carpeta]

Orden de métodos:
  1. Marcadores (bookmarks) del PDF.
  2. Texto de la parte superior de cada página («Capítulo 3», «Unidad II», encabezados
     tipo «Método Científico | Capítulo 1»).
  3. Si el PDF es escaneado (sin texto), genera «hojas de encabezados»: imágenes PNG con la
     franja superior de 12 páginas cada una, rotuladas con su número de página del PDF,
     para que el modelo las mire y encuentre los inicios a simple vista.

Salida: JSON con {"metodo", "secciones": [{"titulo", "desde", "hasta"}], "hojas_encabezados": [...]}.
"""
import argparse
import os
import re

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from comun import abrir_pdf, imprimir_json, pymupdf

PALABRAS = {
    "capitulo": r"cap[ií]tulo",
    "unidad": r"unidad",
    "tema": r"(?:tema|lecci[oó]n|m[oó]dulo)",
    "parte": r"parte",
}


def romano_a_num(s):
    if s.isdigit():
        return int(s)
    val = {"i": 1, "v": 5, "x": 10, "l": 50}
    s, total = s.lower(), 0
    for i, c in enumerate(s):
        a, b = val[c], val.get(s[i + 1], 0) if i + 1 < len(s) else 0
        total += -a if a < b else a
    return total


def titulo_desde_linea(linea, m, patron, siguiente):
    etiqueta = re.sub(r"\s+", " ", m.group(0)).strip()
    etiqueta = etiqueta[0].upper() + etiqueta[1:]
    otras = [x.strip() for x in re.split(r"\s*[|•·]\s*", linea) if x.strip() and not patron.search(x) and len(x.strip()) > 2]
    if otras:
        return f"{etiqueta}: {' '.join(otras)}"
    resto = re.sub(r"^[\s:.\-–—]+", "", linea[m.end():])
    if len(resto) > 2:
        return f"{etiqueta}: {resto}"
    if siguiente and len(siguiente) < 90:
        return f"{etiqueta}: {siguiente}"
    return etiqueta


def completar_hastas(secciones, total):
    secciones.sort(key=lambda s: s["desde"])
    for i, s in enumerate(secciones):
        s["hasta"] = max(s["desde"], secciones[i + 1]["desde"] - 1) if i + 1 < len(secciones) else total
    return secciones


def hojas_encabezados(doc, desde, hasta, carpeta, por_hoja=12, fraccion=0.16):
    os.makedirs(carpeta, exist_ok=True)
    ancho, rotulo = 1000, 26
    rutas = []
    paginas = list(range(desde, hasta + 1))
    for inicio in range(0, len(paginas), por_hoja):
        grupo = paginas[inicio:inicio + por_hoja]
        tiras = []
        for p in grupo:
            pag = doc[p - 1]
            r = pag.rect
            escala = 1400 / max(r.width, r.height)
            tira = pag.get_pixmap(matrix=pymupdf.Matrix(escala, escala), alpha=False,
                                  clip=pymupdf.Rect(0, 0, r.width, r.height * fraccion))
            tiras.append((p, tira))
        alto_total = sum(rotulo + int(t.height * ancho / t.width) + 6 for _, t in tiras)
        hoja = pymupdf.open()
        pag = hoja.new_page(width=ancho, height=alto_total)
        y = 0
        for p, tira in tiras:
            pag.draw_rect(pymupdf.Rect(0, y, ancho, y + rotulo), color=None, fill=(0.15, 0.3, 0.7))
            pag.insert_text((8, y + 18), f"PAGINA DEL PDF {p}", fontsize=15, color=(1, 1, 1))
            y += rotulo
            h = int(tira.height * ancho / tira.width)
            pag.insert_image(pymupdf.Rect(0, y, ancho, y + h), pixmap=tira)
            y += h + 6
        ruta = os.path.join(carpeta, f"encabezados_{grupo[0]:04d}-{grupo[-1]:04d}.png")
        pag.get_pixmap(alpha=False).save(ruta)
        rutas.append(ruta)
    return rutas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--tipo", default="capitulo", choices=list(PALABRAS))
    ap.add_argument("--desde", type=int, default=1)
    ap.add_argument("--hasta", type=int, default=0)
    ap.add_argument("--hojas", default="hojas_encabezados", help="carpeta para las hojas (PDF escaneado)")
    ap.add_argument("--forzar-hojas", action="store_true", help="generar hojas aunque haya texto")
    a = ap.parse_args()

    doc = abrir_pdf(a.pdf)
    total = doc.page_count
    desde, hasta = max(1, a.desde), min(total, a.hasta or total)
    patron = re.compile(rf"\b{PALABRAS[a.tipo]}\s*[:.\-]?\s*(\d{{1,3}}|[ivxl]{{1,6}})\b", re.I)

    # 1) Marcadores
    toc = [(nivel, t.strip(), p) for nivel, t, p, *_ in doc.get_toc(simple=False) if p >= 1]
    if toc:
        filtrados = [x for x in toc if patron.search(x[1])]
        usar = filtrados if len(filtrados) >= 2 else [x for x in toc if x[0] == min(n for n, _, _ in toc)]
        if len(usar) >= 2:
            secs = completar_hastas([{"titulo": t, "desde": p} for _, t, p in usar], total)
            return imprimir_json({"metodo": "marcadores", "secciones": secs, "hojas_encabezados": []})

    # 2) Texto en la parte superior de cada página
    secs, vistos, paginas_con_texto = [], set(), 0
    for p in range(desde, hasta + 1):
        pag = doc[p - 1]
        r = pag.rect
        texto = pag.get_text("text", clip=pymupdf.Rect(0, 0, r.width, r.height * 0.45))
        if len(texto.strip()) > 20:
            paginas_con_texto += 1
        lineas = [l.strip() for l in texto.splitlines() if l.strip()]
        for i, linea in enumerate(lineas):
            m = patron.search(linea)
            if not m:
                continue
            num = romano_a_num(m.group(1))
            if num in vistos:
                break
            vistos.add(num)
            secs.append({"titulo": titulo_desde_linea(linea, m, patron, lineas[i + 1] if i + 1 < len(lineas) else ""), "desde": p})
            break

    escaneado = paginas_con_texto < (hasta - desde + 1) * 0.2
    hojas = []
    if escaneado or a.forzar_hojas or not secs:
        hojas = hojas_encabezados(doc, desde, hasta, a.hojas)

    imprimir_json({
        "metodo": "texto" if secs else "revisar_hojas",
        "pdf_escaneado": escaneado,
        "secciones": completar_hastas(secs, total) if secs else [],
        "hojas_encabezados": hojas,
        "nota": ("PDF escaneado: mira las hojas de encabezados (cada franja está rotulada con su página del PDF) "
                 "y anota dónde aparece por primera vez cada número de capítulo/unidad. "
                 "Alternativa: renderiza las páginas del índice y lee los números de página impresos.")
                if hojas else "",
    })


if __name__ == "__main__":
    main()
