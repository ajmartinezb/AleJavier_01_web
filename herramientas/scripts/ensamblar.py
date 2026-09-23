"""Arma el sitio final a partir de los fragmentos HTML escritos por el modelo.

Uso:
  python ensamblar.py --secciones secciones.json --fragmentos fragmentos --salida sitio \
      [--pdf libro.pdf] [--titulo "Biología"] [--color "#2f855a"] [--incrustar] [--marcas] [--zip]

secciones.json:
  {"documento": "Biología 6ª ed.", "color": "#2f855a",
   "secciones": [{"titulo": "Capítulo 1: Método científico", "desde": 17, "hasta": 50}, ...]}

Fragmentos: fragmentos/01-*.html, fragmentos/02-*.html ... (el número = posición de la sección,
desde 01). Se concatenan en orden alfabético. Cada fragmento debería empezar con
<!-- pdf: 17-19 --> indicando qué páginas del PDF contiene; así el informe detecta faltantes.

Hace: limpia el HTML, recorta las figuras <figure data-pagina data-recorte> desde el PDF,
pone ids a los títulos, arma el índice lateral, navegación anterior/siguiente, index.html
y (opcional) un ZIP. Imprime un informe JSON (páginas faltantes, preguntas sin clave, etc.).
"""
import argparse
import base64
import glob
import html
import json
import os
import re
import shutil
import sys

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from comun import ajustar_caja, imprimir_json, pymupdf, recortar_png, slug

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")


def oscurecer(hexa, f=0.55):
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", hexa or "")
    if not m:
        return "#1f3b5c"
    n = int(m.group(1), 16)
    return "#" + "".join(f"{round(((n >> s) & 255) * f):02x}" for s in (16, 8, 0))


def esc(s):
    return html.escape(str(s or ""), quote=True)


def limpiar(fragmento):
    t = fragmento.strip()
    t = re.sub(r"^```(?:html)?\s*|```\s*$", "", t, flags=re.I | re.M)
    t = re.sub(r"(?is)<(script|style|iframe|object|embed|form)\b.*?</\1\s*>", "", t)
    t = re.sub(r"(?is)<(link|meta|base)\b[^>]*>", "", t)
    t = re.sub(r"(?is)</?(html|head|body)\b[^>]*>", "", t)
    t = re.sub(r"""(?is)\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)""", "", t)
    t = re.sub(r"""(?is)(href|src)\s*=\s*(["'])\s*javascript:[^"']*\2""", r'\1="#"', t)
    t = re.sub(r"(?is)<h1(\b[^>]*)>(.*?)</h1>", r"<h2\1>\2</h2>", t)
    return t


def paginas_cubiertas(texto):
    cub = set()
    for a, b in re.findall(r"<!--\s*pdf:\s*(\d+)(?:\s*-\s*(\d+))?\s*-->", texto):
        cub.update(range(int(a), int(b or a) + 1))
    return cub


class Recortador:
    def __init__(self, ruta_pdf, ajustar=True):
        self.doc = pymupdf.open(ruta_pdf) if (ruta_pdf and pymupdf) else None
        self.ajustar = ajustar
        self.ajustadas = []

    def recortar(self, pagina, caja, destino):
        """Guarda el recorte (ajustado) y devuelve la caja final 0-1000, o None."""
        if not self.doc or not (1 <= pagina <= self.doc.page_count):
            return None
        pag = self.doc[pagina - 1]
        caja = [max(0.0, min(1000.0, v)) for v in caja]
        caja = [min(caja[0], caja[2]), min(caja[1], caja[3]), max(caja[0], caja[2]), max(caja[1], caja[3])]
        if caja[2] - caja[0] < 15 or caja[3] - caja[1] < 15:
            return None
        if self.ajustar:
            nueva, cambio = ajustar_caja(pag, caja)
            if cambio:
                self.ajustadas.append({"pagina": pagina, "antes": [round(v) for v in caja], "despues": nueva})
            caja = nueva
        pix = recortar_png(pag, caja, 2200)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        pix.save(destino, jpg_quality=88)
        return caja

    def portada(self, pagina, destino, fraccion=0.42):
        """Miniatura de la parte superior de la primera página de la sección (para el índice)."""
        if not self.doc or not (1 <= pagina <= self.doc.page_count):
            return False
        pix = recortar_png(self.doc[pagina - 1], [0, 0, 1000, round(fraccion * 1000)], 1100)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        pix.save(destino, jpg_quality=82)
        return True


