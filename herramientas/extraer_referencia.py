#!/usr/bin/env python3
"""Extrae el texto de los capítulos de Biología del proyecto anterior (repo privado escritorio-19)
a Markdown, en biologia/referencia-anterior/ (carpeta ignorada por git: no se publica).

Uso:
    git clone --depth 1 https://github.com/ajmartinezb/escritorio-19 /home/user/escritorio-19
    python herramientas/extraer_referencia.py [/home/user/escritorio-19]
"""
import glob
import os
import re
import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as md

origen = os.path.join(sys.argv[1] if len(sys.argv) > 1 else "/home/user/escritorio-19", "public", "Biologia")
destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biologia", "referencia-anterior")
os.makedirs(destino, exist_ok=True)
for ruta in sorted(glob.glob(os.path.join(origen, "capitulo*.html"))):
    soup = BeautifulSoup(open(ruta, encoding="utf-8").read(), "html.parser")
    for t in soup(["script", "style", "nav", "svg"]):
        t.decompose()
    for im in soup.find_all("img"):
        im.replace_with(f"[imagen: {im.get('alt', '')}]")
    texto = re.sub(r"\n{3,}", "\n\n", md(str(soup.body or soup), heading_style="ATX"))
    n = int(re.search(r"capitulo(\d+)", ruta).group(1))
    nombre = f"cap{n:02d}-" + os.path.basename(ruta).split("-", 1)[1].replace(".html", ".md")
    open(os.path.join(destino, nombre), "w", encoding="utf-8").write(texto)
    print(nombre)
