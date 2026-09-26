---
name: "paes-generador-preguntas"
description: "Genera preguntas tipo PAES (con su respuesta comentada) para el proyecto \"Pregunta comentada PAES, búsqueda en la web\", cuando el usuario indica un ramo (asignatura) y uno o varios capítulos y pide crear, generar, completar o rellenar preguntas/ítems. Ejemplos de disparo: \"hazme preguntas de Matemática M1 capítulo 7\", \"completa el capítulo 3 de Biología\", \"genera el capítulo 5 de Historia\", \"rellena Lenguaje - Localizar información\". Requiere/complementa el skill paes-estudio-demre (metodología DEMRE); si no está disponible, aplica igual las reglas descritas aquí."
---


# Generador de preguntas PAES por ramo y capítulo

Skill "operador": el usuario dice **ramo + capítulo(s)** y tú generas los archivos de preguntas comentadas siguiendo exactamente la estructura de carpetas y el formato ya usados en el proyecto "Pregunta comentada PAES, búsqueda en la web". Si el skill `paes-estudio-demre` está disponible en la sesión, invócalo primero (o lee su SKILL.md) — contiene la metodología DEMRE completa (estructura D→E→F, tipología de distractores, habilidades oficiales) que este skill da por conocida y no repite en detalle.

## 0. Qué preguntar si falta información

Antes de generar, confirma solo lo que sea ambiguo (una pregunta, no un formulario):
- **Ramo**: si no queda claro a cuál de las 5 asignaturas se refiere, pregunta. Ver tabla §1.
- **Capítulo(s)**: número, rango ("del 3 al 6"), nombre parcial, o "todos los que falten". Si dice solo el nombre del tema, ubícalo en la tabla de capítulos de esa asignatura (§1) o listando la carpeta.
- **Cantidad**: si el usuario no dice cuántas preguntas, usa la cuota por defecto (§3) y dilo explícitamente en tu resumen final ("generé 24 por nivel, el estándar del proyecto; dime si quieres otra cantidad").
- **Nivel**: si no especifica, genera principiante + intermedio + avanzado. Si pide "solo avanzado" o similar, respeta eso.

No preguntes por el formato del archivo, la metodología, ni la nomenclatura: eso ya está definido abajo.

## 1. Ramos, carpetas y códigos

| Ramo (como lo puede nombrar el usuario) | Carpeta | Prefijo de código | Nombre de prueba (frontmatter `prueba`) |
|---|---|---|---|
| Competencia Lectora / Lenguaje / Lectura | `1 - Competencia Lectora` | `CL` | "Competencia Lectora" |
| Matemática M1 / M1 | `2 - Matematica M1` | `M1` | "Competencia Matemática 1 (M1)" |
| Matemática M2 / M2 | `3 - Matematica M2` | `M2` | "Competencia Matemática 2 (M2)" |
| Ciencias - Biología | `4 - Ciencias/1 - Biologia` | `BIO` | "Ciencias — Biología" |
| Ciencias - Física | `4 - Ciencias/2 - Fisica` | `FIS` | "Ciencias — Física" |
| Ciencias - Química | `4 - Ciencias/3 - Quimica` | `QUI` | "Ciencias — Química" |
| Historia y Cs. Sociales | `5 - Historia y Ciencias Sociales` | `HIS` | "Historia y Ciencias Sociales" |

Dentro de cada carpeta de ramo, los capítulos son subcarpetas numeradas `NN - Nombre del capítulo` (dos dígitos, salvo Ciencias donde cada sub-área numera sus propios capítulos desde 01). **Siempre lista la carpeta del ramo antes de generar** para confirmar el número y el nombre exacto del capítulo tal como está escrito en disco (no lo inventes ni lo traduzcas).

Dentro de cada capítulo hay tres subcarpetas de nivel: `1 - principiante`, `2 - intermedio`, `3 - avanzado`.

**Excepción — Competencia Lectora**: su estructura no es de ítems sueltos sino de **textos** dentro de cada nivel: `NN - Nombre capítulo/1 - principiante/Texto 1 - Título/`, con 3-4 preguntas por texto, más dos archivos a nivel de capítulo: `_GUIA - <tema> en la PAES.md` (documento de materia, se escribe una sola vez por capítulo) y `_CLAVES.md` (tabla resumen código→clave, se actualiza cada vez que se agregan preguntas). Si el ramo es Lectora, sigue el patrón de §5.2 en vez del genérico de §5.1.

## 2. Flujo de trabajo

