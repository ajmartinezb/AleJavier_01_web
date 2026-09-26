"""Control de equilibrio de un preguntas.json (complementa a `construir.py --revisar`).

Uso (desde la raíz del proyecto):
    python guia-gemini/scripts/reparto_claves.py fisica/capitulos/cap13-tierra-universo/preguntas.json
    python guia-gemini/scripts/reparto_claves.py c13-items-1.json c13-items-2.json   (varios lotes juntos)

Muestra:
  - reparto de claves A, B, C y D (debe ser parejo);
  - posición de largo de la clave: la más larga, la 2.ª, la 3.ª o la más corta
    (la pauta pide entre 22 % y 30 % en cada posición);
  - reparto de habilidades (Observar 10–20 %, Planificar 20–40 %, Procesar 30–50 %, Evaluar 20–30 %);
  - ítems por título (tema) y títulos que repiten la misma clave en todos sus ítems.
"""
import json
import sys
from collections import Counter, defaultdict

RANGOS = {
    "Observar y plantear preguntas": (10, 20),
    "Planificar y conducir una investigación": (20, 40),
    "Procesar y analizar la evidencia": (30, 50),
    "Evaluar": (20, 30),
}
NOMBRES_POS = ["la más larga", "la 2.ª", "la 3.ª", "la más corta"]


def main(rutas):
    items = []
    for r in rutas:
        with open(r, encoding="utf-8") as f:
            items += json.load(f)["preguntas"]
    n = len(items)
    if not n:
        print("No hay preguntas.")
        return
    claves = Counter(p["correcta"] for p in items)
    pos = Counter()
    por_tema = defaultdict(list)
    for p in items:
        largos = [len(a) for a in p["alternativas"]]
        k = "ABCD".index(p["correcta"])
        pos[sorted(largos, reverse=True).index(largos[k])] += 1
        por_tema[p["tema"]].append(p["correcta"])
    hab = Counter(p["habilidad"] for p in items)

    print(f"Preguntas: {n}\n")
    print("Claves:", ", ".join(f"{L} {claves[L]}" for L in "ABCD"))
    print("\nPosición de largo de la clave (objetivo 22–30 % cada una):")
    for i, nombre in enumerate(NOMBRES_POS):
        pc = 100 * pos[i] / n
        marca = "" if 22 <= pc <= 30 else "   <-- fuera de rango"
        print(f"  {nombre:13s} {pos[i]:4d}  ({pc:4.1f} %){marca}")
    print("\nHabilidades:")
    for h, c in hab.most_common():
        pc = 100 * c / n
        lo, hi = RANGOS.get(h, (0, 100))
        marca = "" if lo <= pc <= hi else f"   <-- objetivo {lo}–{hi} %"
        print(f"  {h:42s} {c:4d}  ({pc:4.1f} %){marca}")
    print("\nÍtems por título:")
    for tema, ks in por_tema.items():
        aviso = "   <-- misma clave en todos" if len(ks) > 1 and len(set(ks)) == 1 else ""
        print(f"  {len(ks)}  {tema}  [{' '.join(ks)}]{aviso}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
