# Guía para seguir el proyecto en Google Gemini

Esta guía explica qué trae la descarga, cómo preparar el computador y cómo seguir escribiendo los
libros PAES de Biología y Física con Gemini, con el mismo método y la misma calidad que hasta ahora.

---

## 0. Qué trae la descarga

| Carpeta o archivo | Qué es |
|---|---|
| `index.html`, `login.html`, `inicio.html`, `ramo.html`, `assets/` | El portal: portada, ingreso provisorio, asignaturas y capítulos |
| `biologia/` | Libro de Biología: `capitulos/` (lo que se escribe), `sitio/` (el HTML generado), `pauta.md`, `temario.md`, `progreso.md` y `demre/` (PDF oficiales del DEMRE) |
| `fisica/` | Libro de Física, con la misma estructura, más `fisica/pauta.md` (las diferencias propias de Física) |
| `quimica/libro.json` | Solo los títulos de los capítulos de Química, que aún no se desarrolla |
| `herramientas/` | El generador del sitio (`construir.py`), los scripts de revisión y las reglas de preguntas (`references/`) |
| `libretos/`, `prompts-video/`, `videos-gemini/` | Libretos y prompts para los videos resumen de Gemini Notebook (NotebookLM) de Biología |
| `GEMINI.md` | Las instrucciones del proyecto para Gemini (es el `CLAUDE.md` adaptado) |
| `CLAUDE.md` | Las mismas instrucciones, en la versión que usaba Claude. Se deja por si vuelves a usarlo |
| `guia-gemini/` | Esta guía, las **skills** del proyecto (`skills/`, ver su README), plantillas de prompts y dos scripts de apoyo |
| `requirements.txt` | Las librerías de Python que necesita el generador |

El historial de Git **no** viene en el zip, para que la carpeta sea más simple. El historial sigue guardado en GitHub.

---

## 1. Estado actual (25-09-2026)

**Biología:** 11 capítulos terminados, con teoría, figuras, ejemplos, evaluación, fuentes y **1 211 preguntas IA**. Cubre el temario 2027 completo.

**Física:** 7 capítulos terminados, con **763 preguntas IA**. Cubren todo el temario DEMRE 2027 de Física:

| Cap. | Tema | Área 2027 | Preguntas IA |
|---|---|---|---|
| 1 | Ondas | Ondas | 95 |
| 3 | Luz y óptica geométrica | Ondas | 121 |
| 4 | Sismos y dinámica de la Tierra | Energía – Tierra | 103 |
| 5 | Cinemática | Mecánica | 97 |
| 6 | Dinámica: leyes de Newton | Mecánica | 123 |
| 11 | Electricidad y circuitos | Electricidad | 131 |
| 13 | La Tierra y el Universo | Mecánica | 93 |

**Pendiente en Física:** los capítulos de apoyo, que no están en el temario 2027: 2 (sonido), 7 (movimiento circular), 8 (trabajo y energía), 9 (momentum), 10 (calor) y 12 (magnetismo).

**Química:** sin desarrollar; solo tiene la lista de títulos.

El detalle está siempre en `biologia/progreso.md` y `fisica/progreso.md`.

---

## 2. Preparar el computador (una sola vez)

1. **Descomprime** el zip en una carpeta fija, por ejemplo `Documentos\LibrosPAES`.
2. **Instala Python** (versión 3.10 o superior) desde python.org. En Windows, marca la casilla
   **«Add Python to PATH»** durante la instalación.
3. Abre una terminal **dentro de la carpeta del proyecto**. En Windows, abre la carpeta en el
   Explorador, escribe `cmd` en la barra de direcciones y presiona Enter.
4. Instala las librerías:
   ```
   pip install -r requirements.txt
   ```
5. Prueba el generador:
   ```
   python herramientas/construir.py fisica
   python herramientas/construir.py biologia
   ```
   Si termina sin errores, abre `index.html` con doble clic y navega hasta los libros. Todo funciona
   sin internet, directamente desde la carpeta.

---

## 3. Elige cómo trabajar con Gemini