1. Resuelve ramo → carpeta y prefijo (tabla §1). Si es Ciencias, resuelve también la sub-área.
2. Lista la carpeta del ramo para confirmar nombre/número exacto del o los capítulos pedidos.
3. Para cada capítulo, lista sus 3 subcarpetas de nivel y cuenta los archivos `.md` que ya existen (ignora `_GUIA*.md` y `_CLAVES.md`). Determina cuántos ítems faltan por nivel según la cuota (§3).
4. Si necesitas precisión sobre el contenido curricular exacto del capítulo (definiciones, fórmulas, nombres oficiales de propiedades, subtemas del eje, ejemplos típicos), **usa búsqueda web** contra el temario oficial DEMRE (demre.cl) y fuentes educativas confiables — este proyecto se llama explícitamente "búsqueda en la web" porque la exactitud curricular importa más que la velocidad. No inventes nombres de leyes, teoremas o fechas históricas sin verificarlos.
5. Genera los ítems nuevos, uno por uno, siguiendo la metodología DEMRE (`paes-estudio-demre`: enunciado verosímil y autocontenido, una habilidad focal, alternativas paralelas, distractores tipificados, respuesta comentada de 5 bloques D→E→F) y el formato exacto de archivo de §5.
6. Varía deliberadamente entre ítems de un mismo capítulo/nivel: distinto subtema dentro del eje, distinto contexto (no repitas el mismo escenario dos veces), distinta habilidad cuando la prueba lo permite, y reparte la clave correcta entre A/B/C/D sin que se note un patrón (evita que salga la misma letra más de 2 veces seguidas).
7. Numera los ítems nuevos correlativamente después del último ítem existente de ese nivel (no reinicies ni reutilices números).
8. Escribe los archivos con Write, uno por archivo, en la ruta exacta de carpeta/nivel.
9. Si es Competencia Lectora, además actualiza `_CLAVES.md` del capítulo (agrega filas) y crea `_GUIA - <tema>.md` si el capítulo no lo tiene aún.
10. Al terminar, entrega un resumen breve: capítulo(s) trabajados, cuántos ítems por nivel se crearon, rango de códigos, y cualquier duda curricular que hayas resuelto por web search (cita la fuente si es un dato específico, ej. una fecha o cifra).
11. Usa TaskCreate/TaskUpdate para trackear el trabajo cuando generes más de ~10 archivos, para que el usuario vea el avance.

## 3. Cuota por defecto

El estándar ya establecido en el proyecto (ver capítulo 1 de Matemática M1) es **24 ítems por nivel por capítulo** (72 por capítulo). Úsalo como default para cualquier ramo/capítulo que no tenga ya un estándar distinto. Si el usuario pide una cantidad distinta, o si el capítulo ya tiene un número parcial de ítems con un patrón claro, respeta eso en vez del default.

Para Competencia Lectora la unidad no es "ítems sueltos" sino "textos": el patrón observado es 2 textos por nivel (6 por capítulo), con 3-4 preguntas cada uno.

## 4. Nomenclatura de archivos y de código (`codigo` en el frontmatter)

Formato general (ramos no-Lectora):

```
{PREFIJO}-{capítulo NN}-{nivel letra}-{ítem NN}-{slug-del-titulo}.md
```

- `nivel letra`: `P` principiante, `I` intermedio, `A` avanzado.
- `capítulo NN` e `ítem NN`: dos dígitos con cero a la izquierda.
- `slug-del-titulo`: título del ítem en minúsculas, sin tildes, separado por guiones, recortado a lo esencial (mismo estilo que los archivos existentes). Si se repite un slug dentro del mismo capítulo/nivel (mismo subtema tratado dos veces), añade `-2`, `-3`, etc. al final, igual que hacen los archivos existentes.

Ejemplo real: `M1-01-P-01-orden-y-comparacion-de-enteros.md`, código en frontmatter `M1-01-P-01`.

Para Competencia Lectora, el código sigue el patrón `CL-{cap NN}-{nivel letra}-T{n texto}-{n pregunta}` (ej. `CL-01-P-T1-02`), y el archivo va dentro de la carpeta `Texto N - Título/`.

Para Ciencias, el prefijo es el de la sub-área (`BIO`/`FIS`/`QUI`), no `CIE`.

## 5. Formato exacto del archivo

### 5.1 Ramos no-Lectora (M1, M2, Ciencias, Historia)

