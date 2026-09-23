#!/usr/bin/env python3
"""Construye el libro web a partir de las carpetas de capítulo (Markdown + HTML).

Uso:
    python herramientas/construir.py biologia            # todo el libro
    python herramientas/construir.py biologia --revisar  # además revisa las preguntas IA

Estructura esperada (ver biologia/pauta.md):
    <libro>/libro.json                      título, color, prueba y lista de capítulos
    <libro>/capitulos/capNN-slug/*.md|*.html  un archivo por sección, en orden alfabético
    <libro>/capitulos/capNN-slug/preguntas.json  ítems tipo PAES (formato de preguntas-paes.md)
    <libro>/capitulos/capNN-slug/img/          imágenes propias del capítulo

Markdown admite recuadros con la sintaxis:
    ::: nota            (también tip, ejemplo)
    texto en **Markdown**
    :::
y HTML en bruto (preguntas <div class="pregunta">, <figure>, tablas complejas).

Genera <libro>/sitio/ (index.html + un HTML por capítulo) usando scripts/ensamblar.py.
Los capítulos sin archivos quedan como «Pendiente» en el índice.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

import markdown

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(AQUI, "scripts")
CAJAS = ("nota", "tip", "ejemplo", "ejercicio")


def md_a_html(texto, cap):
    # ::: nota ... :::  →  <div class="nota" markdown="1"> ... </div>
    def caja(m):
        return f'<div class="{m.group(1)}" markdown="1">\n\n{m.group(2).strip()}\n\n</div>'
    patron = r"(?ms)^:::\s*(" + "|".join(CAJAS) + r")\s*\n(.*?)^:::\s*$"
    while re.search(patron, texto):
        texto = re.sub(patron, caja, texto)
    html = markdown.markdown(texto, extensions=["tables", "md_in_html", "attr_list", "sane_lists"],
                             output_format="html")
    return html


def rutas_img(html, cap):
    # src="img/x.png" → src="img/capNN-slug/x.png" (las imágenes se copian al sitio)
    return re.sub(r'(src\s*=\s*")img/', rf'\1img/{cap}/', html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("libro", help="carpeta del libro, p. ej. biologia")
    ap.add_argument("--revisar", action="store_true", help="ejecuta revisar_preguntas.py por capítulo")
    a = ap.parse_args()

    libro = os.path.abspath(a.libro)
    conf = json.load(open(os.path.join(libro, "libro.json"), encoding="utf-8"))
    tmp = os.path.join(libro, ".construccion")
    salida = os.path.join(libro, "sitio")
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(salida, ignore_errors=True)
    os.makedirs(os.path.join(tmp, "fragmentos"))
    os.makedirs(os.path.join(tmp, "preguntas-ia"))

    secciones = []
    for n, c in enumerate(conf["capitulos"], start=1):
        secciones.append({"titulo": c["titulo"], "subtitulo": c.get("area", "")})
        carpeta = os.path.join(libro, "capitulos", c["carpeta"])
        archivos = sorted(glob.glob(os.path.join(carpeta, "*.md")) + glob.glob(os.path.join(carpeta, "*.html")))
        for k, ruta in enumerate(archivos, start=1):
            texto = open(ruta, encoding="utf-8").read()
            html = md_a_html(texto, c["carpeta"]) if ruta.endswith(".md") else texto
            html = rutas_img(html, c["carpeta"])
            with open(os.path.join(tmp, "fragmentos", f"{n:02d}-{k:03d}.html"), "w", encoding="utf-8") as f:
                f.write(html)
        preg = os.path.join(carpeta, "preguntas.json")
        if os.path.exists(preg):
            shutil.copy(preg, os.path.join(tmp, "preguntas-ia", f"{n:02d}.json"))
        img = os.path.join(carpeta, "img")
        if os.path.isdir(img):
            shutil.copytree(img, os.path.join(salida, "img", c["carpeta"]))

    with open(os.path.join(tmp, "secciones.json"), "w", encoding="utf-8") as f:
        json.dump({"documento": conf["titulo"], "color": conf.get("color", "#2f855a"),
                   "secciones": secciones}, f, ensure_ascii=False, indent=1)

    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "ensamblar.py"),
                        "--secciones", os.path.join(tmp, "secciones.json"),
                        "--fragmentos", os.path.join(tmp, "fragmentos"),
                        "--preguntas-ia", os.path.join(tmp, "preguntas-ia"),
                        "--salida", salida, "--titulo", conf["titulo"],
                        "--color", conf.get("color", "#2f855a"), "--sin-portadas"],
                       capture_output=True, text=True)
    print(r.stdout)
    if r.returncode:
        print(r.stderr, file=sys.stderr)
        sys.exit(r.returncode)

    if a.revisar:
        for pj in sorted(glob.glob(os.path.join(tmp, "preguntas-ia", "*.json"))):
            n = int(os.path.basename(pj)[:2])
            print(f"== Revisión preguntas capítulo {n}")
            subprocess.run([sys.executable, os.path.join(SCRIPTS, "revisar_preguntas.py"),
                            "--preguntas", pj, "--fragmentos", os.path.join(tmp, "fragmentos"),
                            "--seccion", str(n), "--paes", "--prueba", conf.get("prueba", "ciencias")])


if __name__ == "__main__":
    main()
