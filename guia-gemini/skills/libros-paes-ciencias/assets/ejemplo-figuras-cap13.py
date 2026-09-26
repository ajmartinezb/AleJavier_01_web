"""Diagramas SVG del capítulo 13 de Física (la Tierra y el Universo)."""
import math
import os

base = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(base, "svg_base.py")).read())
OUT = "fisica/capitulos/cap13-tierra-universo/img"  # ejecutar desde la raíz del proyecto
SOL, TIE, MAR_, VEN = "#f59f00", "#1c7ed6", "#c92a2a", "#e67700"
PUNT2 = 'stroke-dasharray="3 4"'


def circ(cx, cy, r, fill="none", stroke=GR, w=1.5, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>'


def poly(pts, color=AZ, w=2.5, fill="none", extra=""):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{color}" stroke-width="{w}" {extra}/>'


def poligono(pts, color, op=0.3):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color}" opacity="{op}"/>'


def sol(cx, cy, r=16):
    return circ(cx, cy, r, SOL, "#e67700", 1.5)


def fase(cx, cy, r, k, rot=0):
    """Disco con fracción iluminada k (0 nueva, 1 llena); iluminado a la derecha, luego rotado."""
    base_ = circ(cx, cy, r, "#343a40", "#343a40", 1)
    if k <= 0.01:
        return base_
    if k >= 0.99:
        return circ(cx, cy, r, "#fff3bf", "#e67700", 1)
    rx = r * abs(1 - 2 * k)
    sw = 1 if k > 0.5 else 0
    d = (f"M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} "
         f"A{rx:.2f},{r} 0 0 {sw} {cx},{cy - r} z")
    return base_ + f'<path d="{d}" fill="#fff3bf" stroke="#e67700" stroke-width="0.8" transform="rotate({rot} {cx} {cy})"/>'


def ejes(c, ox, oy, W, H, xlab, ylab, xt, yt, sx, sy, fmt=lambda v: str(v).replace(".", ",")):
    c.append(ln(ox, oy, ox + W, oy, GR, 1.5, 'marker-end="url(#mg)"'))
    c.append(ln(ox, oy, ox, oy - H, GR, 1.5, 'marker-end="url(#mg)"'))
    c.append(t(ox + W, oy + 36, xlab, 12, GR, "end"))
    c.append(t(ox + 6, oy - H - 6, ylab, 12, GR, "start"))
    for v in xt:
        c.append(ln(ox + v * sx, oy - 4, ox + v * sx, oy + 4, GR, 1))
        c.append(t(ox + v * sx, oy + 18, fmt(v), 11, GR))
    for v in yt:
        if v == 0:
            continue
        c.append(ln(ox - 4, oy - v * sy, ox + 4, oy - v * sy, GR, 1))
        c.append(ln(ox + 4, oy - v * sy, ox + W - 10, oy - v * sy, "#edf2f7", 1))
        c.append(t(ox - 8, oy - v * sy + 4, fmt(v), 11, GR, "end"))
    return lambda x, y: (ox + x * sx, oy - y * sy)


def miles(v):
    s = f"{v:,}".replace(",", " ")
    return s


# 1. Movimiento retrógrado ------------------------------------------------------
def retrogrado():
    c = [t(450, 28, "El movimiento retrógrado de Marte visto desde la Tierra", 18, weight="700")]
    cx, cy = 240, 330
    rE, rM = 88, 134
    c.append(t(240, 62, "Vista desde arriba del sistema solar", 14, NE, weight="700"))
    c.append(circ(cx, cy, rE, "none", TIE, 1.5, PUNT2))
    c.append(circ(cx, cy, rM, "none", MAR_, 1.5, PUNT2))
    c.append(sol(cx, cy, 16))
    c.append(t(cx, cy + 34, "Sol", 12, NE, weight="700"))
    ts = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3]
    fis = []
    for i, tt in enumerate(ts, 1):
        aE = math.radians(90 + 360 * tt)
        aM = math.radians(90 + 360 * tt / 1.88)
        ex, ey = cx + rE * math.cos(aE), cy - rE * math.sin(aE)
        mx, my = cx + rM * math.cos(aM), cy - rM * math.sin(aM)
        L = math.hypot(mx - ex, my - ey)
        k = 150 / L
        c.append(ln(ex, ey, mx + (mx - ex) * k * 0.55, my + (my - ey) * k * 0.55, "#adb5bd", 1, PUNT2))
        c.append(circ(ex, ey, 6, TIE, "none"))
        c.append(circ(mx, my, 5, MAR_, "none"))
        c.append(t(cx + (rE - 20) * math.cos(aE), cy - (rE - 20) * math.sin(aE) + 4, str(i), 11, TIE, weight="700"))
        c.append(t(cx + (rM + 16) * math.cos(aM), cy - (rM + 16) * math.sin(aM) + 4, str(i), 11, MAR_, weight="700"))
        fis.append(math.degrees(math.atan2(-(my - ey), mx - ex)))
    c.append(t(cx, cy + rM + 22, "órbita de Marte", 12, MAR_))
    c.append(t(cx, cy + rE + 24, "órbita de la Tierra", 12, TIE))
    c.append(t(240, 540, "Líneas punteadas: dirección en que se ve Marte desde la Tierra.", 11, GR, italic=True))
    # Panel derecho: el cielo
    x0, y0 = 500, 140
    c.append(t(690, 62, "Cómo se ve en el cielo, noche a noche", 14, NE, weight="700"))
    c.append(f'<rect x="{x0}" y="{y0 - 60}" width="380" height="170" fill="#212529" rx="10"/>')
    for (x, y) in [(520, 95), (560, 210), (610, 90), (650, 200), (760, 100), (830, 215), (860, 120), (720, 225), (530, 170), (800, 160)]:
        c.append(circ(x, y, 1.6, "#dee2e6", "none"))
    dy = [-16, -14, 0, 26, 8, -2, -18]
    pts = [(690 - (f - 90) * 9, y0 + 10 + d) for f, d in zip(fis, dy)]
    c.append(poly(pts, "#ff8787", 2, extra='marker-end="url(#mr)"'))
    for i, (x, y) in enumerate(pts, 1):
        c.append(circ(x, y, 5, "#ff6b6b", "none"))
        c.append(t(x, y - 10 if i in (1, 2, 7) else y + 20, str(i), 12, "#ffc9c9", weight="700"))
    c.append(t(x0 + 10, y0 + 100, "estrellas lejanas (fondo)", 11, "#adb5bd", "start", italic=True))
    txt = [("1 → 3: Marte avanza entre las estrellas.", NE, "normal"),
           ("3 → 5: parece retroceder (movimiento retrógrado).", RO, "700"),
           ("5 → 7: vuelve a avanzar.", NE, "normal"),
           ("", NE, "normal"),
           ("La Tierra, en su órbita interior, es más rápida", NE, "normal"),
           ("y «adelanta» a Marte cerca de la posición 4", NE, "normal"),
           ("(oposición). Por eso, durante unas semanas,", NE, "normal"),
           ("Marte parece moverse hacia atrás. Marte", NE, "normal"),
           ("nunca retrocede de verdad.", NE, "700")]
    for i, (s_, col, w) in enumerate(txt):
        c.append(t(x0, 350 + 20 * i, s_, 13, col, "start", w))
    c.append(t(x0, 540, "Posiciones cada 36 días. Esquema sin escala.", 11, GR, "start", italic=True))
    svg("movimiento-retrogrado.svg", 900, 555,
        "A la izquierda, vista desde arriba del Sol y de las órbitas de la Tierra y de Marte, con siete posiciones numeradas de cada planeta y la línea de visión de la Tierra hacia Marte en cada una. A la derecha, las posiciones aparentes de Marte sobre el fondo de estrellas: avanza de 1 a 3, retrocede de 3 a 5 y vuelve a avanzar de 5 a 7, formando un lazo",
        "\n".join(c))


