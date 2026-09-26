---
name: "libros-paes-ciencias"
description: "Flujo completo para escribir un capítulo de los libros web PAES de Ciencias (Biología y Física, Admisión 2027) del proyecto AleJavier_01_web: investigación, plan, teoría en Markdown con recuadros, figuras SVG propias, ejemplos PAES, evaluación formativa, fuentes, preguntas IA por lotes, validación y cierre. Úsala cuando se pida avanzar, escribir, completar o revisar un capítulo de biologia/ o fisica/ (o empezar Química con la misma estructura)."
---

# Libros PAES de Ciencias: cómo se hace un capítulo

Esta skill resume el método con que se escribieron los 11 capítulos de Biología y los 7 de Física.
Complementa a `paes-estudio-demre` (metodología DEMRE de preguntas) y a `pdf-a-html-ia-paes`
(el generador del sitio, que en el proyecto vive en `herramientas/`).

## 0. Antes de empezar

1. Lee `GEMINI.md` o `CLAUDE.md`, la pauta (`biologia/pauta.md`, y `fisica/pauta.md` si es Física),
   el temario (`<libro>/temario.md`) y el progreso (`<libro>/progreso.md`).
2. Ubica el capítulo en `<libro>/libro.json`. Si no tiene `"carpeta"`, agrégala (`capNN-slug`) con su
   `"area"` y crea `<libro>/capitulos/capNN-slug/img/`.
3. Revisa qué conocimientos del temario 2027 cubre el capítulo. Si el capítulo no está en el temario,
   es de apoyo: dilo en la portada.
4. Un capítulo, o parte de uno, por sesión. Nunca reescribas un capítulo terminado: suma archivos.

## 1. Investigar

- **Libros de consulta** (Drive, carpetas «Biologia» y «Fisica»): lee solo los capítulos pertinentes
  y toma apuntes **parafraseados**. En la primera línea anota qué se leyó de verdad (libro, edición,
  capítulo y secciones).
- **Web**: fuentes oficiales primero (DEMRE, Currículum Nacional, instituciones chilenas, agencias
  científicas, universidades, enciclopedias). Contrasta cada cifra con dos fuentes. Anota la URL y lo
  que confirma. Si no se puede verificar, se dice.
- Busca contexto chileno real (instituciones, datos, casos) para la teoría y para las preguntas.
- Con varios agentes o conversaciones en paralelo, separa la investigación en dos: libros por un
  lado y web por otro.

## 2. Planificar

Propón las secciones `## 2.` a `## 9.` (entre 7 y 10 en total) con sus subtítulos `### a.`, `### b.`…
y, para cada una: qué conocimiento del temario cubre, qué figura lleva y qué cálculo o ejemplo
resuelto tendrá. Espera el visto bueno antes de escribir.

Cuota de preguntas IA que resultará: **2 por título numerado** (incluido «1. Conceptos clave») y **3 por
subtítulo**. Un capítulo típico queda con 90 a 130 preguntas.

## 3. Escribir la teoría (un archivo por sección)

| Archivo | Contenido |
|---|---|
| `00-portada.md` | `## Capítulo N: Título`, `**Área temática:** …`, apertura con gancho chileno, «qué vas a aprender» y `::: nota` «Este capítulo en la PAES 2027» (qué conocimientos cubre y cómo se pregunta) |
| `01-conceptos-clave.md` | `## 1. Conceptos clave` con una tabla Concepto / Definición (una o dos líneas cada una) |
| `02-…md` a `09-…md` | Teoría |
| `80-ejemplos-paes.md` | 4 ítems resueltos paso a paso, uno por habilidad (Evaluar, Procesar, Planificar, Observar), en `::: ejemplo` con Desarrollo, Clave y «Lo que evalúa» |
| `90-evaluacion-formativa.html` | 20 preguntas con `<div class="pregunta" data-correcta="X">`, 5 claves de cada letra (se genera con un script: `assets/ejemplo-evaluacion-cap13.py`) |
| `99-fuentes.md` | Fuentes agrupadas (oficiales, instituciones chilenas, datos científicos, libros de consulta), con fecha de consulta y nota de redacción propia |

Reglas de cada sección de teoría:
- Al menos una **tabla o figura**, un `::: tip` con el error típico o la trampa PAES, y conexión con
  datos, gráficos o experimentos.
