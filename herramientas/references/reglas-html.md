# Reglas para transcribir páginas a HTML

Estas reglas definen el **fragmento HTML** de cada grupo de páginas. La plantilla
(`assets/plantilla-seccion.html`) ya trae todo el CSS y el JavaScript: el fragmento solo usa
las etiquetas y clases de abajo, y así las preguntas quedan interactivas y el diseño es uniforme.

## Contenido

- Transcribe **todo** el texto de las páginas con fidelidad: no resumas, no inventes, no omitas.
  Solo une palabras cortadas con guion al final de línea.
- Ignora encabezados y pies de página repetitivos (número de página, nombre del libro,
  «Capítulo 1 | Método científico» arriba de cada página), logotipos y marcas de agua.
- Si una página empieza a mitad de un párrafo o lista de la página anterior, continúa sin repetir el título.
- Si el PDF tiene capa de texto, úsala como fuente del texto exacto y mira la imagen de la
  página para la estructura (títulos, recuadros, tablas, figuras). Si es escaneado, lee la imagen.
- Fórmulas: HTML con `<sub>`, `<sup>` y símbolos (×, ÷, √, π, ≤, ≥, →, ⇌, Δ, °).
  Fracciones: `<span class="frac"><span>numerador</span><span>denominador</span></span>`.

## Primera línea de cada fragmento

```html
<!-- pdf: 17-19 -->
```
Indica qué páginas del PDF contiene el fragmento (numeración del PDF, no la impresa).
`ensamblar.py` la usa para avisar si faltan páginas.

## Estructura (usa SOLO esto)

| Qué es | HTML |
|---|---|
| Título principal (capítulo, unidad, tema grande) | `<h2>` |
| Subtítulo | `<h3>` |
| Sub-subtítulo | `<h4>` (nunca `<h1>`) |
| Texto | `<p>`, `<strong>`, `<em>`, `<ul>`/`<ol>`/`<li>`, `<blockquote>` |
| Tabla | `<table>` con `<thead>` y `<tbody>` |
| Definición, resumen, recuadro informativo | `<div class="nota">…</div>` |
| Consejo, «importante», «recuerda», «ojo» | `<div class="tip">…</div>` |
| Ejemplo resuelto (con su resolución completa) | `<div class="ejemplo">…</div>` |

### Figuras, fotos, gráficos, diagramas, mapas

No las describas en texto largo. Marca su posición para que se recorten del PDF:

```html
<figure data-pagina="18" data-recorte="80,95,920,640">
  <figcaption>Pasos del método científico</figcaption>
</figure>
```

- `data-pagina`: página del PDF donde está la figura.
- `data-recorte="x0,y0,x1,y1"`: rectángulo de la figura en esa página, en coordenadas
  **normalizadas de 0 a 1000** (0,0 = esquina superior izquierda; 1000,1000 = inferior derecha).
- Sin herramientas para recortar (modo solo chat): omite `data-recorte` y escribe en el
  `figcaption` una descripción útil de la figura (qué muestra y sus rótulos).

**Extraer TODAS las figuras.** Toda foto, dibujo, ilustración, gráfico, esquema, mapa
conceptual, diagrama, mapa, logo con contenido o fórmula dibujada lleva su `<figure>`.
Recorre cada página de arriba abajo y de izquierda a derecha antes de pasar a la siguiente.
Excepción: las tablas de datos y las cajas de texto se transcriben como HTML, no como imagen.

**Recortes exactos.**
- Incluye la figura completa: títulos del gráfico, rótulos de ejes (también los verticales),
  leyendas, números de los ejes y flechas con sus textos.
- **No** incluyas el pie «Figura N: …» del libro (va en `<figcaption>`), ni párrafos vecinos,
  ni encabezados de página. Si el pie está pegado a la figura, corta justo antes.
- Si `renderizar_paginas.py` devolvió `figuras_detectadas` (PDF con texto), parte de esas
  coordenadas exactas. Las marcadas `vectorial` a veces son tablas: esas se transcriben.
- `ensamblar.py` afina cada recorte (quita márgenes vacíos y completa bordes cortados), pero
  no adivina: la caja debe estar bien desde el principio.

**Bien ubicadas.**
- La figura va en el punto exacto del texto donde aparece en el libro: después del párrafo
  que la precede y antes del que la sigue. Si está al costado de un párrafo, ponla justo
  después de ese párrafo. Si una pregunta tiene figura, va dentro de `.enunciado`, en su lugar.
- Figuras que en el libro están lado a lado (por ejemplo, dos gráficos A y B) van juntas:
  ```html
  <div class="fila-figuras">
    <figure data-pagina="…" data-recorte="…"><figcaption>Gráfico A</figcaption></figure>
    <figure data-pagina="…" data-recorte="…"><figcaption>Gráfico B</figcaption></figure>
  </div>
  ```
- El tamaño en la web es proporcional al que tiene en el libro: una foto pequeña se ve
  pequeña y un esquema a toda página se ve a todo lo ancho. No hace falta indicarlo.

### Preguntas de selección múltiple (A, B, C, D, E)

```html
<div class="pregunta" data-correcta="B">
  <p class="enunciado"><strong>4.</strong> Enunciado…</p>
  <ol class="alternativas">
    <li data-letra="A">texto</li>
    <li data-letra="B">texto</li>
    <li data-letra="C">texto</li>
    <li data-letra="D">texto</li>
    <li data-letra="E">texto</li>
  </ol>
  <div class="respuesta">
    <p><strong>Respuesta correcta: B</strong></p>
    <p>Por qué B es correcta y por qué las demás no.</p>
  </div>
</div>
```

- `data-correcta`: usa la clave del libro si aparece (a veces está en el solucionario al final:
  búscala). Si no aparece, resuelve tú la pregunta **solo si estás seguro** y agrega dentro de
  `.respuesta` `<p class="aviso-ia">Respuesta propuesta por IA (no aparece en el libro).</p>`.
  Si no puedes resolverla con seguridad: `data-correcta=""` y en `.respuesta` indica que la
  clave no está en estas páginas.
- Si el enunciado trae una figura o tabla, ponla dentro de `.enunciado`.

### Ejercicios y preguntas abiertas

```html
<div class="ejercicio">
  <p>Enunciado…</p>
  <div class="respuesta"><p>Solución del libro…</p></div>
</div>
```
Si el libro no trae la solución, escribe una resolución breve y termina `.respuesta` con
`<p class="aviso-ia">Resolución propuesta por IA.</p>`.

### Solucionarios / tablas de claves sueltas

Transcríbelos como `<table>`. Además, usa esas claves para completar `data-correcta`
de las preguntas correspondientes.

## Prohibido en el fragmento

`<html>`, `<head>`, `<body>`, `<style>`, `<script>`, atributos `on…=`, bloques ```` ``` ````,
y comentarios tuyos antes o después del HTML (salvo la línea `<!-- pdf: … -->`).
