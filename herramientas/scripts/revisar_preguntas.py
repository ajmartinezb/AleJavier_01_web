"""Revisa la calidad de las preguntas creadas con IA antes de ensamblar.

Uso:
  python revisar_preguntas.py --preguntas preguntas-ia/01.json [--fragmentos fragmentos --seccion 1] [--paes]

Detecta los defectos que hacen que una pregunta no sirva para estudiar:
  - la clave se adivina por ser la alternativa más larga o más específica;
  - alternativas de largos muy dispares, repetidas o numéricas desordenadas;
  - «todas/ninguna de las anteriores» y dobles negaciones;
  - distractores sin explicación del error;
  - claves mal repartidas (una letra domina) o repetidas dentro de un mismo título;
  - preguntas casi iguales entre sí;
  - enunciados copiados literalmente del libro (se responden reconociendo la frase);
  - con --paes: habilidades fuera del temario oficial, proporciones alejadas del rango
    DEMRE, distractores sin tipo de error declarado y comentarios demasiado breves.

Imprime un JSON con los problemas por pregunta. Corrige el archivo y vuelve a ejecutar
hasta que `problemas` quede vacío.
"""
import argparse
import glob
import html
import json
import os
import re
import statistics
import sys as _sys
import unicodedata

_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import imprimir_json  # noqa: E402

HABILIDADES_PAES = {
    "competencia lectora": {"Localizar": (10, 30), "Interpretar": (30, 60), "Evaluar": (20, 30)},
    "m1": {"Resolver problemas": (30, 60), "Modelar": (5, 25), "Representar": (10, 35), "Argumentar": (5, 15)},
    "m2": {"Resolver problemas": (30, 60), "Modelar": (5, 30), "Representar": (10, 35), "Argumentar": (5, 25)},
    "ciencias": {"Observar y plantear preguntas": (10, 20), "Planificar y conducir una investigación": (20, 40),
                 "Procesar y analizar la evidencia": (30, 50), "Evaluar": (20, 30), "Comunicar": (0, 20)},
    "historia": {"Pensamiento temporal y espacial": (35, 70), "Análisis de fuentes de información": (15, 45),
                 "Pensamiento crítico": (25, 70)},
}
TIPOS_DISTRACTOR = {"verdadero pero irrelevante", "variable equivocada", "sobre-alcance", "sub-alcance",
                    "condición incompleta", "error de cálculo típico", "anacronismo", "atribución cruzada",
                    "relación inversa o inexistente"}
PROHIBIDAS = re.compile(r"(?i)\b(todas|ninguna)\s+(las\s+)?anteriores|\btodas\s+son\s+correctas|\bninguna\s+es\s+correcta")


