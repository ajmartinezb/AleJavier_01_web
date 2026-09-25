# Plantilla: sesión para escribir la teoría de un capítulo

Copia este texto en Gemini (CLI o web) y reemplaza lo que está entre llaves `{…}`.

---

Vamos a trabajar el **capítulo {N} de {Física / Biología}: «{título del capítulo}»**.

1. Lee `GEMINI.md`, `{libro}/pauta.md` (y `biologia/pauta.md`, que es la pauta base), `{libro}/temario.md`
   y `{libro}/progreso.md`. Revisa `{libro}/libro.json` para saber la carpeta del capítulo
   (`{libro}/capitulos/{capNN-slug}/`). Si la carpeta no existe o el capítulo no tiene `carpeta` en `libro.json`,
   agrégala.
2. Mira un capítulo ya terminado del mismo libro como modelo de estructura y estilo
   (por ejemplo `fisica/capitulos/cap13-tierra-universo/` o `biologia/capitulos/cap09-evolucion-biodiversidad/`).
3. Propón primero el **plan de secciones**: `## 2.` … `## 9.` con sus subtítulos `### a.`, `### b.`…,
   qué figura lleva cada sección y qué conocimiento del temario cubre. **Espera mi visto bueno.**
4. Luego escribe, un archivo por sección:
   - `00-portada.md`: título `## Capítulo {N}: …`, área temática, apertura, «qué vas a aprender» y el recuadro
     `::: nota` «Este capítulo en la PAES 2027».
   - `01-conceptos-clave.md`: tabla de conceptos con definiciones de una o dos líneas.
   - `02-….md` a `09-….md`: teoría. Cada sección con al menos una tabla o figura, un recuadro `::: tip`
     con el error típico, conexión con datos o experimentos y, si hay cálculos, un `::: ejemplo` resuelto
     (datos → fórmula → reemplazo → resultado con unidad).
   - `80-ejemplos-paes.md`: 4 ejemplos resueltos, uno por habilidad (Observar, Planificar, Procesar, Evaluar).
   - `90-evaluacion-formativa.html`: 20 preguntas en el HTML `<div class="pregunta" data-correcta="…">`
     (ver `herramientas/references/reglas-html.md` o copia el formato de otro capítulo), 5 claves de cada letra.
   - `99-fuentes.md`: todas las fuentes consultadas, con enlace y fecha.
5. Figuras: diagramas SVG propios en `img/` (con `<title>`, textos legibles, unidades en los ejes)
   enlazados con `<figure><img src="img/archivo.svg" alt="…"><figcaption>Figura N. … Diagrama propio.</figcaption></figure>`.
6. Investiga en la web y contrasta cada dato numérico con al menos dos fuentes. Redacción propia: no copies párrafos.
7. Al terminar: `python herramientas/construir.py {libro}`, abre `{libro}/sitio/index.html` en el navegador
   para revisar, y actualiza `{libro}/progreso.md` y `{libro}/temario.md`.

Datos o enfoque propios de este capítulo: {opcional: lo que quieras destacar}.
