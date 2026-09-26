---
name: pdf-a-html-ia-paes
description: Variante «pdf-a-html+ia+paes» para libros de preparación PAES (Biología, Física, Química, Historia, Lenguaje, Matemática M1 y M2). Convierte el PDF (con texto o escaneado) en páginas web de estudio divididas por capítulo, unidad, tema, cada N páginas o rangos, y crea para cada título 3 ítems tipo PAES con la metodología oficial DEMRE - contexto real, habilidad oficial declarada, distractores con error identificado y respuesta comentada que enseña. Cada título muestra los números de sus preguntas y cada pregunta vuelve a su materia con «Ver tema». Úsala cuando el libro sea de preparación PAES o el usuario pida preguntas tipo PAES, formato DEMRE, ensayo o facsímil por título.
---

# PDF → HTML + preguntas tipo PAES por título  (pdf-a-html+ia+paes)

Tú eres el motor de conversión: lees las páginas (texto o imagen), escribes fragmentos HTML
según `references/reglas-html.md`, **creas ítems tipo PAES para cada título** según
`references/preguntas-paes.md` (metodología DEMRE), y `scripts/ensamblar.py` arma el sitio con
la plantilla de `assets/`. No hace falta ninguna API externa.

Es la variante para **libros de preparación PAES**. Frente a `pdf-a-html+ia`, aquí cada ítem
tiene contexto real, una habilidad oficial del temario, distractores con su error nombrado y
una respuesta comentada con los bloques del DEMRE (habilidad, concepto del libro, desarrollo,
descarte de cada alternativa y «qué hay que saber y saber hacer»).

Resultado en cada página: cada título lleva los números de sus preguntas (**IA: 12 13 14**,
en verde) que bajan a la sección final «Preguntas de práctica (IA)»; cada pregunta tiene el
botón **«↩ Ver tema»** que sube al título que enseña esa materia (ambos con efecto de carga).

## 0. Qué modo usar

- **Con ejecución de código** (Claude con herramientas de código, Claude Code, ChatGPT con
  análisis de datos / Code Interpreter, agentes de Kimi o GLM con terminal): sigue los pasos 1-6.
  Requiere Python con `pymupdf` (`pip install pymupdf` si falta). Las rutas `scripts/…` y
  `assets/…` son relativas a la carpeta de esta skill. Si no se puede instalar PyMuPDF,
  renderiza las páginas con la librería disponible (pdf2image, pypdfium2) y rellena la
  plantilla tú mismo como en el «Modo solo chat», pero entregando archivos.
- **Sin ejecución de código** (solo chat): ve a la sección «Modo solo chat» al final.

## 1. Preguntar lo mínimo

Si el usuario no lo dijo, pregunta en un solo mensaje (con estos valores por defecto):
- **División:** un solo HTML · por capítulo · por unidad · por tema/lección · cada N páginas · manual.
- **Título del sitio** (por defecto el nombre del PDF) y **color** (por defecto `#2563eb`).
- **Rango** si solo quiere una parte (por defecto todo).

## 2. Inspeccionar el PDF

```bash
python scripts/pdf_info.py libro.pdf
```
Devuelve páginas, `tipo` (`con_texto` / `escaneado` / `mixto`) y marcadores.

## 3. Encontrar las secciones

- **Un solo HTML / cada N páginas / manual:** calcula los rangos directamente.
- **Capítulo / unidad / tema:**
  ```bash
  python scripts/detectar_secciones.py libro.pdf --tipo capitulo   # o unidad, tema, parte
  ```
  Usa marcadores, luego el texto de la parte superior de cada página. Si el PDF es escaneado
  genera `hojas_encabezados/*.png`: mira esas imágenes (cada franja dice «PAGINA DEL PDF N»)
  y anota la primera página de cada capítulo. Otra vía: renderiza las páginas del índice,
  léelas, y corrige el desfase entre la página impresa y la del PDF comprobando una página.
  Los encabezados repetidos suelen aparecer 1-2 páginas después de la portadilla del capítulo:
  revisa la página anterior y empieza la sección en la portadilla si existe.