### Opción A (recomendada): Gemini CLI

Gemini CLI es la versión de Gemini que trabaja en la terminal, igual que trabajaba Claude: **lee los
archivos del proyecto, los escribe y ejecuta los scripts de revisión**. Tiene cuota gratuita con
una cuenta de Google. Al abrirlo en la carpeta del proyecto, lee solo el archivo `GEMINI.md`.

1. Instala **Node.js** (versión LTS) desde nodejs.org.
2. En la terminal, instala Gemini CLI:
   ```
   npm install -g @google/gemini-cli
   ```
3. Entra a la carpeta del proyecto y ejecuta `gemini`. La primera vez te pedirá iniciar sesión
   con tu cuenta de Google.
4. Pídele cosas en lenguaje normal, usando las plantillas de la sección 4. Antes de modificar
   archivos o ejecutar comandos, te pedirá permiso.

Los comandos de instalación pueden cambiar con el tiempo. Si alguno falla, revisa las instrucciones
oficiales en el repositorio `google-gemini/gemini-cli` de GitHub.

### Opción B: Gemini en la web (gemini.google.com) con un Gem

Sirve si no quieres usar la terminal, pero es más manual: Gemini **no puede leer ni guardar
archivos en tu computador ni ejecutar los scripts**. Tú copias lo que entrega y corres las revisiones.

1. Crea un **Gem** con las instrucciones y los archivos que indica
   `guia-gemini/plantillas/00-instrucciones-gem.md`.
2. En cada conversación, sube además los archivos del capítulo en que trabajas, y uno terminado
   como modelo.
3. Gemini te entrega cada archivo en un bloque de código. Cópialo en un archivo nuevo con el
   nombre exacto, en la carpeta del capítulo (sirve el Bloc de notas: «Guardar como», codificación
   **UTF-8**, tipo «Todos los archivos»). Un editor como VS Code lo hace más fácil.
4. Corre las revisiones de la sección 5 y pega el resultado en la conversación para que Gemini corrija.

---

## 4. Flujo de una sesión (un capítulo)

1. **Planificar.** Copia `guia-gemini/plantillas/01-prompt-sesion-capitulo.md`, reemplaza lo que está
   entre llaves y envíalo. Gemini debe proponer el plan de secciones y esperar tu visto bueno.
2. **Escribir la teoría.** Portada, conceptos clave, secciones con figuras, ejemplos PAES, evaluación
   formativa y fuentes. Revisa que cada dato numérico venga de una fuente registrada.
3. **Generar el sitio y obtener los títulos:**
   ```
   python herramientas/construir.py fisica
   python herramientas/scripts/listar_titulos.py --fragmentos fisica/.construccion/fragmentos --seccion 2
   ```
   El segundo comando lista el **id exacto** de cada título del capítulo 2 y cuántas preguntas le
   corresponden: 2 por título numerado y 3 por subtítulo. No llevan preguntas la portada, los ejemplos,
   la evaluación ni las fuentes.
4. **Preguntas IA por lotes.** Divide los títulos en 4 o 5 lotes de unas 20 preguntas y usa
   `guia-gemini/plantillas/02-prompt-preguntas-ia.md` para cada lote. Completa las «notas para este
   capítulo»: eje, datos y errores frecuentes. Cada lote se guarda en `notas/items-lote-N.json` dentro
   de la carpeta del capítulo. Pedir las 90 o 100 preguntas de una vez baja mucho la calidad.
5. **Unir los lotes:**
   ```
   python guia-gemini/scripts/unir_lotes.py fisica/capitulos/cap02-sonido notas/items-lote-*.json
   ```
6. **Revisar** (sección 5) y corregir hasta que no queden problemas.
7. **Cerrar** con `guia-gemini/plantillas/03-lista-cierre-sesion.md`: actualiza `progreso.md` y
   `temario.md`, abre el sitio para mirarlo y guarda una copia (sección 7).

---

## 5. Revisar la calidad (siempre)

```
python herramientas/construir.py fisica --revisar
python guia-gemini/scripts/reparto_claves.py fisica/capitulos/cap02-sonido/preguntas.json
```

