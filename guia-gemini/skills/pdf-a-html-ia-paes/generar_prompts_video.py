"""Genera los prompts de «Personaliza la función Resumen de video» de Gemini Notebook (NotebookLM).

Un archivo por título con 3 preguntas IA. Cada archivo trae los dos campos que pide la herramienta:
  1. «Describe un estilo visual personalizado» (tras elegir «Personalizado» en «Elige un estilo visual»)
  2. «Tema personalizado»
Además deja un .zip por capítulo con todos sus prompts.

Uso: python herramientas/generar_prompts_video.py biologia prompts-video/biologia
"""
import collections, json, os, re, sys, unicodedata, zipfile

LIBRO, SALIDA = sys.argv[1], sys.argv[2]

# Estética base de cada capítulo: paleta y motivo gráfico que se repiten en todos sus videos.
ESTETICA = {
    "cap01": ("cuaderno de laboratorio: papel cuadriculado crema, trazos de tinta azul y anotaciones a mano",
              "azul tinta, amarillo resaltador y gris grafito", "matraces, lupas, flechas de un ciclo y tablas de datos dibujadas a mano"),
    "cap02": ("zoom progresivo tipo «potencias de diez», de la molécula a la biósfera, con capas que se abren",
              "verdes y turquesas sobre fondo blanco hueso", "cajas anidadas, escaleras de niveles y siluetas de seres vivos"),
    "cap03": ("infografía molecular limpia con modelos de bolas y varillas en 3D suave",
              "rojo oxígeno, blanco hidrógeno, negro carbono y azul nitrógeno sobre fondo gris claro", "moléculas, gotas de agua y cadenas que se ensamblan como piezas"),
    "cap04": ("ilustración científica en corte transversal, como una ciudad celular vista desde arriba",
              "pasteles translúcidos (lila, verde menta, durazno) con contornos finos", "organelos rotulados, rutas con flechas y lupas de acercamiento"),
    "cap05": ("diagramas anatómicos sobrios y respetuosos, estilo atlas médico moderno, sin realismo explícito",
              "rosados, coral y azul petróleo sobre blanco", "glándulas, ejes con flechas de retroalimentación, calendarios y curvas hormonales"),
    "cap06": ("animación de microscopio de fluorescencia sobre fondo oscuro",
              "cromosomas en magenta y cian, huso en verde neón sobre azul noche", "cromosomas que se duplican, se alinean y se separan, y un reloj circular del ciclo"),
    "cap07": ("estética de laboratorio biotecnológico futurista, interfaz tipo pantalla de datos",
              "azul eléctrico, verde lima y blanco sobre gris grafito", "hélices de ADN, tijeras moleculares, plásmidos y tubos de ensayo"),
    "cap08": ("ilustración tipo cómic científico donde el cuerpo es una fortaleza que se defiende",
              "verdes y violetas para los microbios, dorado y azul para las defensas", "bacterias, virus, murallas, escudos y centinelas"),
    "cap09": ("cuaderno de expedición naturalista del siglo XIX con acuarelas",
              "sepias, verdes selva y ocres sobre papel envejecido", "árboles filogenéticos, mapas de islas, fósiles y picos de pinzones"),
    "cap10": ("infografía ecológica en capas, estilo diorama de papel recortado",
              "amarillo sol, verdes hoja y cafés de suelo", "flechas de energía, pirámides tróficas, ciclos circulares y cadenas alimentarias"),
    "cap11": ("red luminosa de neuronas, estilo visualización de datos sobre fondo oscuro",
              "impulsos en amarillo eléctrico y naranjo sobre azul profundo", "neuronas, sinapsis, cables que conducen chispas y un cerebro por regiones"),
}

def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-")

def plano(md):
    md = re.sub(r"(?m)^:::.*$", "", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"<[^>]+>", "", md)
    return md

def clave(md):
    """Términos en negrita del texto propio del título (sin repetir)."""
    vistos = []
    for t in re.findall(r"\*\*([^*]{2,60})\*\*", md):
        t = t.strip(" .:;,")
        if t and len(t.split()) <= 4 and t.lower() not in [v.lower() for v in vistos] and not re.match(r"(?i)(nota|ojo|importante|ejemplo)", t):
            vistos.append(t)
    return vistos

def ideas(md, n=4):
    """Primeras oraciones con contenido propio, para orientar el guion."""
    txt = plano(md)
    txt = re.sub(r"(?m)^\s*\|.*$", "", txt)
    txt = re.sub(r"(?m)^\s*([-*+]|\d+\.)\s+", "", txt)
    txt = re.sub(r"[*_#>`]", "", txt)
    txt = re.sub(r"(?<=[^.:;!?\s])\n(?=\S)", ". ", txt)
    oraciones = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", txt).strip())
    return [o for o in oraciones if 40 <= len(o) <= 260][:n]

def recorta(t, n):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"