def limpio(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", str(t or "")))).strip()


def palabras(t):
    t = unicodedata.normalize("NFD", limpio(t).lower()).encode("ascii", "ignore").decode()
    return [p for p in re.findall(r"[a-z0-9]+", t) if len(p) > 2]


def similitud(a, b):
    A, B = set(palabras(a)), set(palabras(b))
    return len(A & B) / max(1, len(A | B))


def es_numero(t):
    """«25 %», «8 litros», «−3,5 °C», «1.200 individuos»: número con o sin unidad."""
    return bool(re.fullmatch(r"[-−]?\s*\$?\s*[\d.,]+\s*[a-zA-Z°%µ/²³.]{0,14}", limpio(t)))


def valor(t):
    n = re.sub(r"[^\d,.-]", "", limpio(t)).replace(".", "").replace(",", ".")
    try:
        return float(n)
    except ValueError:
        return None


def texto_fuente(carpeta, seccion):
    if not carpeta:
        return ""
    archivos = sorted(glob.glob(os.path.join(carpeta, f"{seccion:02d}-*.html")) +
                      glob.glob(os.path.join(carpeta, f"{seccion:02d}.html")))
    crudo = "\n".join(open(r, encoding="utf-8").read() for r in archivos)
    crudo = re.sub(r'(?is)<div class="(pregunta|ejercicio)".*?</div>\s*</div>', " ", crudo)
    return " ".join(palabras(crudo))


def copia_literal(enunciado, fuente, n=9):
    """Devuelve la secuencia de n palabras del enunciado que aparece tal cual en el libro."""
    if not fuente:
        return None
    ps = palabras(enunciado)
    for i in range(len(ps) - n + 1):
        trozo = " ".join(ps[i:i + n])
        if trozo in fuente:
            return trozo
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preguntas", required=True)
    ap.add_argument("--fragmentos", help="para detectar enunciados copiados del libro")
    ap.add_argument("--seccion", type=int, default=1)
    ap.add_argument("--paes", action="store_true", help="exigir además la norma DEMRE")
    ap.add_argument("--prueba", help="competencia lectora | m1 | m2 | ciencias | historia (para --paes)")
    a = ap.parse_args()

    with open(a.preguntas, encoding="utf-8") as f:
        datos = json.load(f)
    preguntas = datos.get("preguntas", []) if isinstance(datos, dict) else datos
    prueba = (a.prueba or (datos.get("prueba") if isinstance(datos, dict) else "") or "").strip().lower()
    fuente = texto_fuente(a.fragmentos, a.seccion)

    problemas, claves, habilidades, por_tema = [], [], [], {}

    def anota(i, q, tipo, detalle):
        problemas.append({"n": i, "tema": q.get("tema"), "problema": tipo, "detalle": detalle,
                          "enunciado": limpio(q.get("enunciado"))[:90]})

    for i, q in enumerate(preguntas, start=1):
        alts = q.get("alternativas") or []
        if isinstance(alts, dict):
            alts = [alts[k] for k in sorted(alts)]
        letras = "ABCDE"[:len(alts)]
        correcta = str(q.get("correcta", "")).strip().upper()[:1]
        claves.append(correcta)
        habilidades.append(q.get("habilidad", ""))
        por_tema.setdefault(q.get("tema"), []).append(correcta)

        if len(alts) < 4:
            anota(i, q, "pocas_alternativas", f"{len(alts)} alternativas (la PAES usa 4, o 5 en M2 y Ciencias)")
        if correcta not in letras:
            anota(i, q, "clave_invalida", f"correcta = «{q.get('correcta')}»")
            continue

        largos = [len(limpio(x)) for x in alts]
        ic = letras.index(correcta)
        otros = [l for k, l in enumerate(largos) if k != ic]
        if largos[ic] > 1.4 * (statistics.mean(otros) or 1) and largos[ic] - max(otros) > 12:
            anota(i, q, "clave_mas_larga", f"la correcta tiene {largos[ic]} caracteres y el resto promedia {round(statistics.mean(otros))}")
        if max(largos) > 3 * max(1, min(largos)):
            anota(i, q, "alternativas_dispares", f"largos {largos}: rompen el paralelismo")
        # En alternativas numéricas se compara el texto tal cual (palabras() descarta los números).
        normalizadas = [limpio(x).lower() if es_numero(x) else " ".join(palabras(x)) for x in alts]
        if len(set(normalizadas)) < len(normalizadas):
            anota(i, q, "alternativas_repetidas", "hay dos alternativas equivalentes")
        for l, x in zip(letras, alts):
            if PROHIBIDAS.search(limpio(x)):
                anota(i, q, "alternativa_prohibida", f"{l}) «todas/ninguna de las anteriores»")
        if all(es_numero(x) for x in alts):
            vals = [valor(x) for x in alts]
            if None not in vals and vals != sorted(vals) and vals != sorted(vals, reverse=True):
                anota(i, q, "numeros_desordenados", f"{vals}: deben ir en orden creciente o decreciente")

        enun = limpio(q.get("enunciado"))
        if len(enun) < 40:
            anota(i, q, "enunciado_corto", f"{len(enun)} caracteres: falta contexto o precisión")
        if re.search(r"(?i)\bno\b.*\bno\b", enun) and re.search(r"(?i)\b(incorrecta|falsa)\b", enun):
            anota(i, q, "doble_negacion", "el enunciado combina negaciones")
        literal = copia_literal(q.get("enunciado"), fuente)
        if literal:
            anota(i, q, "copia_literal_del_libro", f"«{literal}…»: se responde reconociendo la frase, no razonando")

        distr = q.get("distractores") or {}
        faltan = [l for l in letras if l != correcta and not str(distr.get(l, "")).strip()]
        if faltan:
            anota(i, q, "distractor_sin_explicacion", "faltan " + ", ".join(faltan))

        if a.paes:
            com = q.get("comentario") or {}
            if not isinstance(com, dict) or not com.get("desarrollo"):
                anota(i, q, "sin_comentario_demre", "falta el comentario con habilidad, concepto, desarrollo y cierre")
            else:
                texto_com = " ".join(str(v) for v in com.values() if isinstance(v, str))
                n_pal = len(limpio(texto_com).split())
                if n_pal < 110:
                    anota(i, q, "comentario_breve", f"{n_pal} palabras: la respuesta comentada debe enseñar (120-220)")
                for bloque in ("habilidad_tarea", "concepto", "saber_hacer"):
                    if not str(com.get(bloque, "")).strip():
                        anota(i, q, "comentario_incompleto", f"falta el bloque «{bloque}»")
            if not q.get("eje"):
                anota(i, q, "sin_eje", "falta el eje o área temática del temario")
            tipos = {l: str(v.get("tipo", "")).strip().lower() if isinstance(v, dict) else ""
                     for l, v in (q.get("distractores") or {}).items()}
            malos = [l for l, t in tipos.items() if t and t not in TIPOS_DISTRACTOR]
            if malos:
                anota(i, q, "tipo_distractor_desconocido", f"{malos}: usa la tipología de la metodología DEMRE")
            if prueba in HABILIDADES_PAES and q.get("habilidad") not in HABILIDADES_PAES[prueba]:
                anota(i, q, "habilidad_no_oficial", f"«{q.get('habilidad')}» no es habilidad de {prueba}")

    # Repetidas entre sí
    for i in range(len(preguntas)):
        for j in range(i + 1, len(preguntas)):
            if similitud(preguntas[i].get("enunciado"), preguntas[j].get("enunciado")) > 0.6:
                anota(j + 1, preguntas[j], "pregunta_repetida", f"muy parecida a la pregunta {i + 1}")

    # Reparto de claves
    total = len(claves)
    reparto = {l: claves.count(l) for l in sorted(set(claves))}
    for l, n in reparto.items():
        if total >= 12 and n / total > 0.35:
            problemas.append({"problema": "clave_desbalanceada", "detalle": f"la letra {l} es la correcta en {n} de {total} preguntas ({round(100*n/total)}%)"})
    for tema, ls in por_tema.items():
        if len(ls) > 1 and len(set(ls)) == 1:
            problemas.append({"tema": tema, "problema": "misma_clave_en_el_tema", "detalle": f"todas las preguntas de «{tema}» tienen la clave {ls[0]}"})

    salida = {"preguntas": total, "problemas": problemas, "reparto_de_claves": reparto,
              "habilidades": {h: habilidades.count(h) for h in sorted(set(habilidades)) if h}}
    if a.paes and prueba in HABILIDADES_PAES:
        rangos, fuera = HABILIDADES_PAES[prueba], []
        for h, (lo, hi) in rangos.items():
            pct = round(100 * habilidades.count(h) / max(1, total))
            if pct < lo or pct > hi:
                fuera.append({"habilidad": h, "porcentaje": pct, "rango_demre": f"{lo}-{hi}%"})
        salida["habilidades_fuera_de_rango"] = fuera
        if fuera:
            problemas.append({"problema": "proporcion_de_habilidades", "detalle": fuera})
    salida["veredicto"] = "sin problemas detectados" if not problemas else f"{len(problemas)} problema(s): corrige y vuelve a ejecutar"
    imprimir_json(salida)


if __name__ == "__main__":
    main()