def procesar_figuras(cuerpo, idx, sec, recortador, salida, incrustar, avisos):
    n = 0

    def reemplazo(m):
        nonlocal n
        atributos, interior = m.group(1), m.group(2)
        pag = re.search(r'data-pagina\s*=\s*"(\d+)"', atributos)
        caja = re.search(r'data-recorte\s*=\s*"([^"]+)"', atributos)
        atributos_limpios = re.sub(r'\s*data-recorte\s*=\s*"[^"]*"', "", atributos)
        if "<img" in interior or not (pag and caja):
            return f"<figure{atributos_limpios}>{interior}</figure>"
        try:
            numeros = [float(x) for x in caja.group(1).split(",")]
            assert len(numeros) == 4
        except (ValueError, AssertionError):
            avisos.append(f"Sección {idx}: recorte inválido «{caja.group(1)}»")
            return f"<figure{atributos_limpios}>{interior}</figure>"
        p = int(pag.group(1))
        if "desde" in sec and not (sec["desde"] <= p <= sec["hasta"]):
            avisos.append(f"Sección {idx}: figura de la página {p} fuera del rango {sec['desde']}-{sec['hasta']}")
        n += 1
        rel = f"assets/s{idx:02d}-p{p}-{n}.jpg"
        ruta = os.path.join(salida, rel)
        final = recortador.recortar(p, numeros, ruta)
        if not final:
            avisos.append(f"Sección {idx}: no se pudo recortar la figura de la página {p} (¿falta --pdf o PyMuPDF?)")
            return f"<figure{atributos_limpios}>{interior}</figure>"
        # Mismo ancho relativo que en el libro (la columna de texto ocupa ~80% de la página).
        ancho = max(22, min(100, round((final[2] - final[0]) / 8)))
        atributos_limpios = re.sub(r'\s*style\s*=\s*"[^"]*"', "", atributos_limpios) + f' style="--ancho:{ancho}%"'
        src = rel
        if incrustar:
            with open(ruta, "rb") as f:
                src = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
            os.remove(ruta)
        leyenda = re.sub(r"<[^>]+>", "", interior).strip() or f"Figura de la página {p}"
        return f'<figure{atributos_limpios}><img src="{src}" alt="{esc(leyenda[:160])}" loading="lazy">{interior}</figure>'

    return re.sub(r"(?is)<figure\b([^>]*)>(.*?)</figure>", reemplazo, cuerpo), n


def ids_y_toc(cuerpo):
    usados, toc = set(), []

    def reemplazo(m):
        nivel, atributos, contenido = m.group(1), m.group(2), m.group(3)
        texto = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", contenido))).strip()
        if not texto:
            return m.group(0)
        existente = re.search(r'\bid\s*=\s*"([^"]+)"', atributos)
        if existente:
            ident = existente.group(1)
        else:
            base = slug(texto, 50)
            ident, k = base, 2
            while ident in usados:
                ident, k = f"{base}-{k}", k + 1
            atributos += f' id="{ident}"'
        usados.add(ident)
        if nivel in "23":
            toc.append((int(nivel), ident, texto if len(texto) <= 70 else texto[:68] + "…"))
        return f"<h{nivel}{atributos}>{contenido}</h{nivel}>"

    cuerpo = re.sub(r"(?is)<h([234])\b([^>]*)>(.*?)</h\1>", reemplazo, cuerpo)
    return cuerpo, toc


def _norm(t):
    return slug(html.unescape(re.sub(r"<[^>]+>", "", str(t or ""))), 200)


