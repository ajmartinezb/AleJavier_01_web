# LÉEME PRIMERO: Libros PAES para Gemini

Este paquete tiene todo el proyecto de los libros PAES de **Biología** y **Física** preparado para
seguir trabajando con **Gemini**. Los documentos vienen en **PDF** y en **TXT** (texto simple), que
Gemini acepta en todas sus versiones. Si tu versión de Gemini acepta uno de los dos, usa ese. No
hace falta subir ambos.

## Qué hay en cada carpeta

| Carpeta o archivo | Para qué sirve |
|---|---|
| `LEEME-PRIMERO` | Este documento |
| `GUIA-COMPLETA` | La guía detallada: preparar el computador, formas de trabajar con Gemini, flujo de una sesión, revisión de calidad y problemas frecuentes |
| `1-SUBIR-A-GEMINI/` | **Los documentos que le das a Gemini** para que trabaje con el mismo método. Son 9, numerados por importancia |
| `2-LIBROS-COMPLETOS/` | El texto completo de los libros de Biología (11 capítulos) y Física (7 capítulos), para que Gemini vea lo que ya está escrito y mantenga el mismo estilo |
| `3-PROYECTO-COMPLETO/` | El proyecto original, con todas sus carpetas: capítulos en Markdown, figuras SVG, preguntas en JSON, el sitio web generado (`index.html`) y los scripts de Python. **Aquí se guarda el trabajo nuevo** |

## Los documentos de `1-SUBIR-A-GEMINI`

| N.º | Documento | ¿Subirlo? |
|---|---|---|
| 01 | Instrucciones del proyecto | **Siempre** |
| 02 | Método para escribir un capítulo | **Siempre** |
| 03 | Metodología DEMRE para preguntas PAES | **Siempre** |
| 04 | Reglas de las preguntas IA y del formato | **Siempre** |
| 05 | Pautas de los libros | **Siempre** |
| 06 | Temarios DEMRE 2027 y progreso | **Siempre** |
| 07 | Plantillas para trabajar con Gemini | Recomendado |
| 08 | Libretos de video de NotebookLM | Solo para hacer videos |
| 09 | Generador de preguntas (referencia) | Opcional |

## Cómo empezar (en 5 pasos)

1. **Descomprime** este zip en una carpeta fija del computador (o dentro de Google Drive para
   escritorio, así queda respaldado solo).
2. **Crea un Gem** en Gemini, por ejemplo «Libros PAES Ciencias»:
   - En **Instrucciones**, pega el texto «Instrucciones para un Gem» del documento 07.
   - En **Conocimiento**, sube los documentos 01 a 06 (en PDF o TXT). Si trabajas un capítulo nuevo
     de Física, sube también `Fisica-PAES-libro-completo`, para que Gemini vea el estilo.
3. **Pide un capítulo** con la plantilla «Sesión de capítulo» del documento 07, por ejemplo:
   «Vamos con el capítulo 12 de Física: Magnetismo y electromagnetismo. Propón el plan de secciones».
4. **Guarda lo que entrega Gemini** dentro de `3-PROYECTO-COMPLETO`, en la carpeta del capítulo
   (por ejemplo `fisica/capitulos/cap12-magnetismo/`). Usa **exactamente** el nombre de archivo que
   indique Gemini, con codificación UTF-8.
5. **Genera el sitio y revisa las preguntas.** Necesitas Python; los pasos están en la guía completa.
   Abre una terminal en `3-PROYECTO-COMPLETO` y ejecuta:
   ```
   pip install -r requirements.txt
   python herramientas/construir.py fisica --revisar
   ```
   Abre `3-PROYECTO-COMPLETO/index.html` en el navegador para ver el resultado.

## Importante

- Los archivos del proyecto (`.md`, `.json`, `.svg`, `.py`) **no se suben a Gemini**: son los que se
  editan y con los que se genera el sitio. A Gemini se le dan los PDF o TXT de las carpetas 1 y 2.
- Gemini en la web no puede ejecutar los scripts ni guardar archivos en tu computador. Si quieres
  que lo haga solo, usa **Gemini CLI** (sección 3 de la guía completa).
- Regla del proyecto: redacción propia, sin copiar textos de libros ni de sitios, y cada fuente
  registrada en `99-fuentes.md` del capítulo.
- Al terminar cada sesión, guarda una copia de la carpeta con la fecha.
