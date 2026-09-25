# AleJavier_01_web — Libros PAES en la nube

## Libro de Biología (`biologia/`)

- **Antes de trabajar, lee `biologia/pauta.md`.** Ahí están la estructura de cada capítulo, las reglas de calidad y el flujo de trabajo de una sesión.
- Se trabaja **un capítulo, o una parte de un capítulo, por sesión**, sumando archivos de sección. Nunca se reescribe un capítulo completo.
- La materia se escribe en Markdown (y HTML para las preguntas) en `biologia/capitulos/capNN-*/`.
- El HTML publicado (`biologia/sitio/`) se genera con:
  ```bash
  pip install -r requirements.txt
  python herramientas/construir.py biologia            # generar
  python herramientas/construir.py biologia --revisar  # generar y revisar las preguntas IA
  ```
  `biologia/sitio/` no se edita a mano.
- Investigación en la web obligatoria. Toda fuente usada se registra en `99-fuentes.md` del capítulo. Redacción propia: no se copian textos (el repo es público).
- `biologia/temario.md` es el temario DEMRE 2027 con el control de cobertura; `biologia/progreso.md` es el estado de cada capítulo. Ambos se actualizan al cerrar cada sesión.
- `herramientas/` viene de la skill `pdf-a-html-ia-paes` (repo `ajmartinezb/pdf-a-html`). Las reglas de preguntas están en `herramientas/references/preguntas-paes.md`.
- Referencia opcional: el libro anterior (repo privado `ajmartinezb/escritorio-19`, `public/Biologia/`) se extrae con `herramientas/extraer_referencia.py` a `biologia/referencia-anterior/`. Esa carpeta está en .gitignore y **nunca se sube**: es una transcripción de un libro con derechos de autor.

## Libros de consulta (Google Drive)

**Estado real, verificado el 24-09-2026: la carpeta hoy es casi inservible como fuente.**
Antes de planificar una sesión contando con ella, lee esto.

- Carpeta **«Biologia»** (sin tilde) del Drive conectado, id `13nsVzi4QJtCB0Ib1IXbdBy-Ab_3ON8bQ`.
  Contiene *BIOLOGY — Concepts and Investigations*, 5.ª ed. (Hoefnagels), con un `.docx` y un
  `.pdf` por capítulo, más el libro completo en un PDF de 692 MB.
- **Sintaxis del conector.** No acepta `and` ni títulos con tilde: `title = 'Biología' and
  mimeType = '...'` devuelve «Operation is not implemented, or supported, or enabled». Va una
  sola cláusula por consulta: `title contains 'Biologia'`, o directamente
  `parentId = '13nsVzi4QJtCB0Ib1IXbdBy-Ab_3ON8bQ'`.
- **Qué se puede leer y qué no:**

  | Archivo | Estado |
  |---|---|
  | `.docx` de los capítulos 1 y 2 | **Legibles.** Transcripción completa, unos 6 MB y 118 000 caracteres cada uno |
  | `.docx` del capítulo 3 | Transcripción empezada: devuelve solo dos líneas |
  | `.docx` de los capítulos 4 a 40 | **Vacíos.** Todos pesan exactamente 13 358 bytes y `read_file_content` devuelve `""` |
  | `.pdf` de cualquier capítulo | **Ilegibles por el conector.** Son escaneos sin capa de texto: `read_file_content` devuelve `""`, y `download_file_content` los rechaza por superar su límite de 10 MB |

- En la práctica, entonces, **solo los capítulos 1 y 2 sirven como fuente de consulta**. Para
  cualquier otro tema hay que transcribir antes el PDF al `.docx` correspondiente, como ya se
  hizo con esos dos, o investigar en la web.
- Cuando un `.docx` sí tenga contenido, son más de 100 000 caracteres y exceden el límite de una
  respuesta: el resultado se guarda en un archivo y hay que leerlo por trozos con jq o python, o
  delegar la lectura a un subagente que devuelva apuntes parafraseados.
- Son **solo fuentes de consulta**: nunca se copian textos ni figuras al repo, que es público.
  Tampoco se publican aquí los enlaces a esos archivos. En `99-fuentes.md` se cita el libro
  (autor, título, edición, capítulo) sin enlace, **y solo si se leyó de verdad**.

## Libro de Física (`fisica/`)

- Misma estructura, herramientas y reglas que Biología. **Lee `fisica/pauta.md`** (diferencias propias de Física) y
  `fisica/temario.md` (temario DEMRE 2027 de Física, págs. 9–11 del PDF de `biologia/demre/`, con la cobertura por capítulo).
- Generar: `python herramientas/construir.py fisica` (`--revisar` para las preguntas IA). `fisica/sitio/` no se edita a mano.
- Estado de cada capítulo en `fisica/progreso.md`.
- **Temario 2027:** el área Ondas se centra en ondas electromagnéticas. Los capítulos 2 (sonido), 7 (MCU), 8 (trabajo y
  energía), 9 (momentum), 10 (calor) y 12 (magnetismo) de `libro.json` **no están en el temario 2027**: son de apoyo.
- **Libros de consulta en Drive** (carpeta «Fisica», id `1C5tCYI4jgcfAAtW8ELr1J7lPRCMwpPPd`, compartida desde otra cuenta),
  verificado el 25-09-2026: los PDF por capítulo de Giancoli (7.ª ed.), Etkina, *Advanced Physics for You* y Shipman
  **tienen capa de texto y se leen** con `read_file_content` (100 000+ caracteres: guardar y leer por trozos o delegar a
  un subagente). Los PDF completos `Fisica-I°-y-II°.pdf` y `Fisica-II°.pdf` son escaneos **ilegibles** por el conector.
  Mismas reglas que Biología: solo consulta, sin copiar texto ni figuras y sin publicar enlaces.

## Portal (raíz del repo)

- `index.html` (landing) → `login.html` (provisorio) → `inicio.html` (asignaturas PAES) → `ramo.html?id=…` (capítulos).
- Asignaturas y capítulos en `assets/data.js`. Biología enlaza a `biologia/sitio/index.html` y Física a `fisica/sitio/index.html`.
- `quimica/libro.json`: solo títulos de capítulos, aún sin desarrollar.