- `--revisar` muestra por capítulo los **problemas** de cada pregunta. Por ejemplo: la clave es
  demasiado larga, falta un tipo de distractor, el comentario es muy corto o muy largo, hay frases
  copiadas del libro o un `tema` no coincide con ningún título. Tiene que terminar en
  `"problemas": []`.
- `reparto_claves.py` revisa lo que la pauta pide en conjunto:
  - claves A–D parejas;
  - la posición de largo de la clave (la más larga, la 2.ª, la 3.ª o la más corta) entre 22 % y 30 %
    cada una, para que el largo no delate la respuesta;
  - las proporciones de habilidades.

Si algo sale fuera de rango, pega la salida en Gemini y pídele que corrija **solo** esas preguntas.

---

## 6. Libros de consulta (Google Drive)

- Las carpetas «Biologia» y «Fisica» del Drive siguen siendo solo fuentes de consulta.
  - En Física, los PDF por capítulo de Giancoli, Etkina, *Advanced Physics for You* y Shipman tienen texto.
  - En Biología, solo los `.docx` de los capítulos 1 y 2 tienen contenido.
  - El detalle está en `GEMINI.md`.
- Con Gemini puedes **subir directamente el PDF de un capítulo** a la conversación. Gemini lee
  PDF, incluso escaneados, así que quizás logres leer algunos que el conector de Claude no podía.
  Hay límites de tamaño: el libro completo de 692 MB no se puede subir. Súbelo por capítulos.
- Las reglas no cambian: no se copian textos ni figuras de esos libros, no se publican sus enlaces,
  y en `99-fuentes.md` se cita el libro (autor, título, edición y capítulo) solo si se leyó de verdad.

---

## 7. Guardar el trabajo

Sin GitHub, lo más seguro es:

- Al terminar cada sesión, **comprime la carpeta** y guarda el zip con la fecha, por ejemplo
  `LibrosPAES-2026-10-02.zip`, en Google Drive. Si algo se estropea, vuelves a la última copia.
- Si más adelante quieres volver a subir los cambios a GitHub, la forma más simple es **GitHub Desktop**:
  clonas `ajmartinezb/AleJavier_01_web`, copias encima tus carpetas actualizadas y haces «Commit» y
  «Push».

---

## 8. Próximos pasos sugeridos

1. **Física, capítulos de apoyo** (fuera del temario 2027), en este orden: 12 magnetismo, 8 energía,
   2 sonido, 10 calor, 9 momentum y 7 movimiento circular. Úsalos para profundizar, con menos
   preguntas si quieres.
2. **Química:** crear `quimica/pauta.md` y `quimica/temario.md` con el temario DEMRE 2027 (está en
   `biologia/demre/`, en las páginas de Química), igual que se hizo con Física, y luego escribir
   capítulo por capítulo.
3. **Videos:** continuar los libretos de Gemini Notebook para Física, siguiendo lo hecho en
   `libretos/` y `prompts-video/` para Biología.

---

## 9. Problemas frecuentes

| Problema | Solución |
|---|---|
| `python` no se reconoce | Reinstala Python marcando «Add Python to PATH», o usa `py` en vez de `python` |
| `ModuleNotFoundError: markdown` (u otra librería) | `pip install -r requirements.txt` |
| Las tildes se ven como `Ã©` | El archivo no se guardó en UTF-8. Vuelve a guardarlo con codificación UTF-8 |
| El capítulo no aparece en el sitio | Revisa que en `libro.json` el capítulo tenga su `"carpeta"` y que la carpeta exista |
| `--revisar` dice que un `tema` no existe | El id debe ser exactamente el que da `listar_titulos.py`. Si cambiaste un título, cambia el id en las preguntas |
| Una figura no se ve | La ruta debe ser `img/archivo.svg`, relativa a la carpeta del capítulo, y el SVG debe abrir en el navegador |
| Gemini copia frases del capítulo en las preguntas | `--revisar` lo detecta. Pídele que reformule esos enunciados con palabras propias |
