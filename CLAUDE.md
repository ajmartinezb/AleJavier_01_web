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

- Carpeta **«Biología»** del Drive conectado (compartida desde la cuenta ajmartinezb2). Se busca con `mcp__Google_Drive__search_files` usando `parentId = '<id de la carpeta>'`; el id se obtiene buscando `title = 'Biología' and mimeType = 'application/vnd.google-apps.folder'`.
- Lo más útil: *Understanding Biology* (Mason y Duncan, 2.ª ed.), dividido en un PDF por capítulo; *Principles of Biology* (Brooker), transcrito en un .docx por capítulo; y los textos del estudiante del Mineduc (Biología de 1.º y 2.º medio, Ciencias de 7.º y 8.º, y Ciencias para la Ciudadanía de 3.º y 4.º medio).
- Se leen con `mcp__Google_Drive__read_file_content`. Un capítulo son unos 80 000 caracteres, así que conviene delegar la lectura a un subagente que devuelva apuntes parafraseados.
- Son **solo fuentes de consulta**: nunca se copian textos ni figuras al repo, que es público. Tampoco se publican aquí los enlaces a esos archivos. En `99-fuentes.md` se cita el libro (autor, título, edición, capítulo) sin enlace.
