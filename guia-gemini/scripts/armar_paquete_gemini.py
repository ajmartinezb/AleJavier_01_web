"""Arma el paquete para Gemini (documentos consolidados en .txt y .pdf).

Uso: python guia-gemini/scripts/armar_paquete_gemini.py
Requiere Python con markdown y Chrome o Chromium para los PDF (variable CHROMIUM con la ruta del navegador).
El LÉEME se toma de guia-gemini/scripts/leeme.md. La carpeta 3-PROYECTO-COMPLETO se copia a mano."""
import glob, json, os, re, subprocess
import markdown

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(R, "..", "LibrosPAES-Gemini")  # se crea al lado de la carpeta del proyecto
SK = R + "/guia-gemini/skills"


def leer(p):
    return open(os.path.join(R, p) if not p.startswith("/") else p, encoding="utf-8").read()


def sin_frontmatter(txt):
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        return txt
    desc = re.search(r'description:\s*"?(.*?)"?\s*$', m.group(1), re.M)
    cuerpo = txt[m.end():]
    cuerpo = re.sub(r"^<!--.*?-->\s*", "", cuerpo, flags=re.S)
    return (f"> **Para qué sirve:** {desc.group(1)}\n\n" if desc else "") + cuerpo


def doc(titulo, partes):
    s = [f"# {titulo}\n"]
    for sub, txt in partes:
        if sub:
            s.append(f"\n\n---\n\n<!-- {sub} -->\n")
        s.append(txt.strip() + "\n")
    return "\n".join(s)


CSS = """body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:11pt;line-height:1.45;color:#1a202c;margin:0}
h1{font-size:20pt;color:#1c4e80;border-bottom:3px solid #1c4e80;padding-bottom:4px}
h2{font-size:15pt;color:#1c4e80;margin-top:22px}h3{font-size:12.5pt;color:#2b6cb0}
table{border-collapse:collapse;margin:8px 0;font-size:9.5pt;width:100%}th,td{border:1px solid #cbd5e0;padding:4px 6px;vertical-align:top}
th{background:#edf2f7}code{background:#f1f3f5;padding:1px 3px;font-size:9.5pt}pre{background:#f1f3f5;padding:8px;white-space:pre-wrap;font-size:9pt}
blockquote{border-left:4px solid #90cdf4;margin:8px 0;padding:4px 10px;background:#ebf8ff}hr{border:0;border-top:1px solid #cbd5e0;margin:18px 0}
@page{size:A4;margin:16mm 15mm}"""