- **Física**: magnitudes en SI, coma decimal, espacio entre número y unidad, potencias con `×10<sup>n</sup>`.
  Toda fórmula va con el significado y la unidad de cada símbolo. Si hay cálculos, un `::: ejemplo`
  con datos → fórmula → reemplazo → resultado con unidad.
- Redacción propia en español de Chile: nada copiado de libros ni de sitios. El repositorio es público.
- Conecta con otros capítulos cuando corresponda («como viste en el capítulo 5…»).

## 4. Figuras SVG propias

- Se dibujan con Python usando `assets/svg_base.py`: funciones `t()` (texto), `ln()` (línea),
  `flecha()` y `svg(nombre, ancho, alto, alt, cuerpo)`. Hay un ejemplo completo con 12 figuras en
  `assets/ejemplo-figuras-cap13.py`: órbitas, gráficos con ejes, espectros, líneas de tiempo y fases.
- Escapa `<` y `>` en los textos como `&lt;` y `&gt;`. Pon siempre un `alt` descriptivo y el `<title>`.
- **Míralas renderizadas** antes de darlas por buenas. Por ejemplo, con Chromium en modo headless:
  `chromium --headless --screenshot=f.png --window-size=900,700 file:///ruta/figura.svg`.
  Corrige textos encimados, flechas al revés y rótulos cortados.
- Revisa la física del dibujo: el sentido de la corriente, que los ángulos coincidan con el texto y que
  los datos del gráfico sean coherentes con los del capítulo.
- Enlace: `<figure><img src="img/x.svg" alt="…"><figcaption>Figura N. … Diagrama propio.</figcaption></figure>`.

## 5. Generar y obtener los ids de los títulos

```
python herramientas/construir.py <libro>
python herramientas/scripts/listar_titulos.py --fragmentos <libro>/.construccion/fragmentos --seccion N
```

La segunda orden entrega el `id` exacto de cada título y las preguntas sugeridas. Usa la cuota 2/3 de
arriba. No llevan preguntas la portada, los ejemplos, la evaluación ni las fuentes.

## 6. Preguntas IA por lotes

- Divide los títulos en 4 o 5 lotes de 16 a 22 preguntas. Cada lote se encarga con
  `assets/encargo-preguntas.md`: formato JSON, reglas DEMRE, equilibrios y **notas del capítulo**
  (eje exacto, datos con las mismas cifras de la teoría y errores frecuentes para los distractores).
- Cada lote debe validarse por sí solo con `revisar_preguntas.py` antes de entregarse.
- Une los lotes con `guia-gemini/scripts/unir_lotes.py` (copia en `assets/`) en `preguntas.json`.
- Revisa los cálculos que el lote reporta. Los datos que no estaban en el encargo deben estar
  verificados o sacarse.

## 7. Validar

```
python herramientas/construir.py <libro> --revisar
python guia-gemini/scripts/reparto_claves.py <libro>/capitulos/capNN-slug/preguntas.json   (copia también en assets/)
```

Criterios para cerrar:
- `"problemas": []` y `"veredicto": "sin problemas detectados"`.
- Claves A–D parejas y ningún título con la misma letra en todos sus ítems.
- **Posición de largo de la clave** entre 22 % y 30 % en cada posición (más larga, 2.ª, 3.ª y más corta).
- Habilidades: Observar 10–20 %, Planificar 20–40 %, Procesar 30–50 %, Evaluar 20–30 %.
- Evaluación formativa: 5 claves por letra y la clave no delatada por el largo.

## 8. Cerrar la sesión

1. Abre `<libro>/sitio/index.html` y mira el capítulo: figuras, tablas, recuadros y botones.
2. Actualiza `<libro>/progreso.md` (estado «Preguntas completas», secciones, figuras, número de ítems
   y fecha) y `<libro>/temario.md` (marca como «Completo» cada conocimiento cubierto, con las secciones).
3. Guarda: commit y push si usas Git, o un zip con fecha del proyecto.

## Errores que ya se corrigieron alguna vez (no repetir)

- Claves que eran siempre la alternativa más larga. Hay que acortar la clave o alargar los distractores.
- Alternativas numéricas desordenadas: deben ir en orden creciente o decreciente.
- Datos que cambian con el tiempo, como instituciones renombradas o valores medidos. Se verifican con
  fuentes recientes y se dan como aproximados cuando las fuentes discrepan.
- Afirmar que una observación «prueba» un modelo cuando solo descarta otro. Por ejemplo, las fases de
  Venus refutan a Ptolomeo pero no a Tycho.
- Figuras con rótulos encimados o cortados por no mirarlas renderizadas.