# 2. Eratóstenes ------------------------------------------------------------------
def eratostenes():
    c = [t(450, 28, "Cómo midió Eratóstenes la Tierra", 18, weight="700")]
    cx, cy, R = 520, 300, 190
    c.append(circ(cx, cy, R, "#e7f5ff", TIE, 2))
    ang = 22  # exagerado
    # Siena: punto a la izquierda (rayos horizontales desde la izquierda)
    sx, sy = cx - R, cy
    a = math.radians(180 - ang)
    ax_, ay_ = cx + R * math.cos(a), cy - R * math.sin(a)
    vx0, vy0 = cx + (R + 34) * math.cos(a), cy - (R + 34) * math.sin(a)
    for y in (cy - 150, vy0, cy - 40, cy):
        xe = cx - math.sqrt(R * R - (y - cy) ** 2)
        c.append(flecha(40, y, xe, y, SOL, 2, "n"))
    c.append(t(40, cy - 170, "rayos del Sol (paralelos)", 12, "#e67700", "start", "700"))
    # Siena: pozo vertical
    c.append(ln(sx, sy, cx, cy, GR, 1.5, PUNT))
    c.append(ln(ax_, ay_, cx, cy, GR, 1.5, PUNT))
    c.append(ln(sx - 26, sy, sx, sy, NE, 4))
    c.append(t(sx - 30, sy + 26, "Siena", 13, NE, "end", "700"))
    c.append(t(sx - 30, sy + 44, "el Sol está en el cénit:", 11, GR, "end"))
    c.append(t(sx - 30, sy + 58, "no hay sombra", 11, GR, "end"))
    # varilla en Alejandría, prolongación de radio
    vx, vy = cx + (R + 34) * math.cos(a), cy - (R + 34) * math.sin(a)
    c.append(ln(ax_, ay_, vx, vy, NE, 4))
    xs_ = cx - math.sqrt(R * R - (vy - cy) ** 2)
    c.append(f'<path d="M{ax_:.1f},{ay_:.1f} A{R},{R} 0 0 1 {xs_:.1f},{vy:.1f}" fill="none" stroke="#495057" stroke-width="5"/>')
    c.append(t(vx - 10, vy - 12, "Alejandría", 13, NE, "end", "700"))
    c.append(t(vx - 10, vy + 4, "la varilla da sombra", 11, GR, "end"))
    # ángulo en Alejandría
    c.append(t(vx + 14, vy - 8, "7,2°", 13, RO, "start", "700"))
    c.append(t(xs_ + 8, vy + 18, "sombra", 11, GR, "start"))
    # ángulo en el centro
    r0 = 55
    p1 = (cx - r0, cy)
    p2 = (cx + r0 * math.cos(a), cy - r0 * math.sin(a))
    c.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r0},{r0} 0 0 1 {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{RO}" stroke-width="2"/>')
    c.append(t(cx - r0 - 6, cy - 16, "7,2°", 13, RO, "end", "700"))
    c.append(circ(cx, cy, 4, NE, "none"))
    c.append(t(cx + 8, cy + 18, "centro de la Tierra", 11, GR, "start"))
    c.append(t(sx + 16, (sy + ay_) / 2 + 4, "≈ 800 km", 12, NE, "start", "700"))
    c.append(t(450, 540, "7,2° es 1/50 de la circunferencia (360°), así que la circunferencia de la Tierra ≈ 50 × 800 km ≈ 40 000 km.", 13, NE))
    c.append(t(450, 560, "Ángulos exagerados para que se vean.", 11, GR, italic=True))
    svg("eratostenes.svg", 900, 575,
        "La Tierra como un círculo iluminado por rayos solares paralelos. En Siena el Sol está en el cénit y no hay sombra; en Alejandría una varilla vertical proyecta una sombra que forma un ángulo de 7,2 grados, igual al ángulo en el centro de la Tierra entre ambas ciudades, separadas unos 800 km",
        "\n".join(c))


# 3. Universo de Aristóteles ----------------------------------------------------
def aristoteles():
    c = [t(450, 28, "El universo de Aristóteles", 18, weight="700")]
    cx, cy = 300, 300
    capas = [(34, "Luna"), (62, "Mercurio"), (88, "Venus"), (114, "Sol"), (140, "Marte"),
             (166, "Júpiter"), (192, "Saturno"), (222, "estrellas fijas")]
    c.append(circ(cx, cy, 240, "#f8f9fa", "#adb5bd", 1.5))
    c.append(circ(cx, cy, 34, "#e7f5ff", "none"))
    for r, nombre in reversed(capas):
        col = SOL if nombre == "Sol" else ("#7048e8" if nombre == "estrellas fijas" else GR)
        c.append(circ(cx, cy, r, "none", col, 2 if nombre in ("Luna", "estrellas fijas") else 1.3))
    for r, nombre in capas:
        ang = math.radians(-35)
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
        col = "#e67700" if nombre == "Sol" else ("#7048e8" if nombre == "estrellas fijas" else NE)
        c.append(circ(px, py, 5 if nombre != "estrellas fijas" else 3, SOL if nombre == "Sol" else col, "none"))
    for i, (r, nombre) in enumerate(capas):
        c.append(t(cx, cy - r + 14 if r > 34 else cy - 14, nombre, 10 if r < 100 else 11, NE))
    c.append(circ(cx, cy, 10, "#2f9e44", "none"))
    c.append(t(cx, cy + 24, "Tierra", 11, NE, weight="700"))
    c.append(t(cx, cy + 232, "primer motor", 11, "#7048e8", italic=True))
    x0 = 570
    c.append(f'<rect x="{x0}" y="80" width="300" height="130" rx="10" fill="#e7f5ff" stroke="{AZ}"/>')
    c.append(t(x0 + 14, 104, "Mundo sublunar", 14, AZ, "start", "700"))
    for i, s in enumerate(["Bajo la esfera de la Luna.", "Cuatro elementos: tierra, agua,", "aire y fuego.", "Todo cambia, nace y muere.", "Movimiento natural: rectilíneo."]):
        c.append(t(x0 + 14, 126 + 18 * i, s, 12, NE, "start"))
    c.append(f'<rect x="{x0}" y="240" width="300" height="130" rx="10" fill="#f3f0ff" stroke="#7048e8"/>')
    c.append(t(x0 + 14, 264, "Mundo supralunar", 14, "#7048e8", "start", "700"))
    for i, s in enumerate(["Desde la Luna hacia afuera.", "Un quinto elemento: el éter.", "Perfecto e inmutable.", "Movimiento natural: circular", "y uniforme, para siempre."]):
        c.append(t(x0 + 14, 286 + 18 * i, s, 12, NE, "start"))
    c.append(t(x0, 410, "La Tierra, inmóvil, en el centro;", 12, GR, "start"))
    c.append(t(x0, 428, "cada astro va en su esfera transparente.", 12, GR, "start"))
    c.append(t(x0, 446, "Esquema simplificado; sin escala.", 11, GR, "start", italic=True))
    svg("universo-aristoteles.svg", 900, 560,
        "Esferas concéntricas con la Tierra inmóvil en el centro; hacia afuera, las esferas de la Luna, Mercurio, Venus, el Sol, Marte, Júpiter, Saturno y las estrellas fijas. Bajo la Luna está el mundo sublunar, de cuatro elementos y cambiante; desde la Luna hacia afuera, el mundo supralunar, de éter, perfecto y con movimiento circular",
        "\n".join(c))


# 4. Epiciclo y deferente --------------------------------------------------------
def epiciclo():
    c = [t(450, 28, "El modelo de Ptolomeo: epiciclo y deferente", 18, weight="700")]
    cx, cy, R, r = 330, 300, 170, 60
    c.append(circ(cx, cy, R, "none", GR, 1.8))
    # trayectoria resultante (epitrocoide)
    pts = []
    for i in range(0, 1201):
        th = 2 * math.pi * i / 1200
        ph = 7 * th
        pts.append((cx + R * math.cos(th) + r * math.cos(ph), cy - R * math.sin(th) - r * math.sin(ph)))
    c.append(poly(pts, MAR_, 1.4, extra='stroke-dasharray="4 3" opacity="0.7"'))
    th0 = math.radians(40)
    ex, ey = cx + R * math.cos(th0), cy - R * math.sin(th0)
    c.append(circ(ex, ey, r, "none", AZ, 2))
    ph0 = 7 * th0
    px, py = ex + r * math.cos(ph0), ey - r * math.sin(ph0)
    c.append(ln(cx, cy, ex, ey, GR, 1, PUNT))
    c.append(ln(ex, ey, px, py, AZ, 1, PUNT))
    c.append(circ(ex, ey, 3.5, AZ, "none"))
    c.append(circ(px, py, 8, MAR_, "none"))
    c.append(t(px + 12, py - 8, "planeta", 13, MAR_, "start", "700"))
    c.append(t(ex + r + 8, ey + 30, "epiciclo", 13, AZ, "start", "700"))
    c.append(t(cx - R + 10, cy + R - 34, "deferente", 13, GR, "start", "700"))
    c.append(circ(cx - 22, cy + 6, 11, "#2f9e44", "none"))
    c.append(t(cx - 22, cy + 32, "Tierra", 12, NE, weight="700"))
    c.append(circ(cx + 22, cy - 6, 3.5, NE, "none"))
    c.append(t(cx + 28, cy - 12, "ecuante", 11, NE, "start"))
    x0 = 580
    txt = ["El planeta gira en un círculo pequeño,", "el epiciclo, cuyo centro recorre un", "círculo grande, el deferente.", "",
           "Visto desde la Tierra, el planeta", "a veces avanza y a veces", "retrocede: la línea punteada roja", "muestra los lazos.", "",
           "La Tierra no está exactamente en", "el centro del deferente, y el", "centro del epiciclo se mueve", "uniforme visto desde el ecuante."]
    for i, s in enumerate(txt):
        c.append(t(x0, 120 + 20 * i, s, 13, NE, "start"))
    c.append(t(x0, 520, "Sin escala; un epiciclo por planeta.", 11, GR, "start", italic=True))
    svg("epiciclo-deferente.svg", 900, 540,
        "Un círculo grande, el deferente, con la Tierra cerca de su centro y un punto llamado ecuante. Sobre el deferente se mueve el centro de un círculo pequeño, el epiciclo, que lleva al planeta. La trayectoria resultante, en línea punteada, forma lazos",
        "\n".join(c))


# 5. Tres modelos -----------------------------------------------------------------
def modelos():
    c = [t(450, 28, "Tres modelos del sistema solar", 18, weight="700")]
    paneles = [(150, "Ptolomeo (~150 d. C.)", "geocéntrico"), (450, "Copérnico (1543)", "heliocéntrico"),
               (750, "Tycho Brahe (1588)", "geoheliocéntrico")]
    cy = 260
    for cx, tit, sub in paneles:
        c.append(t(cx, 70, tit, 14, NE, weight="700"))
        c.append(t(cx, 90, sub, 12, GR, italic=True))
    # Ptolomeo
    cx = 150
    orden = [(26, "Luna", GR), (44, "Mercurio", GR), (62, "Venus", VEN), (80, "Sol", SOL), (100, "Marte", MAR_), (118, "Júpiter", GR), (136, "Saturno", GR)]
    for r, n, col in orden:
        c.append(circ(cx, cy, r, "none", col, 1.2))
        c.append(circ(cx + r, cy, 7 if n == "Sol" else 4, col, "none"))
    c.append(circ(cx, cy, 8, "#2f9e44", "none"))
    c.append(t(cx, cy + 160, "Tierra inmóvil en el centro", 12, NE))
    c.append(t(cx, cy + 178, "(epiciclos no dibujados)", 11, GR, italic=True))
    # Copérnico
    cx = 450
    orden = [(24, "Mercurio", GR), (44, "Venus", VEN), (66, "Tierra", "#2f9e44"), (90, "Marte", MAR_), (114, "Júpiter", GR), (136, "Saturno", GR)]
    for r, n, col in orden:
        c.append(circ(cx, cy, r, "none", col, 1.2))
        c.append(circ(cx + r * 0.7, cy - r * 0.714, 6 if n == "Tierra" else 4, col, "none"))
    c.append(circ(cx + 66 * 0.7 + 12, cy - 66 * 0.714, 6, "none", GR, 1))
    c.append(circ(cx + 66 * 0.7 + 12, cy - 66 * 0.714 + 6, 2.5, GR, "none"))
    c.append(sol(cx, cy, 10))
    c.append(t(cx, cy + 160, "Sol en el centro; la Tierra es", 12, NE))
    c.append(t(cx, cy + 178, "un planeta y la Luna gira en torno a ella", 12, NE))
    # Tycho
    cx = 750
    c.append(circ(cx, cy, 8, "#2f9e44", "none"))
    c.append(circ(cx, cy, 30, "none", GR, 1.2))
    c.append(circ(cx - 30, cy, 4, GR, "none"))
    c.append(circ(cx, cy, 95, "none", SOL, 1.5))
    sx, sy = cx + 95 * math.cos(math.radians(30)), cy - 95 * math.sin(math.radians(30))
    for r, col in ((18, GR), (34, VEN), (62, MAR_)):
        c.append(circ(sx, sy, r, "none", col, 1.2, PUNT2))
        c.append(circ(sx - r, sy, 4, col, "none"))
    c.append(sol(sx, sy, 9))
    c.append(t(cx, cy + 160, "Luna y Sol giran en torno a la Tierra;", 12, NE))
    c.append(t(cx, cy + 178, "los demás planetas, en torno al Sol", 12, NE))
    # leyenda
    ley = [("#2f9e44", "Tierra"), (SOL, "Sol"), (VEN, "Venus"), (MAR_, "Marte"), (GR, "otros")]
    for i, (col, n) in enumerate(ley):
        c.append(circ(250 + 100 * i, 490, 6, col, "none"))
        c.append(t(262 + 100 * i, 494, n, 12, NE, "start"))
    c.append(t(450, 520, "Esquemas sin escala.", 11, GR, italic=True))
    svg("tres-modelos.svg", 900, 535,
        "Tres esquemas. Ptolomeo: la Tierra inmóvil al centro y alrededor la Luna, Mercurio, Venus, el Sol, Marte, Júpiter y Saturno. Copérnico: el Sol al centro y alrededor Mercurio, Venus, la Tierra con la Luna, Marte, Júpiter y Saturno. Tycho Brahe: la Tierra al centro, con la Luna y el Sol girando en torno a ella, y los demás planetas girando en torno al Sol",
        "\n".join(c))


# 6. Fases de Venus ---------------------------------------------------------------
def venus():
    c = [t(450, 28, "Las fases de Venus: la prueba de Galileo", 18, weight="700")]
    # Panel geocéntrico
    c.append(t(220, 64, "Si Ptolomeo tuviera razón", 14, RO, weight="700"))
    tx, ty = 220, 440
    c.append(circ(tx, ty, 10, "#2f9e44", "none"))
    c.append(t(tx, ty + 28, "Tierra", 12, NE, weight="700"))
    sx, sy = 220, 110
    c.append(sol(sx, sy, 20))
    c.append(t(sx + 28, sy + 4, "Sol", 12, NE, "start", "700"))
    c.append(ln(tx, ty, sx, sy, GR, 1, PUNT))
    ex, ey, r = 220, 260, 55
    c.append(circ(ex, ey, r, "none", VEN, 1.5, PUNT2))
    c.append(circ(ex, ey, 3, VEN, "none"))
    c.append(t(ex + r + 6, ey + 40, "epiciclo", 11, VEN, "start"))
    for ang in (90, 150, 210, 270, 330, 30):
        a = math.radians(ang)
        vx, vy = ex + r * math.cos(a), ey - r * math.sin(a)
        # Venus siempre entre Tierra y Sol: se ve nueva o creciente
        k = 0.08 if ang in (90,) else (0.02 if ang == 270 else 0.25)
        c.append(circ(vx, vy, 7, "#fff3bf", "#e67700", 1))
    c.append(f'<rect x="100" y="334" width="240" height="60" fill="#fff"/>')
    c.append(t(220, 350, "Venus nunca pasa detrás del Sol:", 12, NE))
    c.append(t(220, 368, "desde la Tierra se vería", 12, NE))
    c.append(t(220, 386, "solo nueva o creciente", 12, NE))
    for i, k in enumerate((0.0, 0.1, 0.25, 0.1)):
        c.append(fase(150 + 46 * i, 500, 14, k, rot=-90 if False else 0))
    # Panel heliocéntrico
    c.append(t(660, 64, "Con el modelo heliocéntrico", 14, VE, weight="700"))
    sx, sy = 660, 240
    c.append(sol(sx, sy, 20))
    rv = 95
    c.append(circ(sx, sy, rv, "none", VEN, 1.5, PUNT2))
    tx, ty = 660, 440
    c.append(circ(tx, ty, 10, "#2f9e44", "none"))
    c.append(t(tx, ty + 28, "Tierra", 12, NE, weight="700"))
    for ang in (270, 330, 30, 90, 150, 210):
        a = math.radians(ang)
        vx, vy = sx + rv * math.cos(a), sy - rv * math.sin(a)
        c.append(circ(vx, vy, 7, "#fff3bf", "#e67700", 1))
    c.append(t(sx, sy - rv - 14, "lejos: casi llena y pequeña", 12, NE))
    c.append(t(sx + 16, sy + rv + 22, "cerca: creciente y grande", 12, NE, "start"))
    # fases vistas desde la Tierra (tamaño aparente)
    datos = [(0.95, 8), (0.75, 10), (0.5, 13), (0.25, 18), (0.08, 24)]
    x = 540
    for k, rr in datos:
        c.append(fase(x, 500, rr, k))
        x += rr + 34
    c.append(t(450, 548, "Abajo: cómo se vería Venus desde la Tierra en cada caso (la parte iluminada mira hacia el Sol).", 12, GR))
    c.append(t(450, 566, "Galileo observó en 1610 el ciclo completo de fases y el cambio de tamaño: el esquema de la izquierda no lo explica.", 12, NE, weight="700"))
    c.append(ln(450, 60, 450, 520, "#dee2e6", 1.5))
    svg("fases-venus.svg", 900, 580,
        "Dos esquemas. A la izquierda, el modelo de Ptolomeo: Venus gira en un epiciclo siempre entre la Tierra y el Sol, por lo que desde la Tierra solo se vería nueva o creciente. A la derecha, el modelo heliocéntrico: Venus gira en torno al Sol y desde la Tierra se ve casi llena y pequeña cuando está lejos, detrás del Sol, y creciente y grande cuando está cerca",
        "\n".join(c))


# 7. Leyes de Kepler -------------------------------------------------------------
def kepler():
    c = [t(450, 28, "Primera y segunda ley de Kepler", 18, weight="700")]
    a, e = 300, 0.6
    b = a * math.sqrt(1 - e * e)
    cx, cy = 450, 270
    fx = cx - a * e  # Sol en el foco izquierdo
    c.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{a}" ry="{b:.1f}" fill="none" stroke="{AZ}" stroke-width="2.2"/>')

    def pos(M):
        E = M
        for _ in range(50):
            E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        # perihelio a la izquierda
        x = -a * math.cos(E)
        y = b * math.sin(E)
        return cx + x, cy - y

    def sector(M0, M1, col):
        pts = [(fx, cy)] + [pos(M0 + (M1 - M0) * i / 60) for i in range(61)]
        return poligono(pts, col, 0.35)

    dM = 0.55
    c.append(sector(-dM / 2, dM / 2, RO))
    c.append(sector(math.pi - dM / 2, math.pi + dM / 2, VE))
    c.append(sol(fx, cy, 14))
    c.append(t(fx + 4, cy + 34, "Sol (en un foco)", 12, NE, weight="700"))
    f2 = cx + a * e
    c.append(f'<line x1="{f2 - 5}" y1="{cy - 5}" x2="{f2 + 5}" y2="{cy + 5}" stroke="{GR}" stroke-width="2"/><line x1="{f2 - 5}" y1="{cy + 5}" x2="{f2 + 5}" y2="{cy - 5}" stroke="{GR}" stroke-width="2"/>')
    c.append(t(f2, cy + 22, "otro foco (vacío)", 11, GR))
    c.append(t(cx - a - 8, cy + 4, "perihelio", 13, RO, "end", "700"))
    c.append(t(cx + a + 8, cy + 4, "afelio", 13, VE, "start", "700"))
    p1, p2 = pos(-dM / 2), pos(dM / 2)
    c.append(t(cx - a - 10, cy - 150, "arco largo: el planeta", 12, RO, "end"))
    c.append(t(cx - a - 10, cy - 134, "va más rápido", 12, RO, "end"))
    c.append(t(cx + a - 70, cy - 120, "arco corto: va", 12, VE, "end"))
    c.append(t(cx + a - 70, cy - 104, "más lento", 12, VE, "end"))
    c.append(t(450, cy + b + 38, "Las dos áreas sombreadas son iguales: el planeta las barre en el mismo tiempo.", 13, NE, weight="700"))
    c.append(t(450, cy + b + 58, "Excentricidad muy exagerada: la órbita de la Tierra (e ≈ 0,017) se vería como una circunferencia.", 12, GR, italic=True))
    svg("leyes-kepler.svg", 900, cy + b + 76,
        "Órbita elíptica muy alargada con el Sol en uno de los focos y el otro foco vacío. Cerca del Sol está el perihelio y en el extremo opuesto el afelio. Dos sectores sombreados de igual área: el del perihelio es corto y ancho, con un arco largo, y el del afelio es largo y angosto, con un arco corto",
        "\n".join(c))


# 8. Tercera ley ------------------------------------------------------------------
def tercera():
    c = [t(450, 28, "Tercera ley de Kepler: T² es proporcional a a³", 18, weight="700")]
    datos = [("Mercurio", 0.387, 0.241), ("Venus", 0.723, 0.615), ("Tierra", 1.0, 1.0), ("Marte", 1.524, 1.881), ("Ceres", 2.77, 4.60)]
    c.append(t(450, 52, "a: semieje mayor de la órbita, en unidades astronómicas (UA) · T: período orbital, en años", 12, GR))
    ox, oy = 130, 470
    P = ejes(c, ox + 10, oy, 690, 390, "a³ (UA³)", "T² (años²)", [0, 5, 10, 15, 20], [0, 5, 10, 15, 20], 30, 16.5)
    x1, y1 = P(0, 0)
    x2, y2 = P(22, 22)
    c.append(ln(x1, y1, x2, y2, AZ, 2, PUNT))
    for n, a, T in datos:
        x, y = P(a ** 3, T ** 2)
        c.append(circ(x, y, 6, RO, "#fff", 1.2))
        if n in ("Mercurio", "Venus", "Tierra"):
            ly = {"Mercurio": 446, "Venus": 428, "Tierra": 410}[n]
            c.append(ln(x, y, 104, ly - 4, "#adb5bd", 1))
            c.append(t(100, ly, n, 12, NE, "end", "700"))
        else:
            c.append(t(x + (10 if n == "Marte" else -12), y + 4, n, 12, NE, "start" if n == "Marte" else "end", "700"))
    c.append(t(640, 130, "Todos los puntos caen en la misma recta:", 13, NE, "end"))
    c.append(t(640, 150, "T² / a³ = 1 año²/UA³ para todo el sistema solar", 13, AZ, "end", "700"))
    c.append(t(640, 170, "(Ceres es un planeta enano del cinturón de asteroides)", 11, GR, "end", italic=True))
    svg("tercera-ley-kepler.svg", 900, 520,
        "Gráfico del período orbital al cuadrado, en años al cuadrado, en función del semieje mayor al cubo, en unidades astronómicas al cubo. Mercurio, Venus, la Tierra, Marte y Ceres caen sobre una misma recta que pasa por el origen, de pendiente 1",
        "\n".join(c))


# 9. Ley de Hubble ----------------------------------------------------------------
def hubble():
    c = [t(450, 28, "Ley de Hubble-Lemaître: las galaxias más lejanas se alejan más rápido", 18, weight="700")]
    ox, oy = 130, 470
    P = ejes(c, ox, oy, 680, 380, "distancia d (Mpc)", "rapidez de alejamiento v (km/s)",
             [0, 100, 200, 300, 400], [0, 5000, 10000, 15000, 20000, 25000], 1.6, 0.0145,
             fmt=lambda v: miles(v))
    import random
    rnd = random.Random(7)
    for i in range(22):
        d = 20 + 17 * i + rnd.uniform(-8, 8)
        v = 70 * d * rnd.uniform(0.9, 1.1)
        x, y = P(d, v)
        c.append(circ(x, y, 4.5, RO, "none"))
    x1, y1 = P(0, 0)
    x2, y2 = P(390, 70 * 390)
    c.append(ln(x1, y1, x2, y2, AZ, 2.2))
    c.append(t(x2 + 8, y2 + 26, "v = H₀ · d", 14, AZ, "start", "700"))
    c.append(t(170, 110, "Pendiente: H₀ ≈ 70 km/s por megapársec", 13, NE, "start", "700"))
    c.append(t(170, 130, "1 Mpc ≈ 3,26 millones de años luz", 12, GR, "start"))
    c.append(t(170, 150, "Datos ilustrativos, con la dispersión típica de las mediciones.", 11, GR, "start", italic=True))
    svg("ley-hubble.svg", 900, 520,
        "Gráfico de la rapidez de alejamiento de galaxias, en kilómetros por segundo, en función de su distancia, en megapársecs. Los puntos siguen una recta que pasa por el origen, cuya pendiente es la constante de Hubble, de unos 70 kilómetros por segundo por megapársec",
        "\n".join(c))


# 10. Corrimiento al rojo --------------------------------------------------------
def espectro_color(nm):
    stops = [(380, (110, 0, 160)), (440, (40, 40, 255)), (490, (0, 190, 220)), (510, (0, 200, 60)),
             (580, (240, 230, 0)), (620, (255, 120, 0)), (700, (220, 0, 0)), (750, (120, 0, 0))]
    for (l0, c0), (l1, c1) in zip(stops, stops[1:]):
        if l0 <= nm <= l1:
            f = (nm - l0) / (l1 - l0)
            return "#%02x%02x%02x" % tuple(int(a + (b - a) * f) for a, b in zip(c0, c1))
    return "#000"


def corrimiento():
    c = [t(450, 28, "Corrimiento al rojo en el espectro de una galaxia", 18, weight="700")]
    x0, x1, l0, l1 = 90, 810, 380, 750
    X = lambda nm: x0 + (nm - l0) / (l1 - l0) * (x1 - x0)
    grad = "".join(f'<stop offset="{(nm - l0) / (l1 - l0):.3f}" stop-color="{espectro_color(nm)}"/>' for nm in range(380, 751, 10))
    c.append(f'<defs><linearGradient id="esp">{grad}</linearGradient></defs>')
    lineas = [410.2, 434.0, 486.1, 656.3]
    z = 0.05
    for yb, tit, sh in ((80, "Hidrógeno en un laboratorio (en reposo)", 1.0), (230, "Hidrógeno en una galaxia lejana (z = 0,05)", 1 + z)):
        c.append(t(x0, yb - 10, tit, 14, NE, "start", "700"))
        c.append(f'<rect x="{x0}" y="{yb}" width="{x1 - x0}" height="60" fill="url(#esp)"/>')
        for lam in lineas:
            c.append(ln(X(lam * sh), yb, X(lam * sh), yb + 60, "#000", 3.5))
    for lam in lineas:
        c.append(ln(X(lam), 142, X(lam * (1 + z)), 196, "#495057", 1.3, 'marker-end="url(#mg)"'))
    for nm in (400, 450, 500, 550, 600, 650, 700, 750):
        c.append(ln(X(nm), 292, X(nm), 300, GR, 1))
        c.append(t(X(nm), 316, str(nm), 11, GR))
    c.append(t(x1, 336, "longitud de onda λ (nm)", 12, GR, "end"))
    c.append(t(450, 368, "Las mismas líneas aparecen desplazadas hacia longitudes de onda mayores (hacia el rojo).", 13, NE, weight="700"))
    c.append(t(450, 388, "z = Δλ / λ = (689 − 656) / 656 ≈ 0,05. Para z pequeño, v ≈ z · c ≈ 15 000 km/s de alejamiento.", 13, NE))
    svg("corrimiento-al-rojo.svg", 900, 405,
        "Dos franjas del espectro visible con cuatro líneas oscuras del hidrógeno. En la franja de laboratorio las líneas están en 410, 434, 486 y 656 nanómetros; en la de una galaxia lejana las mismas líneas aparecen desplazadas unos 5 por ciento hacia longitudes de onda mayores, hacia el rojo",
        "\n".join(c))


# 11. Línea de tiempo --------------------------------------------------------------
def linea():
    c = [t(450, 28, "Una historia del universo en 13 800 millones de años", 18, weight="700")]
    y = 200
    xs = [60, 170, 280, 390, 500, 610, 720, 840]
    c.append(f'<defs><linearGradient id="lt"><stop offset="0" stop-color="#fff3bf"/><stop offset="0.35" stop-color="#ffa94d"/><stop offset="0.55" stop-color="#5c7cfa"/><stop offset="1" stop-color="#1a1b4b"/></linearGradient></defs>')
    c.append(f'<rect x="50" y="{y - 10}" width="800" height="20" rx="10" fill="url(#lt)"/>')
    hitos = [("0", "Big Bang", ["inicio de la", "expansión"]),
             ("≈ 10⁻³² s", "Inflación", ["expansión muy", "rápida"]),
             ("≈ 1 s", "Protones y", ["neutrones"]),
             ("≈ 3 min", "Núcleos de", ["H y He (≈ 75 %", "y 25 % en masa)"]),
             ("380 000 años", "Átomos neutros", ["se libera la radiación", "de fondo"]),
             ("≈ 200 millones", "Primeras", ["estrellas y", "galaxias"]),
             ("9 200 millones", "Se forma el", ["Sistema Solar", "(hace 4 600 millones)"]),
             ("13 800 millones", "Hoy", ["expansión", "acelerada"])]
    for i, (x, (tt, h, rest)) in enumerate(zip(xs, hitos)):
        c.append(circ(x, y, 7, "#fff", NE, 2))
        up = i % 2 == 0
        yy = y - 30 if up else y + 38
        c.append(ln(x, y - 8 if up else y + 8, x, yy + (8 if up else -16), GR, 1))
        if up:
            c.append(t(x, yy - 30 - 16 * len(rest), tt, 12, AZ, weight="700"))
            c.append(t(x, yy - 14 - 16 * len(rest), h, 13, NE, weight="700"))
            for j, r_ in enumerate(rest):
                c.append(t(x, yy + 2 - 16 * (len(rest) - j), r_, 11, GR))
        else:
            c.append(t(x, yy, tt, 12, AZ, weight="700"))
            c.append(t(x, yy + 18, h, 13, NE, weight="700"))
            for j, r_ in enumerate(rest):
                c.append(t(x, yy + 34 + 15 * j, r_, 11, GR))
    c.append(t(450, 350, "Tiempo desde el Big Bang. Escala no proporcional: los primeros minutos ocupan tanto espacio como miles de millones de años.", 11, GR, italic=True))
    svg("historia-universo.svg", 900, 365,
        "Línea de tiempo del universo: Big Bang; inflación a unos 10 elevado a menos 32 segundos; protones y neutrones al primer segundo; núcleos de hidrógeno y helio a los 3 minutos; átomos neutros y liberación de la radiación de fondo a los 380 000 años; primeras estrellas a unos 200 millones de años; formación del Sistema Solar a los 9 200 millones de años; hoy, a los 13 800 millones de años, con expansión acelerada",
        "\n".join(c))


# 12. Destinos del universo ---------------------------------------------------------
def destinos():
    c = [t(450, 28, "¿Cómo podría terminar el universo?", 18, weight="700")]
    ox, oy, W, H = 110, 450, 720, 370
    c.append(ln(ox, oy, ox + W, oy, GR, 1.5, 'marker-end="url(#mg)"'))
    c.append(ln(ox, oy, ox, oy - H, GR, 1.5, 'marker-end="url(#mg)"'))
    c.append(t(ox + W, oy + 26, "tiempo", 12, GR, "end"))
    c.append(t(ox + 6, oy - H - 6, "tamaño del universo (distancia entre galaxias)", 12, GR, "start"))
    th = 260  # hoy
    yh = oy - 150
    c.append(ln(ox + th, oy, ox + th, oy - H + 20, GR, 1, PUNT))
    c.append(t(ox + th, oy + 18, "hoy", 12, NE, weight="700"))
    c.append(t(ox + 4, oy + 18, "Big Bang", 12, NE, "start", "700"))
    # pasado común
    past = [(ox + x, oy - 150 * (x / th) ** 0.66) for x in range(0, th + 1, 4)]
    c.append(poly(past, NE, 2.8))

    def rama(f, x_max, col):
        pts = []
        for x in range(th, x_max + 1, 4):
            y = f(x)
            if y is None:
                break
            pts.append((ox + x, min(oy, y)))
        return poly(pts, col, 2.6)

    # Big Crunch: sube y baja
    c.append(rama(lambda x: yh - 110 * math.sin(math.pi * (x - th) / 700 + 0.001) + 0.0015 * (x - th) ** 2 * 0 - (0 if x < 600 else 0), 700, VE))
    crunch = [(ox + x, yh - 90 * math.sin(math.pi * (x - th) / 440 * 0.5 + 0.0) * 1 - 0) for x in range(th, th + 1)]
    # redefinir Big Crunch explícitamente como parábola
    c.pop()
    cr = []
    for x in range(th, 720, 4):
        u = (x - th) / (700 - th)
        y = yh - 120 * math.sin(math.pi * u * 0.95) ** 1 + 150 * u ** 3 * 0
        cr.append((ox + x, y))
    # que termine en el eje: ajuste lineal final
    cr = []
    for x in range(th, 700, 4):
        u = (x - th) / (700 - th)
        y = yh - 100 * math.sin(math.pi * u) + 150 * u ** 2
        cr.append((ox + x, min(oy, y)))
    c.append(poly(cr, VE, 2.6))
    # Big Freeze: crece cada vez más lento
    fr = [(ox + x, yh - 70 * math.log(1 + (x - th) / 60)) for x in range(th, 720, 4)]
    c.append(poly(fr, AZ, 2.6))
    # Acelerada (energía oscura constante): exponencial
    ac = []
    for x in range(th, 720, 4):
        y = yh - 60 * (math.exp((x - th) / 190) - 1) - 0.4 * (x - th)
        if y < oy - H + 30:
            break
        ac.append((ox + x, y))
    c.append(poly(ac, NA, 2.6))
    # Big Rip: diverge en tiempo finito
    rp = []
    for x in range(th, 720, 2):
        y = yh - 50 * ((520 - th) / (520 - x) - 1) * 1.0 - 0.4 * (x - th)
        if y < oy - H + 30:
            break
        rp.append((ox + x, y))
    c.append(poly(rp, RO, 2.6))
    ex, ey = cr[-1]
    c.append(t(ex - 14, ey - 22, "Big Crunch", 13, VE, "end", "700"))
    c.append(t(ex - 14, ey - 6, "(gran implosión)", 11, VE, "end"))
    fx, fy = fr[-1]
    c.append(t(fx, fy + 24, "Big Freeze", 13, AZ, "end", "700"))
    c.append(t(fx, fy + 40, "(expansión eterna; todo se enfría)", 11, AZ, "end"))
    axx, ayy = ac[-1]
    c.append(t(axx + 8, ayy + 8, "Expansión acelerada", 13, NA, "start", "700"))
    c.append(t(axx + 8, ayy + 24, "(lo que se mide hoy)", 11, NA, "start"))
    rx, ry = rp[-1]
    c.append(t(rx - 8, ry + 4, "Big Rip", 13, RO, "end", "700"))
    c.append(t(rx - 8, ry + 20, "(gran desgarro)", 11, RO, "end"))
    c.append(t(450, 490, "Curvas cualitativas: el futuro depende de cuánta materia hay y de cómo se comporta la energía oscura.", 12, GR, italic=True))
    svg("destinos-universo.svg", 900, 505,
        "Gráfico cualitativo del tamaño del universo en función del tiempo. Desde el Big Bang hasta hoy la curva crece. Después se abren cuatro posibilidades: Big Crunch, en que el universo deja de expandirse y colapsa; Big Freeze, expansión eterna cada vez más lenta; expansión acelerada, que es lo que se mide hoy; y Big Rip, en que la expansión se vuelve infinita en un tiempo finito",
        "\n".join(c))


os.makedirs(OUT, exist_ok=True)
for fn in (retrogrado, eratostenes, aristoteles, epiciclo, modelos, venus, kepler, tercera, hubble, corrimiento, linea, destinos):
    fn()
print("ok")