caps = os.path.join(LIBRO, "capitulos")
os.makedirs(SALIDA, exist_ok=True)
indice_general = []
for cap in sorted(os.listdir(caps)):
    ruta = os.path.join(caps, cap)
    if not os.path.isfile(os.path.join(ruta, "preguntas.json")):
        continue
    preg = collections.OrderedDict()
    for p in json.load(open(os.path.join(ruta, "preguntas.json"), encoding="utf-8"))["preguntas"]:
        preg.setdefault(p["tema"], []).append(p)
    portada = open(os.path.join(ruta, "00-portada.md"), encoding="utf-8").read()
    capitulo = re.search(r"(?m)^#+\s+(.+)$", portada).group(1).strip()
    estilo_base, paleta, motivos = ESTETICA[cap[:5]]

    # Títulos (## a ####) con su texto propio y la sección a la que pertenecen.
    titulos = {}
    for f in sorted(os.listdir(ruta)):
        if not re.match(r"[0-7]\d-.*\.md$", f) or f.startswith("00"):
            continue
        partes = re.split(r"(?m)^(#{2,4}) (.+)$", open(os.path.join(ruta, f), encoding="utf-8").read())
        seccion = None
        for i in range(1, len(partes), 3):
            nivel, tit, cuerpo = len(partes[i]), re.sub(r"<[^>]+>", "", partes[i + 1]).strip(), partes[i + 2]
            if nivel == 2:
                seccion = tit
            titulos.setdefault(slug(tit)[:50].rstrip("-"), (tit, None if nivel == 2 else seccion, cuerpo))

    carpeta = os.path.join(SALIDA, cap)
    os.makedirs(carpeta, exist_ok=True)
    filas, n = [], 0
    for tema, ps in preg.items():
        if len(ps) != 3:
            continue
        if tema not in titulos:
            print("  ! sin título para", cap, tema)
            continue
        n += 1
        tit, sec, cuerpo = titulos[tema]
        tit_limpio = re.sub(r"^\s*([0-9]+|[a-z]|[ivx]+)[.)]\s+", "", tit)
        terminos = clave(cuerpo)[:6]
        lineas = ideas(cuerpo)
        elementos = ", ".join(terminos) if terminos else tit_limpio.lower()

        estilo = (f"Estilo {estilo_base}, pensado para el tema «{tit_limpio}». "
                  f"Paleta: {paleta}. Recursos gráficos: {motivos}. "
                  f"Cada escena debe mostrar visualmente {elementos}, con íconos y diagramas simples y rotulados en español. "
                  f"Los términos clave aparecen como etiquetas destacadas la primera vez que se nombran. "
                  f"Las preguntas tipo PAES se muestran como tarjetas con alternativas A, B, C y D, y la correcta se ilumina al revelarla. "
                  f"Tipografía sans serif grande y legible, fondos despejados, sin fotografías reales ni imágenes de libros.")

        bloques = []
        for k, p in enumerate(ps, 1):
            alts = "\n".join(f"{'ABCDE'[j]}) {a}" for j, a in enumerate(p["alternativas"]))
            bloques.append(f"Pregunta {k} ({p['habilidad']}): {p['enunciado']}\n{alts}\n"
                           f"Correcta: {p['correcta']}. Por qué: {recorta(p['comentario']['desarrollo'], 450)}")
        tema_txt = (
            f"Video para estudiantes chilenos que preparan la PAES de Ciencias, eje Biología (temario DEMRE 2027). "
            f"Tema único: «{tit}»" + (f", dentro de la sección «{sec}»" if sec else "") + f" del {capitulo}. "
            f"Céntrate solo en este título y usa solo la información de las fuentes.\n\n"
            + (f"Conceptos que deben quedar claros: {', '.join(terminos)}.\n\n" if terminos else "")
            + ("Ideas guía:\n" + "\n".join(f"- {l}" for l in lineas) + "\n\n" if lineas else "")
            + "Estructura: 1) gancho con una situación cotidiana; 2) idea central en una o dos frases; "
              "3) desarrollo paso a paso con un ejemplo por idea; 4) error típico en la PAES y cómo evitarlo; "
              "5) resolver la Pregunta 1 en pantalla: pausa para pensar, revelar la correcta y explicar por qué fallan los distractores; "
              "6) cierre con tres ideas clave y dejar las Preguntas 2 y 3 como desafío, sin dar su respuesta.\n\n"
            + "\n\n".join(bloques)
            + "\n\nNarración en español de Chile neutro, tono cercano y riguroso.")

        nombre = f"{n:02d}-{slug(tit)[:60].rstrip('-')}.txt"
        doc = (f"{capitulo} · Biología PAES — Ciencias\nVideo {n:02d}: {tit}\n"
               + (f"Sección: {sec}\n" if sec else "")
               + "\nEn Gemini Notebook → Resumen de video → Personalizar:\n"
                 "Elige un estilo visual: Personalizado\n\n"
                 "=== DESCRIBE UN ESTILO VISUAL PERSONALIZADO ===\n" + estilo + "\n\n"
                 "=== TEMA PERSONALIZADO ===\n" + tema_txt + "\n")
        open(os.path.join(carpeta, nombre), "w", encoding="utf-8").write(doc)
        filas.append(f"| {n} | {sec or '—'} | {tit} | `{nombre}` |")

    open(os.path.join(carpeta, "00-indice.md"), "w", encoding="utf-8").write(
        f"# Prompts de video · {capitulo}\n\n{n} títulos con 3 preguntas IA.\n\n"
        "| # | Sección | Título | Archivo |\n|---|---|---|---|\n" + "\n".join(filas) + "\n")
    nombre_zip = os.path.join(SALIDA, f"{cap}.zip")
    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(carpeta)):
            z.write(os.path.join(carpeta, f), os.path.join(cap, f))
    indice_general.append((capitulo, n, cap))
    print(f"{cap}: {n} prompts")
print("Total:", sum(x[1] for x in indice_general))
