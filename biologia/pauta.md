# Pauta del libro de Biología PAES

Esta pauta fija **cómo se escribe cada capítulo**. Toda sesión de trabajo la sigue.
El objetivo es la **calidad**, no la extensión: no hay límite de páginas.

## 1. Regla de oro: sumar, no reescribir

- Cada capítulo vive en `biologia/capitulos/capNN-slug/`, con **un archivo por sección**.
- Una sesión de trabajo crea o mejora **uno o pocos archivos**. Nunca se regenera un capítulo completo.
- El HTML (`biologia/sitio/`) **no se edita a mano**: se genera con
  `python herramientas/construir.py biologia`.
- Al cerrar la sesión: construir, revisar, commit y push.

## 2. Archivos de un capítulo (orden = nombre del archivo)

| Archivo | Contenido |
|---|---|
| `00-portada.md` | Título (`##`), área temática, frase de apertura y un párrafo de «qué vas a aprender». Mientras el capítulo está incompleto, lleva el recuadro «Capítulo en construcción» con la estructura planificada. |
| `01-conceptos-clave.md` | Lista de conceptos clave, cada uno con una definición precisa de una o dos líneas. |
| `02-….md` a `79-….md` | **Teoría**, un archivo por sección grande (`## 2. Título`), con subsecciones `###` (i, ii, iii… o a, b, c…). |
| `80-ejemplos-paes.md` | Ejemplos resueltos al estilo PAES, desarrollados paso a paso (recuadros `ejemplo`). |
| `90-evaluacion-formativa.md` | 20–30 preguntas de selección múltiple en HTML (`<div class="pregunta">`), con clave y explicación. |
| `99-fuentes.md` | Bibliografía y recursos web usados en el capítulo, con enlace y fecha de consulta. |
| `preguntas.json` | Ítems tipo PAES creados con IA: **3 por título** con materia, formato de `herramientas/references/preguntas-paes.md`. El generador los agrega al final («Preguntas de práctica (IA)») con los números en cada título y el botón «↩ Ver tema». |
| `img/` | Imágenes del capítulo (se enlazan como `img/archivo.png`). |
| `notas/` | Apuntes de investigación. **No se publican.** |

Para intercalar una sección nueva entre dos existentes se usa un número libre (p. ej. `035-…md` va entre `03-…` y `04-…`). Así nunca hay que renombrar.

## 3. Cómo se escribe (Markdown + HTML)

- Títulos: `##` para las secciones del capítulo y `###`/`####` para las subsecciones. Nunca `#`.
- Recuadros:
  ```
  ::: nota          definición, resumen, dato clave
  ::: tip           «ojo», «recuerda», error típico en la PAES
  ::: ejemplo       ejemplo resuelto con su desarrollo
  ```
  y cada uno se cierra con `:::`.
- Tablas en Markdown (`| a | b |`). Fórmulas con `<sub>`, `<sup>` y símbolos (→, ⇌, Δ, °).
- Figuras:
  ```html
  <figure><img src="img/mitosis.svg" alt="Fases de la mitosis"><figcaption>Figura 1. Fases de la mitosis. Fuente: …</figcaption></figure>
  ```
- Preguntas de evaluación formativa: el HTML `pregunta` de `herramientas/references/reglas-html.md`.

## 4. Calidad del contenido

1. **Redacción propia.** Se investiga en varias fuentes y se explica con palabras propias. **No se copian** párrafos de libros ni de sitios web. El repo es público.
2. **Cobertura del temario DEMRE 2027.** Cada conocimiento de `biologia/temario.md` que toca el capítulo debe quedar explicado. Al terminar, se marca en esa tabla.
3. **Fuentes confiables**, en este orden: DEMRE (temarios, modelos de prueba, «Pregunta comentada PAES»), Curriculum Nacional / Mineduc (textos del estudiante y programas de 1.º a 4.º medio), OpenStax *Biology 2e* y *Concepts of Biology*, Khan Academy en español, Educarchile, universidades chilenas y revistas científicas. Toda fuente usada se registra en `99-fuentes.md`.
4. **Explicar para entender**: qué es, cómo funciona, por qué importa y cómo lo pregunta la PAES. Cada sección debe incluir al menos:
   - un esquema, tabla comparativa o figura;
   - un recuadro `tip` con el error típico o la confusión frecuente;
   - su conexión con experimentos, gráficos o datos (habilidades científicas).
5. **Imágenes**: diagramas propios (SVG o generados) o imágenes con licencia libre (Wikimedia Commons, OpenStax CC BY), siempre con autor y licencia en el pie de figura.
6. **Precisión científica**: los datos numéricos y las afirmaciones discutibles se contrastan con al menos dos fuentes.

## 5. Preguntas

- **Ítems IA (`preguntas.json`)**: metodología DEMRE (contexto real, una habilidad focal, 4 alternativas paralelas, distractores con su error nombrado y respuesta comentada de 120–220 palabras). Se validan con
  `python herramientas/construir.py biologia --revisar` hasta que `problemas` quede vacío.
- **Habilidades de Ciencias** y su proporción: Observar y plantear preguntas (10–20 %), Planificar y conducir una investigación (20–40 %), Procesar y analizar la evidencia (30–50 %), Evaluar (20–30 %) y Comunicar.
- Si están disponibles las skills `paes-estudio-demre` o `paes-generador-preguntas`, su metodología manda.

## 6. Flujo de una sesión de capítulo

1. Leer esta pauta, `biologia/temario.md` y la estructura planificada en `00-portada.md`.
2. (Opcional) Consultar el capítulo anterior como guía de estructura: `python herramientas/extraer_referencia.py`. Queda en `biologia/referencia-anterior/`, que no se sube al repo.
3. Investigar en la web y dejar los apuntes en `notas/`.
4. Escribir la(s) sección(es) de la sesión.
5. Construir, revisar el HTML en el navegador y corregir.
6. Actualizar `biologia/progreso.md`, hacer commit y push.
