"""Utilidades compartidas por los scripts de la skill pdf-a-html."""
import json
import re
import sys
import unicodedata

try:
    import pymupdf  # PyMuPDF >= 1.24
except ImportError:  # pragma: no cover
    try:
        import fitz as pymupdf  # versiones antiguas
    except ImportError:
        pymupdf = None


def abrir_pdf(ruta):
    if pymupdf is None:
        sys.exit("Falta PyMuPDF. Instálalo con:  pip install pymupdf")
    return pymupdf.open(ruta)


def rango_paginas(texto, total):
    """'3-5,8' -> [3, 4, 5, 8] (numeración desde 1, recortado a [1, total])."""
    paginas = set()
    for parte in re.split(r"[,;\s]+", str(texto or "").strip()):
        if not parte:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", parte)
        if m:
            paginas.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif parte.isdigit():
            paginas.add(int(parte))
    return sorted(p for p in paginas if 1 <= p <= total)


def slug(texto, maximo=60):
    t = unicodedata.normalize("NFD", str(texto or "")).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:maximo].rstrip("-")
    return t or "seccion"


def imprimir_json(obj):
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def renderizar(pagina, lado_max=1600):
    """Devuelve un Pixmap de la página con su lado mayor = lado_max píxeles."""
    r = pagina.rect
    escala = lado_max / max(r.width, r.height)
    return pagina.get_pixmap(matrix=pymupdf.Matrix(escala, escala), alpha=False)


# ------------------------------------------------------------------ figuras ---

def _gris(pagina, lado=1000):
    """Página en escala de grises: (bytes, ancho, alto, stride)."""
    r = pagina.rect
    escala = lado / max(r.width, r.height)
    pix = pagina.get_pixmap(matrix=pymupdf.Matrix(escala, escala), colorspace=pymupdf.csGRAY, alpha=False)
    return pix.samples, pix.width, pix.height, pix.stride


