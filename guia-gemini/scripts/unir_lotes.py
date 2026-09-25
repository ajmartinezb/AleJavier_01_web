"""Une varios lotes de ítems IA en el preguntas.json de un capítulo.

Uso (desde la raíz del proyecto):
    python guia-gemini/scripts/unir_lotes.py fisica/capitulos/cap02-sonido notas/items-lote-*.json

- El primer argumento es la carpeta del capítulo.
- Los demás son los lotes (rutas relativas a esa carpeta, se aceptan comodines).
- Los ítems quedan en el orden de los lotes. Si ya existía un preguntas.json, se guarda una
  copia en notas/preguntas-anterior.json antes de reemplazarlo.
"""
import glob
import json
import os
import shutil
import sys

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)
carpeta = sys.argv[1]
rutas = []
for patron in sys.argv[2:]:
    rutas += sorted(glob.glob(os.path.join(carpeta, patron))) or sorted(glob.glob(patron))
if not rutas:
    sys.exit("No encontré lotes con esos nombres.")
items = []
for r in rutas:
    with open(r, encoding="utf-8") as f:
        lote = json.load(f)["preguntas"]
    print(f"{len(lote):4d} ítems  {r}")
    items += lote
destino = os.path.join(carpeta, "preguntas.json")
if os.path.exists(destino):
    os.makedirs(os.path.join(carpeta, "notas"), exist_ok=True)
    shutil.copy(destino, os.path.join(carpeta, "notas", "preguntas-anterior.json"))
with open(destino, "w", encoding="utf-8") as f:
    json.dump({"prueba": "ciencias", "preguntas": items}, f, ensure_ascii=False, indent=1)
print(f"\nTotal: {len(items)} ítems en {destino}")