Escribe `secciones.json` y **muéstraselo al usuario como tabla** (título, desde, hasta, nº de
páginas) antes de convertir un libro largo:
```json
{"documento": "Biología 6ª edición", "color": "#2f855a",
 "secciones": [{"titulo": "Capítulo 1: Método científico", "desde": 16, "hasta": 50}]}
```

## 4. Convertir cada sección

Para cada sección, en grupos de 2-4 páginas:
```bash
python scripts/renderizar_paginas.py libro.pdf --paginas 16-19 --salida paginas --texto
```
Mira cada `paginas/pNNNN.png` (y lee `pNNNN.txt` si trae texto) y escribe el fragmento en
`fragmentos/NN-MMM.html` (NN = número de sección con 2 cifras, MMM = orden de la parte:
`01-001.html`, `01-002.html`…), siguiendo **al pie de la letra** `references/reglas-html.md`.
Cada fragmento empieza con `<!-- pdf: 16-19 -->`.

Libros largos: trabaja sección por sección, dile al usuario el avance («Capítulo 3 listo:
páginas 51-88») y, si el contexto se agota, continúa en el siguiente mensaje: los fragmentos
ya escritos en disco no se repiten.

## 4b. Revisar las figuras (obligatorio antes de ensamblar)

Las imágenes son lo que más se nota. Al terminar cada sección:
```bash
python scripts/revisar_figuras.py libro.pdf --fragmentos fragmentos \
    --secciones secciones.json --seccion 1 --salida revision
```
1. Mira **todas** las hojas `revision/paginas_*.png` (4 páginas por hoja, cada recorte
   dibujado y numerado). Cada foto, dibujo, gráfico, esquema o mapa de la página debe tener
   su rectángulo. Si falta alguno, agrégalo al fragmento en su lugar del texto.
   Si el informe trae `paginas_con_figuras_pdf_sin_marcar`, esas se te escaparon seguro.
2. Mira `revision/recortes_*.png`: cada recorte tal como quedará. Corrige `data-recorte` si
   ves una figura cortada (falta un rótulo, un eje, una parte) o con texto de más (pie
   «Figura N», líneas de un párrafo).
3. Repite hasta que todo esté bien. No entregues con figuras faltantes o mal recortadas.

## 4c. Crear los ítems tipo PAES de la sección

Cuando la sección esté transcrita (y sus figuras revisadas):
```bash
python scripts/listar_titulos.py --fragmentos fragmentos --seccion 1
```
Devuelve cada título con su `id` y `preguntas_sugeridas` (3 por título con materia; 2 si
tiene poco texto; 0 en «Ejemplos», «Evaluación» y el título del capítulo).

Antes de redactar, confirma con el usuario **a qué prueba PAES corresponde el libro**
(Competencia Lectora, M1, M2, Ciencias o Historia) si no es evidente por la portada, y
anótala en el JSON (`"prueba"`). Si en la sesión existe la skill `paes-estudio-demre` o
`paes-generador-preguntas`, léela y aplícala: manda esa metodología.

Relee la materia
de cada título en los fragmentos y escribe `preguntas-ia/01.json` siguiendo **al pie de la
letra** `references/preguntas-paes.md` (campo `tema` = el `id`).

## 4d. Revisar la calidad de los ítems (obligatorio)

```bash
python scripts/revisar_preguntas.py --preguntas preguntas-ia/01.json \
    --fragmentos fragmentos --seccion 1 --paes --prueba ciencias
```
Detecta los defectos que arruinan una pregunta: la clave se adivina por ser la alternativa más
larga, alternativas dispares o repetidas, «todas las anteriores», números desordenados,
enunciados copiados del libro, distractores sin error declarado, claves mal repartidas,
preguntas repetidas, comentarios breves o incompletos y habilidades fuera del rango DEMRE.
**Corrige y repite hasta que `problemas` quede vacío.** Luego revisa a mano las dos preguntas
del DEMRE: ¿se adivina la clave leyendo solo las alternativas?, ¿falla el ítem quien sabe la
materia pero no la habilidad?