def _tiene_tinta(buf, stride, valores_idx):
    """True si la línea de píxeles tiene contenido (no es un color uniforme)."""
    vals = [buf[i] for i in valores_idx]
    if len(vals) < 4:
        return False
    muestra = sorted(vals[:: max(1, len(vals) // 200)])
    fondo = muestra[len(muestra) // 2]
    distintos = sum(1 for v in vals if abs(v - fondo) > 38)
    return distintos > max(3, 0.012 * len(vals))


def ajustar_caja(pagina, caja, margen=0.012, max_crecer=0.035):
    """Corrige un recorte normalizado 0-1000 (x0,y0,x1,y1):
    - lo agranda por cada lado cuyo borde corta contenido (hasta max_crecer de la página),
    - lo encoge quitando franjas uniformes (márgenes vacíos),
    - y deja un margen pequeño. Devuelve (caja_nueva, cambio_relevante)."""
    buf, w, h, st = _gris(pagina)
    x0, y0, x1, y1 = [max(0.0, min(1000.0, float(v))) for v in caja]
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    X0, X1 = int(x0 * (w - 1) / 1000), int(x1 * (w - 1) / 1000)
    Y0, Y1 = int(y0 * (h - 1) / 1000), int(y1 * (h - 1) / 1000)
    orig = (X0, Y0, X1, Y1)

    fila = lambda y, a, b: [y * st + x for x in range(a, b + 1)]
    col = lambda x, a, b: [y * st + x for y in range(a, b + 1)]
    paso_x, paso_y = max(2, w // 120), max(2, h // 120)
    lim_x, lim_y = int(w * max_crecer), int(h * max_crecer)

    # Un borde "corta" la figura solo si hay contenido continuo hacia adentro. Si justo por
    # dentro hay una franja vacía, lo que toca el borde es otro elemento (pie «Figura N»,
    # párrafo vecino) y no se debe crecer hacia él.
    bx, by = max(2, int(w * 0.012)), max(2, int(h * 0.012))

    def corta(lado):
        if lado == "izq":
            return _tiene_tinta(buf, st, col(X0, Y0, Y1)) and all(_tiene_tinta(buf, st, col(x, Y0, Y1)) for x in range(X0 + 1, min(X1, X0 + bx)))
        if lado == "der":
            return _tiene_tinta(buf, st, col(X1, Y0, Y1)) and all(_tiene_tinta(buf, st, col(x, Y0, Y1)) for x in range(max(X0, X1 - bx), X1))
        if lado == "arr":
            return _tiene_tinta(buf, st, fila(Y0, X0, X1)) and all(_tiene_tinta(buf, st, fila(y, X0, X1)) for y in range(Y0 + 1, min(Y1, Y0 + by)))
        return _tiene_tinta(buf, st, fila(Y1, X0, X1)) and all(_tiene_tinta(buf, st, fila(y, X0, X1)) for y in range(max(Y0, Y1 - by), Y1))

    crecer = {lado: corta(lado) for lado in ("izq", "der", "arr", "aba")}

    # 1) Crecer mientras el borde atraviese contenido.
    for _ in range(40):
        movido = False
        if crecer["izq"] and X0 > 0 and orig[0] - X0 < lim_x and _tiene_tinta(buf, st, col(X0, Y0, Y1)):
            X0 = max(0, X0 - paso_x); movido = True
        if crecer["der"] and X1 < w - 1 and X1 - orig[2] < lim_x and _tiene_tinta(buf, st, col(X1, Y0, Y1)):
            X1 = min(w - 1, X1 + paso_x); movido = True
        if crecer["arr"] and Y0 > 0 and orig[1] - Y0 < lim_y and _tiene_tinta(buf, st, fila(Y0, X0, X1)):
            Y0 = max(0, Y0 - paso_y); movido = True
        if crecer["aba"] and Y1 < h - 1 and Y1 - orig[3] < lim_y and _tiene_tinta(buf, st, fila(Y1, X0, X1)):
            Y1 = min(h - 1, Y1 + paso_y); movido = True
        if not movido:
            break

    # 2) Encoger quitando franjas vacías.
    while X1 - X0 > 20 and not _tiene_tinta(buf, st, col(X0, Y0, Y1)):
        X0 += 1
    while X1 - X0 > 20 and not _tiene_tinta(buf, st, col(X1, Y0, Y1)):
        X1 -= 1
    while Y1 - Y0 > 20 and not _tiene_tinta(buf, st, fila(Y0, X0, X1)):
        Y0 += 1
    while Y1 - Y0 > 20 and not _tiene_tinta(buf, st, fila(Y1, X0, X1)):
        Y1 -= 1

    # 3) Margen, pero sin llegar a tocar otro contenido (pies de figura pegados, texto vecino).
    mx, my = int(w * margen), int(h * margen)
    for _ in range(mx):
        if X0 > 0 and not _tiene_tinta(buf, st, col(X0 - 1, Y0, Y1)):
            X0 -= 1
        if X1 < w - 1 and not _tiene_tinta(buf, st, col(X1 + 1, Y0, Y1)):
            X1 += 1
    for _ in range(my):
        if Y0 > 0 and not _tiene_tinta(buf, st, fila(Y0 - 1, X0, X1)):
            Y0 -= 1
        if Y1 < h - 1 and not _tiene_tinta(buf, st, fila(Y1 + 1, X0, X1)):
            Y1 += 1
    # Si el margen se detuvo por tocar otro elemento, retroceder 2 px para que no asome
    # ni un borde del pie de figura (al recortar en alta resolución se notaría).
    if Y1 < h - 1 and _tiene_tinta(buf, st, fila(Y1 + 1, X0, X1)):
        Y1 = max(Y0 + 10, Y1 - 2)
    if Y0 > 0 and _tiene_tinta(buf, st, fila(Y0 - 1, X0, X1)):
        Y0 = min(Y1 - 10, Y0 + 2)
    if X1 < w - 1 and _tiene_tinta(buf, st, col(X1 + 1, Y0, Y1)):
        X1 = max(X0 + 10, X1 - 2)
    if X0 > 0 and _tiene_tinta(buf, st, col(X0 - 1, Y0, Y1)):
        X0 = min(X1 - 10, X0 + 2)
    nueva = [round(X0 * 1000 / (w - 1)), round(Y0 * 1000 / (h - 1)), round(X1 * 1000 / (w - 1)), round(Y1 * 1000 / (h - 1))]
    cambio = max(abs(a - b) for a, b in zip(nueva, [x0, y0, x1, y1])) > 15
    return nueva, cambio


def recortar_png(pagina, caja, lado=2200):
    """Pixmap del rectángulo normalizado 0-1000 de la página."""
    r = pagina.rect
    x0, y0, x1, y1 = [v / 1000 for v in caja]
    clip = pymupdf.Rect(r.width * x0, r.height * y0, r.width * x1, r.height * y1)
    escala = lado / max(r.width, r.height)
    return pagina.get_pixmap(matrix=pymupdf.Matrix(escala, escala), clip=clip, alpha=False)


def figuras_en_fragmentos(textos):
    """[(pagina, caja, leyenda)] de todas las <figure data-pagina data-recorte> de los fragmentos."""
    out = []
    for texto in textos:
        for m in re.finditer(r"(?is)<figure\b([^>]*)>(.*?)</figure>", texto):
            pag = re.search(r'data-pagina\s*=\s*"(\d+)"', m.group(1))
            caja = re.search(r'data-recorte\s*=\s*"([^"]+)"', m.group(1))
            if not (pag and caja):
                continue
            try:
                nums = [float(x) for x in caja.group(1).split(",")]
            except ValueError:
                continue
            if len(nums) == 4:
                leyenda = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip()
                out.append((int(pag.group(1)), nums, leyenda))
    return out


def figuras_detectadas(pagina):
    """Figuras que el propio PDF declara (imágenes incrustadas y dibujos vectoriales),
    en coordenadas 0-1000. En PDFs escaneados devuelve [] (la página entera es una imagen)."""
    r = pagina.rect
    area_pag = r.width * r.height
    cajas = []
    try:
        for info in pagina.get_image_info():
            b = pymupdf.Rect(info["bbox"]) & r
            if b.is_empty or b.get_area() > 0.8 * area_pag or b.get_area() < 0.004 * area_pag:
                continue
            cajas.append(("imagen", b))
    except Exception:
        pass
    try:
        for b in pagina.cluster_drawings():
            b = pymupdf.Rect(b) & r
            if not b.is_empty and 0.015 * area_pag < b.get_area() < 0.8 * area_pag:
                cajas.append(("vectorial", b))
    except Exception:
        pass
    return [{"tipo": t, "recorte": [round(b.x0 * 1000 / r.width), round(b.y0 * 1000 / r.height),
                                     round(b.x1 * 1000 / r.width), round(b.y1 * 1000 / r.height)]}
            for t, b in cajas]