def escribir(carpeta, nombre, md_txt, pdf=True):
    for sub in ("TXT", "PDF"):
        os.makedirs(os.path.join(OUT, carpeta, sub), exist_ok=True)
    open(os.path.join(OUT, carpeta, "TXT", nombre + ".txt"), "w", encoding="utf-8").write(md_txt)
    base = os.path.join(OUT, carpeta, "PDF", nombre)
    if not pdf:
        return
    txt = re.sub(r"^::: ?(nota|tip|ejemplo)\s*$", lambda m: f"**[{m.group(1).upper()}]**", md_txt, flags=re.M)
    txt = re.sub(r"^:::\s*$", "", txt, flags=re.M)
    txt = re.sub(r"^([A-E]\) .*)$", r"\1  ", txt, flags=re.M)
    html = markdown.markdown(txt, extensions=["tables", "fenced_code"])
    html = re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>', r"<em>[Figura: \1]</em>", html)
    h = f"<!doctype html><html lang='es'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>"
    tmp = base + ".html"
    open(tmp, "w", encoding="utf-8").write(h)
    subprocess.run([os.environ.get("CHROMIUM", "chromium"), "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={base}.pdf", "file://" + tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.remove(tmp)


# 1. Documentos para subir a Gemini -------------------------------------------------
D = "1-SUBIR-A-GEMINI"
docs = [
    ("01-instrucciones-del-proyecto", "Instrucciones del proyecto Libros PAES", [(None, leer("GEMINI.md"))]),
    ("02-metodo-para-escribir-un-capitulo", "Método para escribir un capítulo (Biología y Física)",
     [(None, sin_frontmatter(leer(SK + "/libros-paes-ciencias/SKILL.md")))]),
    ("03-metodologia-DEMRE", "Metodología DEMRE para preguntas PAES",
     [(None, sin_frontmatter(leer(SK + "/paes-estudio-demre/SKILL.md")))]),
    ("04-reglas-de-preguntas-y-formato", "Reglas de las preguntas IA y del formato HTML",
     [("preguntas-paes.md", leer("herramientas/references/preguntas-paes.md")),
      ("reglas-html.md", leer("herramientas/references/reglas-html.md")),
      ("encargo de preguntas por lotes", leer("guia-gemini/plantillas/02-prompt-preguntas-ia.md"))]),
    ("05-pautas-de-los-libros", "Pautas de los libros",
     [("biologia/pauta.md (pauta base de ambos libros)", leer("biologia/pauta.md")),
      ("fisica/pauta.md (diferencias de Física)", leer("fisica/pauta.md"))]),
    ("06-temarios-y-progreso", "Temarios DEMRE 2027 y progreso de los libros",
     [("biologia/temario.md", leer("biologia/temario.md")), ("biologia/progreso.md", leer("biologia/progreso.md")),
      ("fisica/temario.md", leer("fisica/temario.md")), ("fisica/progreso.md", leer("fisica/progreso.md"))]),
    ("07-plantillas-de-sesion", "Plantillas para trabajar con Gemini",
     [("instrucciones para un Gem", leer("guia-gemini/plantillas/00-instrucciones-gem.md")),
      ("sesión de capítulo", leer("guia-gemini/plantillas/01-prompt-sesion-capitulo.md")),
      ("lista de cierre", leer("guia-gemini/plantillas/03-lista-cierre-sesion.md"))]),
    ("08-libretos-de-video-NotebookLM", "Libretos para videos de NotebookLM / Gemini Notebook",
     [(None, sin_frontmatter(leer(SK + "/libreto-video-notebooklm/SKILL.md")))]),
    ("09-generador-de-preguntas-referencia", "Generador de preguntas PAES (referencia de estilo)",
     [(None, "> Parte de las rutas que menciona son de otro proyecto. En este proyecto mandan los documentos 01 a 05.\n\n"
       + sin_frontmatter(leer(SK + "/paes-generador-preguntas/SKILL.md")))]),
]
for nombre, titulo, partes in docs:
    escribir(D, nombre, doc(titulo, partes))

# 2. Libros completos en texto ----------------------------------------------------
D2 = "2-LIBROS-COMPLETOS"
for libro, nom in (("biologia", "Biologia"), ("fisica", "Fisica")):
    lj = json.load(open(f"{R}/{libro}/libro.json", encoding="utf-8"))
    partes = []
    for cap in lj["capitulos"]:
        c = cap.get("carpeta")
        if not c or not os.path.isdir(f"{R}/{libro}/capitulos/{c}"):
            continue
        mds = sorted(glob.glob(f"{R}/{libro}/capitulos/{c}/*.md"))
        if not mds:
            continue
        cuerpo = "\n\n".join(open(m, encoding="utf-8").read() for m in mds)
        partes.append((f"{libro}/capitulos/{c}", cuerpo))
    escribir(D2, f"{nom}-PAES-libro-completo", doc(lj["titulo"], partes))
escribir(".", "GUIA-COMPLETA", leer("guia-gemini/GUIA.md").replace("# Guía para seguir el proyecto en Google Gemini", "# Guía completa para seguir el proyecto en Google Gemini"))
escribir(".", "LEEME-PRIMERO", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "leeme.md"), encoding="utf-8").read())
for sub in ("TXT", "PDF"):
    for f in glob.glob(os.path.join(OUT, sub, "*")):
        os.replace(f, os.path.join(OUT, os.path.basename(f)))
    os.rmdir(os.path.join(OUT, sub))
print("ok")