## 5. Ensamblar

```bash
python scripts/ensamblar.py --secciones secciones.json --fragmentos fragmentos \
    --preguntas-ia preguntas-ia --salida sitio --pdf libro.pdf --zip
```
Opciones: `--incrustar` (imágenes dentro del HTML, útil para un solo archivo), `--marcas`
(muestra «PDF p. N»), `--titulo`, `--color`, `--sin-portadas` (tarjetas del índice sin la
imagen de la primera página de cada sección), `--portada-alto 0.34` (qué parte superior de
esa página se usa como portada). Lee el informe JSON: si hay
`paginas_faltantes`, conviértelas y vuelve a ensamblar. Revisa también, por sección,
`titulos_sin_preguntas` (agrega las que falten, salvo en ejercicios del libro) y
`respuestas_correctas_por_letra` (si una letra supera ~35%, reordena alternativas). Si hay `preguntas_sin_clave`, busca
el solucionario del libro (suele estar al final) y completa `data-correcta`.

## 6. Entregar

Entrega el ZIP (o la carpeta) e indica qué abrir: `index.html` si hay varias secciones, o el
único `.html`. Resume: secciones, páginas, preguntas del libro, ítems PAES creados, figuras y avisos.

## Qué produce

```
sitio/
  index.html                 portada, progreso total, buscador y tarjetas con imagen
  01-capitulo-1-....html     títulos con «IA: 12 13 14», índice lateral, figuras, «Ver respuesta»,
                             sección final «Preguntas de práctica (IA)» con «↩ Ver tema»,
  02-capitulo-2-....html     contador «X de N respondidas · Y correctas», modo oscuro
  assets/                    figuras recortadas del PDF
```

## Modo solo chat (sin ejecución de código)

1. Pregunta la división (paso 1) y propone la tabla de secciones leyendo el índice del PDF.
2. Convierte **una sección por respuesta**. Toma `assets/plantilla-seccion.html` y reemplaza:
   `{{TITULO}}` y `{{DOCUMENTO}}` (texto), `{{ACENTO}}` (color, ej. `#2563eb`),
   `{{ACENTO_OSCURO}}` (el mismo color más oscuro), `{{CUERPO}}` (el fragmento según las
   reglas), `{{TOC}}` (`<nav class="sidebar" aria-label="Contenido"><h2>Contenido</h2><ol><li class="n2"><a href="#id">Título</a></li>…</ol></nav>`,
   con `id` en cada `<h2>`/`<h3>`), `{{BOTON_TOC}}` (`<button class="btn-top" id="toc-btn" type="button">☰ Contenido</button>`),
   `{{BOTON_INDICE}}` (`<a class="btn-top" href="index.html">Índice</a>` si hay varias secciones)
   y `{{NAV}}` (enlaces anterior/siguiente o vacío). Figuras: sin `data-recorte`, con descripción.
   Ítems PAES: créalos según `references/preguntas-paes.md` y escríbelas en HTML al final del
   cuerpo con el formato del ensamblador: `<section class="seccion-ia">` con
   `<h2 id="preguntas-ia">Preguntas de práctica (IA)</h2>`; cada pregunta
   `<div class="pregunta" id="pia-N" data-correcta="X">` con
   `<a class="volver-tema" href="#id-del-titulo">↩ Ver tema</a>` después del número; y en cada
   título `<span class="ref-badges"><span class="ref-group"><span class="ref-label">IA:</span><a class="ref-badge ref-ia" href="#pia-N">N</a>…</span></span>`.
3. Entrega el HTML completo en un bloque de código con el nombre de archivo sugerido
   (`01-capitulo-1-metodo-cientifico.html`) y pide «continúa» para la siguiente sección.
4. Al final entrega `index.html` con `assets/plantilla-indice.html`.
