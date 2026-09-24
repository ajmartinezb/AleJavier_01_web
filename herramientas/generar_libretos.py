"""Genera un prompt de libreto (video de Gemini Notebook) por cada título de un capítulo.

Uso: python herramientas/generar_libretos.py <carpeta_capitulo> <carpeta_salida> ["Capítulo N: Nombre"]
La carpeta del capítulo trae los NN-*.md de materia y preguntas.json (del libro de Biología).
"""
import json, os, re, sys, unicodedata

def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-")

def limpiar(md):
    md = re.sub(r"(?m)^::: ?(\w+)\s*$", lambda m: f"**[{m.group(1).capitalize()}]**", md)
    md = re.sub(r"(?m)^:::\s*$", "", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    return re.sub(r"\n{3,}", "\n\n", md).strip()

cap, salida = sys.argv[1], sys.argv[2]
preg = {}
for p in json.load(open(os.path.join(cap, "preguntas.json"), encoding="utf-8"))["preguntas"]:
    preg.setdefault(p["tema"], []).append(p)
portada = open(os.path.join(cap, "00-portada.md"), encoding="utf-8").read()
m = re.search(r"(?m)^#\s+(.+)$", portada)
capitulo = sys.argv[3] if len(sys.argv) > 3 else (m.group(1).strip() if m else os.path.basename(cap))

titulos = []  # (nivel, titulo, seccion, texto propio, texto completo de la sección)
for f in sorted(os.listdir(cap)):
    if not re.match(r"0[1-9]-.*\.md$", f):
        continue
    md = open(os.path.join(cap, f), encoding="utf-8").read()
    partes = re.split(r"(?m)^(#{2,3}) (.+)$", md)
    seccion = None
    for i in range(1, len(partes), 3):
        nivel, tit, cuerpo = len(partes[i]), partes[i + 1].strip(), partes[i + 2]
        if nivel == 2:
            seccion = tit
        titulos.append((nivel, tit, seccion if nivel == 3 else None, limpiar(cuerpo)))

os.makedirs(salida, exist_ok=True)
indice = []
for n, (nivel, tit, sec, texto) in enumerate(titulos, 1):
    ps = preg.get(slug(tit)[:50].rstrip("-"), [])
    tipo = ("**Video panorámico de la sección.** Presenta la idea general y anuncia los subtemas "
            "que vienen, sin desarrollarlos a fondo (cada uno tiene su propio video).") if nivel == 2 else \
           "**Video de un solo subtema.** Profundiza solo en este título; no expliques otros subtemas de la sección."
    if nivel == 2 and slug(tit).startswith("1-conceptos"):
        tipo = "**Video de vocabulario.** Recorre los conceptos clave del capítulo con un ejemplo cotidiano breve para cada uno."
    bloque_p = ""
    for k, p in enumerate(ps, 1):
        alts = "\n".join(f"   {'ABCDE'[j]}) {a}" for j, a in enumerate(p["alternativas"]))
        c = p["comentario"]
        bloque_p += (f"\n**Pregunta {k}** · Habilidad: {p['habilidad']}\n\n{p['enunciado']}\n\n{alts}\n\n"
                     f"   Correcta: **{p['correcta']}**. {c['desarrollo']}\n")
    contexto = f"Sección: **{sec}**\n" if sec else ""
    doc = f"""# Libreto {n:02d} · {tit}

*{capitulo} · Biología PAES — Ciencias*
{contexto}
> **Cómo usarlo:** en Gemini Notebook (NotebookLM) sube como fuente el capítulo completo, pega todo el bloque de abajo en «Personalizar» del resumen en video (o en el chat si quieres primero el libreto escrito) y genera. Un video por archivo.

---

## ROL Y PÚBLICO

Actúa como profesor de Biología chileno que prepara a estudiantes de 3.° y 4.° medio para la **PAES de Ciencias (eje Biología)**, según el temario DEMRE. Hablas claro, cercano y riguroso, en español de Chile neutro, sin modismos forzados.

## TEMA DEL VIDEO

**{tit}**{f" (dentro de «{sec}»)" if sec else ""}

{tipo}

## CONTENIDO BASE (usa solo esto; no agregues datos, cifras ni citas que no estén aquí)

{texto if texto else "_Este título es solo el encabezado de la sección: presenta la idea general a partir de sus subtítulos._"}

## ESTRUCTURA DEL LIBRETO (5 a 7 minutos)

1. **Gancho (20-30 s):** una pregunta o situación cotidiana que despierte curiosidad sobre el tema.
2. **Idea central:** define el concepto en una o dos frases simples.
3. **Desarrollo:** explica el contenido base paso a paso, con un ejemplo concreto por idea. Si hay tablas, conviértelas en comparaciones habladas.
4. **Error típico en la PAES:** la confusión más frecuente sobre este tema y cómo evitarla.
5. **Pregunta tipo PAES:** plantea la pregunta 1 de abajo, da unos segundos para pensar, y luego explica por qué la correcta lo es y por qué fallan los distractores.
6. **Cierre (30 s):** resumen en tres ideas y una frase que conecte con el siguiente tema.

## PREGUNTAS DE ESTE TÍTULO
{bloque_p or chr(10) + "_Sin preguntas asociadas: inventa una sola pregunta original tipo PAES de 4 alternativas sobre el contenido base._"}
Usa la pregunta 1 dentro del video; las preguntas 2 y 3 menciónalas al final como «desafío para practicar», sin dar la respuesta.

## REGLAS

- Nada de contenido fuera del tema del video ni fuera del contenido base.
- Destaca los términos clave la primera vez que aparecen.
- Visuales: diagramas simples, tablas limpias y ejemplos ilustrados; nada de imágenes copiadas de libros.
- Idioma: todo en español.
"""
    nombre = f"{n:02d}-{slug(tit)[:60].rstrip('-')}.md"
    open(os.path.join(salida, nombre), "w", encoding="utf-8").write(doc)
    indice.append(f"| {n} | {sec or '—'} | [{tit}]({nombre}) | {len(ps)} |")

open(os.path.join(salida, "README.md"), "w", encoding="utf-8").write(
    f"# Libretos · {capitulo}\n\nUn prompt por video de Gemini Notebook ({len(titulos)} en total).\n\n"
    "| # | Sección | Libreto | Preguntas |\n|---|---|---|---|\n" + "\n".join(indice) + "\n")
print(len(titulos), "libretos")