def insertar_preguntas_ia(cuerpo, toc, ruta_json, avisos, idx):
    """Agrega las preguntas IA al final de la sección, insignias con sus números en cada
    título y el botón «Ver tema» en cada pregunta. Devuelve (cuerpo, toc, estadísticas)."""
    with open(ruta_json, encoding="utf-8") as f:
        datos = json.load(f)
    preguntas = datos.get("preguntas", []) if isinstance(datos, dict) else datos

    titulos = []  # (id, nivel, texto) en orden del documento
    for m in re.finditer(r'(?is)<h([234])\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h\1>', cuerpo):
        titulos.append((m.group(2), int(m.group(1)), re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))).strip()))
    por_id = {t[0]: t for t in titulos}
    por_norm = {}
    for t in titulos:
        por_norm.setdefault(_norm(t[2]), t)

    def buscar(tema):
        tema = str(tema or "").strip().lstrip("#")
        if tema in por_id:
            return por_id[tema]
        n = _norm(tema)
        if n in por_norm:
            return por_norm[n]
        candidatos = [t for t in titulos if _norm(t[2]).startswith(n) or n.startswith(_norm(t[2]))]
        if len(candidatos) == 1:
            return candidatos[0]
        palabras = set(n.split("-")) - {"", "de", "la", "el", "y", "los", "las", "del", "en"}
        mejor, puntaje = None, 0
        for t in titulos:
            comunes = len(palabras & set(_norm(t[2]).split("-")))
            if comunes > puntaje:
                mejor, puntaje = t, comunes
        return mejor if puntaje >= max(1, len(palabras) // 2) else None

    grupos = {}
    for k, q in enumerate(preguntas):
        t = buscar(q.get("tema"))
        if not t:
            avisos.append(f"Sección {idx}: pregunta IA sin título reconocible («{q.get('tema')}»), se omite")
            continue
        alts = q.get("alternativas") or []
        if isinstance(alts, dict):
            alts = [alts[k2] for k2 in sorted(alts)]
        letras = "ABCDE"[:len(alts)]
        correcta = str(q.get("correcta", "")).strip().upper()[:1]
        if not (3 <= len(alts) <= 5) or correcta not in letras or not q.get("enunciado"):
            avisos.append(f"Sección {idx}: pregunta IA inválida en «{t[2]}» (alternativas/correcta/enunciado), se omite")
            continue
        grupos.setdefault(t[0], []).append((k, q, alts, letras, correcta))

    orden = [t for t in titulos if t[0] in grupos]
    numero, bloques, mapa, letras_correctas = 0, [], {}, {}
    for t in orden:
        bloques.append(f'<p class="tema-ia">Tema: <a href="#{t[0]}">{esc(t[2])}</a></p>')
        for _, q, alts, letras, correcta in grupos[t[0]]:
            numero += 1
            mapa.setdefault(t[0], []).append(numero)
            letras_correctas[correcta] = letras_correctas.get(correcta, 0) + 1
            hab = f' <span class="habilidad">{esc(q["habilidad"])}</span>' if q.get("habilidad") else ""
            hab += f' <span class="eje">{esc(q["eje"])}</span>' if q.get("eje") else ""
            items = "".join(f'<li data-letra="{l}">{a}</li>' for l, a in zip(letras, alts))
            distr = q.get("distractores") or {}

            def _texto(d):
                return d.get("texto", "") if isinstance(d, dict) else d

            def _tipo(d):
                return f' <span class="tipo-error">({esc(d["tipo"])})</span>' if isinstance(d, dict) and d.get("tipo") else ""

            extra = "".join(f'<li><strong>{esc(l)})</strong>{_tipo(d)} {_texto(d)}</li>'
                            for l, d in sorted(distr.items()) if l != correcta and _texto(d))
            extra = f"<ul>{extra}</ul>" if extra else ""
            # Respuesta comentada al estilo DEMRE (variante PAES): bloques fijos.
            com = q.get("comentario")
            if isinstance(com, dict) and com.get("desarrollo"):
                partes = []
                for etiqueta, clave in (("Habilidad evaluada", "habilidad_tarea"), ("Concepto del libro", "concepto"),
                                        ("Desarrollo", "desarrollo")):
                    if com.get(clave):
                        partes.append(f"<p><strong>{etiqueta}.</strong> {com[clave]}</p>")
                if extra:
                    partes.append("<p><strong>Por qué fallan las otras alternativas.</strong></p>" + extra)
                if com.get("saber_hacer"):
                    partes.append(f'<p><strong>Qué hay que saber y saber hacer.</strong> {com["saber_hacer"]}</p>')
                cuerpo_resp = f'<div class="comentario">{"".join(partes)}</div>'
            else:
                cuerpo_resp = f'<p>{q.get("explicacion", "")}</p>{extra}'
            bloques.append(
                f'<div class="pregunta" id="pia-{numero}" data-correcta="{correcta}" data-origen="ia">'
                f'<p class="enunciado"><strong>{numero}.</strong><a class="volver-tema" href="#{t[0]}" '
                f'title="Ir a la materia: {esc(t[2])}">↩ Ver tema</a> {q["enunciado"]}{hab}</p>'
                f'<ol class="alternativas">{items}</ol>'
                f'<div class="respuesta"><p><strong>Respuesta correcta: {correcta}</strong></p>'
                f'{cuerpo_resp}'
                f'<p class="aviso-ia">Pregunta creada con IA a partir del contenido de esta sección.</p></div></div>')

    if not numero:
        return cuerpo, toc, {"preguntas_ia": 0}

    # Insignias con los números dentro de cada título
    def poner_insignias(m):
        nivel, atributos, ident, contenido = m.group(1), m.group(2), m.group(3), m.group(4)
        if ident not in mapa:
            return m.group(0)
        chips = "".join(f'<a class="ref-badge ref-ia" href="#pia-{n}" title="Ir a la pregunta {n} de práctica (IA)">{n}</a>'
                        for n in mapa[ident])
        return (f'<h{nivel}{atributos}>{contenido}<span class="ref-badges"><span class="ref-group">'
                f'<span class="ref-label">IA:</span>{chips}</span></span></h{nivel}>')

    cuerpo = re.sub(r'(?is)<h([234])(\b[^>]*\bid="([^"]+)"[^>]*)>(.*?)</h\1>', poner_insignias, cuerpo)

    seccion = (f'<section class="seccion-ia"><h2 id="preguntas-ia">Preguntas de práctica (IA)</h2>'
               f'<div class="nota"><p>Estas {numero} preguntas fueron creadas con inteligencia artificial a partir de los '
               f'contenidos de esta sección; no son del libro. Los números verdes junto a cada título llevan a sus '
               f'preguntas, y el botón «↩ Ver tema» de cada pregunta te devuelve a la materia que la explica.</p></div>'
               + "\n".join(bloques) + "</section>")
    toc = toc + [(2, "preguntas-ia", "Preguntas de práctica (IA)")]
    niveles_revisables = [t for t in titulos if t[0] not in mapa]
    return cuerpo + "\n" + seccion, toc, {
        "preguntas_ia": numero,
        "titulos_con_preguntas": len(mapa),
        "titulos_sin_preguntas": [f"h{t[1]} {t[2]}" for t in niveles_revisables],
        "respuestas_correctas_por_letra": dict(sorted(letras_correctas.items())),
    }


def llenar(plantilla, valores):
    for k, v in valores.items():
        plantilla = plantilla.replace("{{" + k + "}}", v)
    return plantilla


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--secciones", required=True)
    ap.add_argument("--fragmentos", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--pdf", help="PDF original (necesario para recortar figuras)")
    ap.add_argument("--titulo")
    ap.add_argument("--color")
    ap.add_argument("--incrustar", action="store_true", help="imágenes dentro del HTML (base64)")
    ap.add_argument("--marcas", action="store_true", help="mostrar «PDF p. N» donde empieza cada fragmento")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--sin-ajuste", action="store_true", help="no corregir automáticamente los recortes")
    ap.add_argument("--preguntas-ia", help="carpeta con NN.json de preguntas creadas con IA (variante pdf-a-html+ia)")
    ap.add_argument("--sin-portadas", action="store_true", help="tarjetas del índice sin imagen")
    ap.add_argument("--portada-alto", type=float, default=0.34, help="fracción superior de la 1.ª página usada como portada")
    a = ap.parse_args()

    with open(a.secciones, encoding="utf-8") as f:
        conf = json.load(f)
    if isinstance(conf, list):
        conf = {"secciones": conf}
    documento = a.titulo or conf.get("documento") or "Documento"
    acento = a.color or conf.get("color") or "#2563eb"
    secciones = conf["secciones"]
    os.makedirs(a.salida, exist_ok=True)

    with open(os.path.join(ASSETS, "plantilla-seccion.html"), encoding="utf-8") as f:
        p_seccion = f.read()
    with open(os.path.join(ASSETS, "plantilla-indice.html"), encoding="utf-8") as f:
        p_indice = f.read()

    recortador = Recortador(a.pdf, ajustar=not a.sin_ajuste)
    avisos, informe, listas = [], [], []

    for i, sec in enumerate(secciones, start=1):
        archivos = sorted(glob.glob(os.path.join(a.fragmentos, f"{i:02d}-*.html")) +
                          glob.glob(os.path.join(a.fragmentos, f"{i:02d}.html")))
        if not archivos:
            avisos.append(f"Sección {i} «{sec['titulo']}»: sin fragmentos todavía (se omite)")
            continue
        crudo = "\n".join(open(r, encoding="utf-8").read() for r in archivos)
        cubiertas = paginas_cubiertas(crudo)
        faltan = [p for p in range(sec["desde"], sec["hasta"] + 1) if p not in cubiertas] if (cubiertas and "desde" in sec) else None
        cuerpo = limpiar(crudo)
        if a.marcas:
            cuerpo = re.sub(r"<!--\s*pdf:\s*(\d+(?:\s*-\s*\d+)?)\s*-->", r'<div class="marca-pagina">PDF p. \1</div>', cuerpo)
        if not re.search(r"(?i)<h2\b", cuerpo):
            cuerpo = f"<h2>{esc(sec['titulo'])}</h2>\n" + cuerpo
        cuerpo, nfig = procesar_figuras(cuerpo, i, sec, recortador, a.salida, a.incrustar, avisos)
        cuerpo, toc = ids_y_toc(cuerpo)
        stats_ia = {}
        if a.preguntas_ia:
            ruta_ia = os.path.join(a.preguntas_ia, f"{i:02d}.json")
            if os.path.exists(ruta_ia):
                cuerpo, toc, stats_ia = insertar_preguntas_ia(cuerpo, toc, ruta_ia, avisos, i)
            else:
                avisos.append(f"Sección {i}: no hay {ruta_ia} (sin preguntas IA)")
        preguntas = len(re.findall(r'class="pregunta"', cuerpo))
        sin_clave = len(re.findall(r'class="pregunta"[^>]*data-correcta=""', cuerpo)) + \
            len(re.findall(r'data-correcta=""[^>]*class="pregunta"', cuerpo))
        listas.append({**sec, "n": i, "cuerpo": cuerpo, "toc": toc, "preguntas": preguntas})
        informe.append({"seccion": i, "titulo": sec["titulo"], "fragmentos": len(archivos),
                        "paginas_faltantes": faltan, "preguntas": preguntas,
                        "preguntas_sin_clave": sin_clave, "figuras": nfig, **stats_ia})

    if not listas:
        sys.exit("No hay fragmentos para ninguna sección. Revisa --fragmentos y los nombres 01-*.html.")

    varias = len(secciones) > 1  # según el plan, no según cuántas estén listas
    for s in listas:
        s["archivo"] = f"{s['n']:02d}-{slug(s['titulo'], 50)}.html" if varias else f"{slug(documento)}.html"

    comunes = {"DOCUMENTO": esc(documento), "ACENTO": acento, "ACENTO_OSCURO": oscurecer(acento)}
    for k, s in enumerate(listas):
        ant = listas[k - 1] if k > 0 else None
        sig = listas[k + 1] if k + 1 < len(listas) else None
        nav = ""
        if ant or sig:
            nav = '<nav class="navsec">' + (
                f'<a href="{ant["archivo"]}"><small>← Anterior</small>{esc(ant["titulo"])}</a>' if ant else "<span></span>") + (
                f'<a class="sig" href="{sig["archivo"]}"><small>Siguiente →</small>{esc(sig["titulo"])}</a>' if sig else "<span></span>") + "</nav>"
        toc = ""
        if s["toc"]:
            toc = '<nav class="sidebar" aria-label="Contenido"><h2>Contenido</h2><ol>' + "".join(
                f'<li class="n{n}"><a href="#{i}">{esc(t)}</a></li>' for n, i, t in s["toc"]) + "</ol></nav>"
        pagina = llenar(p_seccion, {
            **comunes,
            "TITULO": esc(s["titulo"]),
            "TOC": toc,
            "BOTON_TOC": '<button class="btn-top" id="toc-btn" type="button">☰ Contenido</button>' if s["toc"] else "",
            "BOTON_INDICE": '<a class="btn-top" href="index.html">Índice</a>' if varias else "",
            "NAV": nav,
            "CUERPO": s["cuerpo"],
        })
        with open(os.path.join(a.salida, s["archivo"]), "w", encoding="utf-8") as f:
            f.write(pagina)

    if varias:
        hechas = {s["n"]: s for s in listas}
        piezas = []
        for n, sec in enumerate(secciones, start=1):
            s = hechas.get(n)
            img = ""
            rel = f"assets/portada-{n:02d}.jpg"
            if not a.sin_portadas and "desde" in sec and recortador.portada(sec["desde"], os.path.join(a.salida, rel), a.portada_alto):
                img = rel
                if a.incrustar:
                    ruta = os.path.join(a.salida, rel)
                    with open(ruta, "rb") as f:
                        img = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
                    os.remove(ruta)
            portada = (f'<div class="portada"><img src="{img}" alt="" loading="lazy"><span class="num">{n}</span></div>' if img
                       else f'<div class="portada sin-imagen"><span class="grande">{n}</span><span class="num">{n}</span></div>')
            paginas = sec["hasta"] - sec["desde"] + 1 if "desde" in sec else 1
            rango = f'Págs. {sec["desde"]}–{sec["hasta"]}' if "desde" in sec else esc(sec.get("subtitulo", ""))
            if s:
                preg = f' · {s["preguntas"]} preguntas' if s["preguntas"] else ""
                apertura = (f'<a class="tarjeta" href="{s["archivo"]}" data-archivo="{s["archivo"]}" '
                            f'data-paginas="{paginas}" data-preguntas="{s["preguntas"]}">')
                cierre, estado = "</a>", "Sin empezar"
            else:
                preg = ""
                apertura = f'<div class="tarjeta pendiente" aria-disabled="true" data-paginas="{paginas}" data-preguntas="0">'
                cierre, estado = "</div>", "Pendiente de convertir"
            piezas.append(
                f'{apertura}\n  {portada}\n  <div class="info">\n    <span class="tt">{esc(sec["titulo"])}</span>\n'
                f'    <span class="pp">{rango}{preg}</span>\n'
                f'    <span class="barra"><i></i></span>\n    <span class="res">{estado}</span>\n  </div>\n{cierre}')
        with open(os.path.join(a.salida, "index.html"), "w", encoding="utf-8") as f:
            f.write(llenar(p_indice, {**comunes, "TARJETAS": "\n".join(piezas)}))

    zip_ruta = None
    if a.zip:
        zip_ruta = shutil.make_archive(os.path.abspath(a.salida.rstrip("/\\")), "zip",
                                       root_dir=os.path.dirname(os.path.abspath(a.salida.rstrip("/\\"))),
                                       base_dir=os.path.basename(a.salida.rstrip("/\\")))

    imprimir_json({
        "salida": os.path.abspath(a.salida),
        "principal": "index.html" if varias else listas[0]["archivo"],
        "zip": zip_ruta,
        "secciones": informe,
        "recortes_ajustados": recortador.ajustadas,
        "avisos": avisos,
    })


if __name__ == "__main__":
    main()