```markdown
---
codigo: {PREFIJO}-{cap}-{nivel}-{item}
asignatura: {nombre del ramo, ej. "Matemática M1", "Biología", "Historia y Ciencias Sociales"}
prueba: {nombre de prueba de la tabla §1}
capitulo: {número de capítulo sin ceros, ej. 7}
capitulo_nombre: "{nombre exacto de la carpeta del capítulo, sin el número}"
nivel: {principiante|intermedio|avanzado}
item: {número de ítem sin ceros}
titulo: "{título breve y descriptivo del contexto del ítem}"
eje: "{eje o área temática oficial, ver paes-estudio-demre §3}"
contenido: "{subtema específico dentro del eje/capítulo}"
habilidad: "{habilidad oficial exacta, ver paes-estudio-demre §3}"
clave: {A|B|C|D o A-E si es M2 suficiencia de datos}
origen: propio
---

# {Título}

**{Asignatura} · Capítulo {N} — {Nombre capítulo} · Nivel {nivel} · Ítem {N}**

**Eje:** {eje} · **Contenido:** {contenido} · **Habilidad:** {habilidad} · **Clave:** {letra}

{Enunciado completo, con contexto verosímil, datos, tablas/tablas markdown si aplica, y la pregunta directa al final.}

A) {alternativa}
B) {alternativa}
C) {alternativa}
D) {alternativa}

### Respuesta comentada

**Habilidad y tarea.** {bloque D, parte 1: nombrar y definir la habilidad, qué pide la tarea}

**El concepto que aplica.** {bloque D, parte 2: la regla/propiedad/ley exacta}

**Desarrollo.** {bloque D, parte 3: paso a paso}

**Por qué falla cada alternativa.** {bloque E: una frase por cada distractor, nombrando el tipo de error; no hace falta justificar la clave aquí si ya se justificó en Desarrollo}

**Qué hay que saber y saber hacer.** {bloque F: conocimiento declarativo + procedimiento + un dato/tip que extienda la materia}

---

> Ítem propio, construido con la metodología pública de las "preguntas comentadas" del DEMRE (serie oficial de videos y criterios del Informe Técnico). No es material oficial del DEMRE ni una pregunta liberada de la PAES.
```

Fórmulas matemáticas: en estos archivos markdown se pueden escribir en texto plano/LaTeX inline (`$...$`) salvo que el proyecto ya tenga un sitio HTML asociado a ese capítulo, en cuyo caso usar el mecanismo de SVG descrito en `paes-estudio-demre` §5.

### 5.2 Competencia Lectora

Cada texto es una carpeta `Texto N - Título breve/` dentro del nivel, con un archivo por pregunta:

```markdown
---
codigo: CL-{cap}-{nivel}-T{n}-{pregunta}
asignatura: Competencia Lectora
capitulo: {N}
capitulo_nombre: "{nombre capítulo}"
nivel: {principiante|intermedio|avanzado}
texto: "{Texto N — Título}"
pregunta: {n}
marca_textual: "{cita o referencia exacta al fragmento del texto que sostiene la respuesta}"
habilidad: {Localizar|Interpretar|Evaluar}
clave: {A|B|C|D}
origen: propio
---

# {Título de la pregunta o de la marca textual}

**Competencia Lectora · Capítulo {N} — {Nombre capítulo} · Nivel {nivel} · {Texto N} · Pregunta {n}**

{Presentación del texto: "[género] escrito por [autor], publicado en [medio] el año [año]" — solo en la primera pregunta de cada texto, o repetida como referencia breve.}

{Fragmento o texto completo, con párrafos numerados si el ítem los referencia.}

**Pregunta.** {enunciado}

A) {alternativa}
B) {alternativa}
C) {alternativa}
D) {alternativa}

### Respuesta comentada

{mismo esquema D→E→F que 5.1, adaptado a lectura: marca textual citada, por qué cada alternativa falla, qué habilidad y tarea lectora se evaluó}

---

> Ítem propio, construido con la metodología pública de las "preguntas comentadas" del DEMRE. No es material oficial del DEMRE ni una pregunta liberada de la PAES.
```

Actualiza `_CLAVES.md` del capítulo agregando una fila por pregunta nueva, con el mismo formato de tabla que las filas existentes (columnas: Código, Nivel, Texto, Pregunta, Habilidad, Clave).

## 6. Reglas de calidad (resumen; el detalle completo está en `paes-estudio-demre`)

- Una sola habilidad focal por ítem, tomada de la lista oficial de la prueba correspondiente.
- Enunciado autocontenido, con contexto real y verosímil, nunca decorativo.
- Alternativas paralelas en estructura/extensión; numéricas en orden; nunca "todas/ninguna de las anteriores".
- Cada distractor debe poder explicarse con una frase que nombre el error de razonamiento (verdadero-pero-irrelevante, variable equivocada, sobre-alcance, condición incompleta, error de cálculo típico, etc.).
- La respuesta comentada tiene tono de clase (120-220 palabras), no de solucionario telegráfico, y sigue siempre el orden D→E→F.
- No debe poder acertarse el ítem sin desplegar la habilidad declarada.
- Verifica al final: ¿se adivina la clave por longitud o lenguaje de las alternativas? Si sí, reescribe.

## 7. Al terminar

Resume en texto plano (sin tablas ni bullets extensos): qué capítulo(s) y ramo se trabajó, cuántos ítems se crearon por nivel, el rango de códigos usado, y ofrece seguir con el siguiente capítulo si quedan pendientes en ese ramo.

