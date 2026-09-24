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

- Carpeta **«Biologia»** (sin tilde) del Drive conectado, id `13nsVzi4QJtCB0Ib1IXbdBy-Ab_3ON8bQ`.
- **Sintaxis del conector, verificada el 24-09-2026.** Este conector **no acepta `and`** ni
  títulos con tilde: `title = 'Biología' and mimeType = '...'` devuelve «Operation is not
  implemented, or supported, or enabled». Usar una sola cláusula por consulta:
  ```
  title contains 'Biologia'                     # para encontrar la carpeta
  parentId = '13nsVzi4QJtCB0Ib1IXbdBy-Ab_3ON8bQ'  # para listar su contenido
  ```
  Conviene ir directo al `parentId`, que ya está anotado arriba.
- El libro es ***BIOLOGY — Concepts and Investigations***, 5.ª ed. (Hoefnagels), con un archivo
  por capítulo. **Los `.docx` están casi todos vacíos**: solo los capítulos 1 y 2 tienen texto
  (6 MB); el resto pesa 13 358 bytes y `read_file_content` devuelve una cadena vacía. **El
  contenido real está en los PDF**, de 55 a 85 MB cada uno, uno por capítulo, más el libro
  completo en un solo PDF de 692 MB.
- Capítulos del libro que sirven para el temario PAES: 11 (Tecnología del ADN) → cap. 7 del
  libro propio; 12, 13, 14 y 15 (fuerzas del cambio evolutivo, evidencia de la evolución,
  especiación y extinción, origen e historia de la vida) → cap. 9; 8 y 9 (mitosis, meiosis) →
  cap. 6; 3 (células) → cap. 4; 5 (fotosíntesis) y 6 (respiración) → cap. 10; 26 (sistema
  nervioso) → cap. 11; 28 (sistema endocrino) y 35 (reproducción) → cap. 5; 16, 17 y 34
  (virus, bacterias, sistema inmunológico) → cap. 8.
- Se leen con `mcp__Google_Drive__read_file_content`. Un capítulo son más de 100 000 caracteres
  y excede el límite de una respuesta: el resultado se guarda en un archivo y hay que leerlo por
  trozos, o delegar la lectura a un subagente que devuelva apuntes parafraseados.
- Son **solo fuentes de consulta**: nunca se copian textos ni figuras al repo, que es público.
  Tampoco se publican aquí los enlaces a esos archivos. En `99-fuentes.md` se cita el libro
  (autor, título, edición, capítulo) sin enlace, **y solo si se leyó de verdad**.
