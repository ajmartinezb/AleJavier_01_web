"""Lista los títulos de una sección (ya transcrita) con el id que tendrán en la página.

Uso:
  python listar_titulos.py --fragmentos fragmentos --seccion 1

Imprime un JSON con, por título: id (úsalo en el campo "tema" de las preguntas IA),
nivel (2, 3, 4), texto, palabras de contenido propio (hasta el siguiente título) y cuántas
preguntas crear (3 por título con materia; 2 si casi no tiene texto propio; 0 en las
secciones que ya son preguntas del libro y en el título del capítulo).
"""
import argparse
import glob
import html
import os
import re
import sys as _sys

_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import imprimir_json  # noqa: E402
from ensamblar import ids_y_toc, limpiar  # noqa: E402

# Secciones que son preguntas del propio libro (no materia): no llevan preguntas IA.
EXCLUIR = re.compile(r"(?i)^\s*((ejemplos|ejercicios|preguntas|actividades)(\s*\(.*\))?\s*$"
                     r"|(evaluaci[oó]n|autoevaluaci[oó]n|solucionario|respuestas|bibliograf[ií]a|ensayo)\b)")
# Título del capítulo o unidad (primer título): sus temas ya llevan preguntas.
PORTADA = re.compile(r"(?i)^\s*(cap[ií]tulo|unidad|lecci[oó]n|m[oó]dulo)\s+\S+")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fragmentos", required=True)
    ap.add_argument("--seccion", type=int, required=True)
    a = ap.parse_args()

    archivos = sorted(glob.glob(os.path.join(a.fragmentos, f"{a.seccion:02d}-*.html")) +
                      glob.glob(os.path.join(a.fragmentos, f"{a.seccion:02d}.html")))
    if not archivos:
        _sys.exit(f"No hay fragmentos de la sección {a.seccion}")
    cuerpo, _ = ids_y_toc(limpiar("\n".join(open(r, encoding="utf-8").read() for r in archivos)))
    partes = re.split(r'(?is)(<h[234]\b[^>]*\bid="[^"]+"[^>]*>.*?</h[234]>)', cuerpo)
    titulos = []
    for k in range(1, len(partes), 2):
        m = re.match(r'(?is)<h([234])\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h[234]>', partes[k])
        texto = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))).strip()
        contenido = partes[k + 1] if k + 1 < len(partes) else ""
        # Las preguntas del libro no cuentan como materia.
        materia = re.sub(r'(?is)<div class="(pregunta|ejercicio)".*?</div>\s*</div>', " ", contenido)
        palabras = len(re.sub(r"<[^>]+>", " ", materia).split())
        nota = None
        if EXCLUIR.match(texto):
            sugerencia, nota = 0, "preguntas o ejercicios del libro: sin preguntas IA"
        elif PORTADA.match(texto) and not titulos:
            sugerencia, nota = 0, "título del capítulo o unidad: sus temas ya llevan preguntas"
        elif palabras >= 15:
            sugerencia = 3
        else:
            sugerencia, nota = 2, "poco texto propio: 2 preguntas (integradoras si el título agrupa subtítulos)"
        titulos.append({"id": m.group(2), "nivel": int(m.group(1)), "titulo": texto, "palabras": palabras,
                        "preguntas_sugeridas": sugerencia, **({"nota": nota} if nota else {})})
    imprimir_json({"seccion": a.seccion, "titulos": titulos,
                   "total_sugerido": sum(t["preguntas_sugeridas"] for t in titulos)})


if __name__ == "__main__":
    main()
