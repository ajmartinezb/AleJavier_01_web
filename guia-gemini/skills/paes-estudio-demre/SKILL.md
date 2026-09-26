---
name: "paes-estudio-demre"
description: "Metodología oficial DEMRE (derivada de la serie de videos \"Pregunta comentada PAES\") para crear preguntas tipo PAES y redactar sus respuestas explicadas en los sitios web de estudio (Matemáticas M1, Tomo 1, Tomo 2, Biología, Física, Química, Historia, Lenguaje). Úsala siempre que se cree o edite un capítulo/libro de estos sitios, se agreguen preguntas, se mejore el botón \"Ver respuesta\", o se desarrollen las subunidades (\"Sub\") de una unidad."
---

# Metodología de estudio PAES (estilo DEMRE) para los sitios de libros Moraleja

## Contexto del proyecto

El usuario (Ale) tiene una carpeta con libros escaneados en PDF (editorial Moraleja, ediciones oficiales de estudio PAES): Biología, Física, Historia, Lenguaje, Matemáticas M1, Matemáticas Tomo 1, Matemáticas Tomo 2, Química. A partir de esos libros construye sitios web de estudio en HTML (uno por capítulo, ej. `capitulo1-numeros-enteros.html`), desplegados en Netlify (`deploy-netlify/`). Cada capítulo trae ejercicios de opción múltiple (formato DEMRE) con un botón `Ver respuesta` que despliega un `div.respuesta-caja` con la alternativa correcta y una explicación.

El sitio principal del temario vive en `paes-2027/*.html` (uno por ramo y uno por capítulo, ej. `m1-cap-1.html`), con su propio HTML/CSS de unidades (`.subject`, `.units`, `.concept`, `.guided-example`, `.paes-problem`, `.exercise-set`, `.subunits-detail`, etc.) — es distinto del formato de archivos `.md` sueltos descrito en `paes-generador-preguntas`, y ambos formatos conviven en el proyecto según qué parte se esté trabajando.

Objetivo permanente: que **cada respuesta enseñe algo nuevo** — que el botón "Ver respuesta" entregue tanta materia como una clase completa sobre ese contenido, igual que un profesor explicando la página del libro de la que salió la pregunta.

Releer y aplicar este skill **cada vez que se trabaje un nuevo libro o capítulo**, en cualquier asignatura.

En la carpeta del proyecto existe el documento de referencia `METODO-DEMRE-PREGUNTA-COMENTADA.md`, con el inventario completo de los videos, las fichas de los 14 ítems del ciclo 2026 y las citas literales del DEMRE. Consultarlo cuando se necesiten ejemplos concretos.

---

## 1. La plantilla de "pregunta comentada" del DEMRE

Fuente: los 28 videos de la serie *Pregunta comentada PAES* del canal oficial @DEMREUchile, donde profesionales de la Unidad de Construcción de Pruebas (UCP) construyen y explican un ítem. **Todos siguen exactamente esta secuencia**, y esa secuencia es el molde a copiar:

| Bloque | Contenido |
|---|---|
| **A. Encuadre** | Identificar la prueba y, en Ciencias, el **área temática** del ítem ("del área de mecánica", "del área temática de química orgánica"). |
| **B. Contextualización del estímulo** *(si hay texto o fuente)* | Género + autoría + medio + año → clasificación de la **situación de lectura** → características del género → estructura → síntesis temática → hipótesis de lectura. |
| **C. Presentación del ítem** | Enunciado completo y las alternativas **una por una**. Si hay gráficos/tablas, invitar a detenerse a analizarlos. |
| **D. Resolución** | **Nombrar y definir la habilidad evaluada**, luego razonar paso a paso hasta la clave. |
| **E. Descarte** | Explicar **una por una** por qué cada opción incorrecta lo es. |
| **F. Metacognición** | "¿Qué hay que saber y saber hacer para responder correctamente?" — conocimiento declarativo + procedimiento. |
| **G. Cierre** | Cierre breve. |

El orden **D → E → F** es invariable.

---

## 2. Reglas de construcción del ítem

### Enunciado

1. **Contexto real y verosímil, nunca decorativo** (un agrónomo comparando vitamina C en tres frutas; máquinas pintando líneas de carretera; alguien verificando lo que dice su libro de óptica).
2. **Toda la información necesaria está en el enunciado** o en el estímulo adjunto, incluidas las restricciones que hacen válido el procedimiento ("con x ≠ y y x ≠ −y", "cuerdas inextensibles y de masa despreciable", "se mantuvo controlada la humedad").
3. **Una sola habilidad focal por ítem**, decidida antes de redactar.
4. **Pregunta directa y acotada**; cuando corresponda, indicar dónde mirar ("En el cuarto párrafo, ¿por qué…?", "Con base en los datos recopilados, ¿cuál…?").
5. **No debe poder acertarse sin desplegar el conocimiento y la habilidad del constructo** (criterio explícito de la revisión de evaluación del DEMRE).

### Alternativas

6. **Cuatro opciones A–D** en Competencia Lectora, M1 e Historia. En **M2 y Ciencias** conviven ítems de 4 y de 5 opciones; los de **suficiencia de datos** (solo M2) son siempre de 5.
7. **Paralelismo sintáctico y de extensión** entre las cuatro ("El afianzamiento de… / La internacionalización de… / El aumento de… / La instalación de…").
8. **Alternativas numéricas en orden** creciente o decreciente.
9. **Nada de "todas las anteriores" / "ninguna de las anteriores"**, ni dobles negaciones.
10. **Ningún distractor absurdo.** Este es el corazón del método DEMRE.

### Tipología de distractores (usar esta lista al construir y al explicar)

| Tipo | Cómo funciona |
|---|---|
| **Verdadero pero irrelevante** | La afirmación es correcta, pero no responde lo preguntado (ej.: "20 + 5 = 25" no justifica que 5 sea el 25 % de 20). |
| **Variable equivocada** | Mide o relaciona una variable distinta de la del objetivo (contar gametos en vez de gametos *unidos*). |
| **Sobre-alcance** | Afirma más de lo que los datos permiten concluir. |
| **Sub-alcance / dato no recogido** | Usa una distinción que los datos no contienen. |
| **Condición incompleta** | Cumple una de las dos condiciones necesarias (misma cuerda ✔, distinta posición ✘). |
| **Error de cálculo típico** | Resultado plausible de una operación mal encaminada. |
| **Anacronismo / desfase temporal** | Correcto, pero en otro periodo. |
| **Atribución cruzada** | Asigna a un sujeto lo que hizo otro. |
| **Relación inversa o inexistente** | Invierte una causalidad o inventa un vínculo sin respaldo en la fuente. |

Regla operativa: cada distractor debe poder explicarse en una frase que empiece con *"esta opción es incorrecta porque…"* y esa frase debe **nombrar el error de razonamiento**, no limitarse a decir que no es.

### Mecanismos de dificultad en Competencia Lectora

- La información pedida aparece de forma **literal, parafraseada o mediante hiperónimos** (el enunciado dice "el aporte de matemáticos relevantes" donde el texto enumera "Euclides, Fermat, Gauss, Riemann…").
- La conclusión debe apoyarse en **marcas textuales citables**.
- Toda lectura va precedida de una **presentación** de dos líneas antes del título: `[género] escrito por [autor], publicado en [medio] el año [año]`. Permite formular hipótesis de lectura y sostiene los ítems de la habilidad *Evaluar*.
- Trampas de conteo declaradas por el DEMRE: la bajada o subtítulo **no** cuenta como párrafo.

### Ciencias: el ítem se construye sobre el método científico

El contenido disciplinar es el vehículo; lo evaluado es la habilidad científica. Tareas típicas: formular la **pregunta de investigación** que dio origen a un estudio; elegir el **procedimiento** que pone a prueba una hipótesis identificando variable independiente, dependiente y controlada; elegir la **representación correcta** de los resultados esperados; reconocer la **evidencia que apoya** una hipótesis; comparar el **modelo ideal** con la situación real.

### M2: suficiencia de datos

Enunciado + dos afirmaciones (1) y (2). No se pide resolver, sino decidir si la información alcanza. Cinco opciones fijas: **A)** (1) por sí sola · **B)** (2) por sí sola · **C)** Ambas juntas · **D)** Cada una por sí sola · **E)** Se requiere información adicional.

Protocolo: 1) identificación inicial · 2) definición del objetivo (simplificar primero) · 3) evaluar (1) · 4) evaluar (2) **olvidando (1)** · 5) análisis de resultados (si (1) sí y (2) no → A; si (2) sí y (1) no → B; si ambas por separado → D, y el desarrollo se detiene ahí) · 6) solo si ninguna sirvió sola, análisis conjunto → C, o si tampoco alcanza → E.

---

## 3. Habilidades y ejes oficiales (Admisión 2027, demre.cl)

| Prueba | Habilidades (nombres exactos) | Rango de ítems |
|---|---|---|
| **Competencia Lectora** | Localizar · Interpretar · Evaluar | 10–30 % · 30–60 % · 20–30 % |
| **M1** | Resolver problemas · Modelar · Representar · Argumentar | 30–60 % · 5–25 % · 10–35 % · 5–15 % |
| **M2** | Resolver problemas · Modelar · Representar · Argumentar | 30–60 % · 5–30 % · 10–35 % · 5–25 % |
| **Ciencias** | Observar y plantear preguntas · Planificar y conducir una investigación · Procesar y analizar la evidencia · Evaluar · Comunicar | 10–20 % · 20–40 % · 30–50 % · 20–30 % |
| **Historia y Cs. Sociales** | Pensamiento temporal y espacial · Análisis de fuentes de información · Pensamiento crítico | 35–70 % · 15–45 % · 25–70 % |

**Tareas lectoras.** *Localizar*: extraer información explícita, también cuando aparece vía sinónimos o paráfrasis. *Interpretar*: relaciones problema/solución, categoría/ejemplo, causa/consecuencia; inferencias locales y globales; significado de una parte o del todo; sintetizar ideas centrales; jerarquía de ideas; función de un elemento textual. *Evaluar*: intención comunicativa según destinatario; juzgar la información (calidad, pertinencia, suficiencia, consistencia); juzgar la forma (registro, estructura, propósito); calificar posición, actitud o tono del emisor; valorar recursos lingüísticos y no lingüísticos; valorar la información en nuevos contextos.

**Situaciones de lectura — son tres.** *Personales* (intereses individuales, ocio; lenguaje sencillo y cercano, público masivo). *Públicas* (participación ciudadana: reglamentos, leyes, instructivos, documentos estatales). *Educativas* (aprender en educación formal, propósito instructivo; lenguaje formal, estructura expositiva o argumentativa, fuente confiable; se subdividen en especializadas y de divulgación). No existe una situación "laboral" en Competencia Lectora.

**Ejes y áreas temáticas**

- **M1** (7° a 2° medio): Números · Álgebra y funciones · Geometría · Probabilidad y estadística.
- **M2** (7° a 4° medio): los mismos ejes ampliados — reales, logaritmos, matemática financiera; sistemas 2×2, función potencia/exponencial/logarítmica y trigonométricas; homotecia, razones trigonométricas, relaciones métricas en la circunferencia, esferas, rectas en el plano; medidas de dispersión, probabilidad condicional, combinatoria, binomial y normal.
- **Ciencias** (11 áreas): *Biología* — organización, estructura y actividad celular; procesos y funciones biológicas; herencia y evolución; organismo y ambiente. *Física* — ondas; mecánica; energía-Tierra; electricidad. *Química* — estructura atómica; química orgánica; reacciones químicas y estequiometría.
- **Historia y Cs. Sociales**: Historia (Mundo, América y Chile) · Formación ciudadana · Sistema económico.
- **Competencia Lectora** no tiene ejes temáticos; su referente es el eje de Lectura de las Bases Curriculares (textos no literarios y literarios como conocimiento subyacente).

**Estructura de las pruebas.** Competencia Lectora 65 preguntas sobre 7 textos (60 puntúan, 2 h 30) · M1 65 (60, 2 h 20) · M2 55 (50, 2 h 20) · Ciencias 80 = 54 módulo común + 26 electivo (75, 2 h 40) · Historia 65 (60, 2 h). No se descuenta puntaje por respuestas erradas.

**Enlaces.** Temarios: <https://demre.cl/la-prueba/pruebas-y-temarios/presentacion-pruebas-temarios-paes-regular> · Informe Técnico cap. 2 (construcción de las pruebas): <https://demre.cl/investigacion/documentos/informes/informe-tecnico-paes-capitulo-02.pdf> · Ejemplos de preguntas comentadas: <https://demre.cl/la-prueba/ejemplos-preguntas/paes-p2023/index.html> · Pruebas oficiales: <https://demre.cl/publicaciones/2026/pruebas-oficiales-y-seleccion-preguntas-paes> · Videos: <https://www.youtube.com/@DEMREUchile>

---

## 4. Estándar de una respuesta "que enseña algo nuevo"

El contenido de `respuesta-explicacion` debe tener, **en este orden**, los bloques D–F del guion DEMRE:

1. **Habilidad y tarea** — "Esta pregunta evalúa la habilidad de *[habilidad oficial]*, es decir, *[definición en una frase]*. La tarea consiste en *[qué hay que hacer con la información]*."
2. **Concepto o regla del libro que aplica** (1-2 frases): nombrar y enunciar la propiedad, teorema, ley o definición exacta que resuelve el ejercicio, citando si es posible el capítulo del libro fuente.
3. **Desarrollo paso a paso**: cada transformación algebraica/numérica o cada inferencia, mostrando el dato o la marca textual que la sostiene.
4. **Por qué falla cada distractor**: una frase por alternativa, **nombrando el error de razonamiento** según la tipología de la sección 2.
5. **"Qué hay que saber y saber hacer"**: el conocimiento declarativo, el procedimiento, y un dato/tip que extienda la materia más allá del ejercicio (un caso especial, una generalización, un atajo de resolución, o la conexión con la siguiente unidad).

Tono de clase, no de solucionario telegráfico. Extensión orientativa: 120–220 palabras (más si el concepto lo amerita).

Frases-marca reutilizables, literales del DEMRE: *"Ahora que ya conoces el ítem y sus opciones, te explicaremos cómo se contesta esta pregunta."* · *"¿Cómo se podría responder la pregunta?"* · *"Para responder correctamente esta pregunta, debes considerar que…"* · *"Teniendo en cuenta lo anterior, la opción A es incorrecta porque…"* · *"¿Qué hay que saber y saber hacer para responder la pregunta correctamente?"*

Ejemplo de transformación (antes → después), sobre ecuaciones de 2º grado:

- **Antes:** "De ax²+bx+c=0 se obtiene x=(−b±√(b²−4ac))/2a, por lo tanto x=2."
- **Después:** "Esta pregunta evalúa la habilidad de *resolver problemas*. Es una ecuación cuadrática de la forma ax²+bx+c=0; la Fórmula General permite obtener sus soluciones sin factorizar: x=(−b±√(b²−4ac))/2a. Identificamos a=…, b=…, c=… y reemplazamos: […desarrollo…], obteniendo x=2. La alternativa B (x=−2) corresponde a tomar solo la raíz negativa del discriminante sin considerar el signo de b; la C surge de un error de signo al reemplazar c; la D confunde el producto de las raíces con su suma. **Qué hay que saber y saber hacer:** reconocer la forma canónica y aplicar la fórmula general. Dato clave para la PAES: el discriminante Δ=b²−4ac dice, sin resolver, cuántas soluciones reales hay (Δ>0 dos, Δ=0 una, Δ<0 ninguna) — conviene calcularlo primero para descartar alternativas."

---

## 5. Formato técnico en los sitios HTML

```html
<ol type="A"><li>...</li><li>...</li><li>...</li><li>...</li></ol>
<button type="button" class="ver-respuesta-btn" data-target="demre-resp-N">Ver respuesta</button>
<div class="respuesta-caja" id="demre-resp-N" hidden data-correct-index="X">
  <p class="respuesta-titulo">Respuesta correcta: alternativa Y</p>
  <p class="respuesta-explicacion">...</p>
</div>
```

Las fórmulas matemáticas se insertan como SVG (LaTeX renderizado, base64 inline `<img>`), no como texto plano ni MathML. Mantener ese mecanismo al agregar contenido matemático nuevo.

### 5.1 Desarrollo de las subunidades ("Sub")

Cada unidad de los sitios `paes-2027/*-cap-N.html` termina con una lista de subunidades (`Sub 1.1.1: ...`). Por defecto estas nacían como una simple lista `<ul class="subunits"><li>título</li>...</ul>` sin contenido propio — es deuda pendiente en todos los capítulos del proyecto. **Siempre que se trabaje o revise una unidad, desarrollar sus Sub con este patrón** (mini-teoría de 2-4 líneas + un ejemplo resuelto corto, plegable con `<details>`), en vez de dejarlas como títulos sueltos:

```html
<style>
/* agregar una sola vez por archivo, junto al resto del <style> */
.subunits-detail{list-style:none;margin:.7rem 0 .3rem;padding:0;display:grid;gap:.6rem}
.subunit-detail{border:1px solid var(--line);border-left:3px solid var(--subject);border-radius:0 12px 12px 0;background:#fbfcfe;padding:.75rem .85rem}
.subunit-detail summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:.75rem;font-weight:750;font-size:.88rem;color:#344054}
.subunit-detail summary::-webkit-details-marker{display:none}
.subunit-detail summary .subunit-chevron{color:var(--subject);font-size:1.1rem;transition:transform .15s}
.subunit-detail:not([open]) .subunit-chevron{transform:rotate(-90deg)}
.subunit-body{margin-top:.55rem;padding-top:.55rem;border-top:1px dashed var(--line)}
.subunit-body p{margin:0 0 .5rem;color:#526078;font-size:.85rem;line-height:1.6}
.subunit-example{margin:.5rem 0 0;padding:.55rem .65rem;border-radius:8px;background:color-mix(in srgb,var(--subject) 6%,white);font-size:.82rem;color:#344054;line-height:1.55}
.subunit-example strong{color:var(--subject)}
</style>

<ul class="subunits-detail">
  <details class="subunit-detail">
    <summary>Sub N.N.N: Título de la subunidad<span class="subunit-chevron" aria-hidden="true">⌄</span></summary>
    <div class="subunit-body">
      <p>Mini-teoría de la subunidad: 2-4 líneas, definición o regla concreta (no repetir la explicación conceptual de la unidad completa; ir un nivel más específico).</p>
      <p class="subunit-example"><strong>Ejemplo.</strong> Un ejemplo corto resuelto en 1-2 líneas, con números o caso concreto.</p>
    </div>
  </details>
  <!-- repetir un <details> por cada Sub de la unidad -->
</ul>
```

Reglas: el CSS se agrega **una sola vez** por archivo HTML (verificar con grep que `.subunit-detail` no exista ya antes de insertarlo, para no duplicar el `<style>`); cada `<details>` reemplaza un `<li>` de la lista original; el ejemplo del mini-bloque debe ser propio (no copiado del libro fuente, mismo criterio de `libros-ingles-extractor-mate` §6); y tras editar, verificar con BeautifulSoup o similar que no haya quedado contenido duplicado (`soup.select('.unit-title')` debe devolver la cantidad exacta de unidades del capítulo, ni una más).

---

## 6. Fuente del contenido: usar el libro, no solo el enunciado

1. Localizar en el PDF del libro correspondiente la sección de teoría del tema (usar el índice del PDF).
2. Extraer definiciones exactas, nombres de propiedades/teoremas y ejemplos resueltos que usa el libro, para que la explicación use su terminología y no una explicación genérica de internet.
3. Complementar con el temario oficial DEMRE de esa asignatura y mencionar la unidad temática a la que pertenece el ejercicio.

---

## 7. Checklist al crear o mejorar preguntas

**Antes de escribir**
1. Leer este skill completo y abrir `ESTUDIO-METODOLOGIA-PAES.md` para ubicar el libro/capítulo en la tabla de avance.
2. Elegir prueba, eje/área temática y **una** habilidad oficial.
3. Verificar en el temario vigente que el contenido esté dentro del programa.
4. Ubicar la sección de teoría relevante en el PDF del libro.

**Al redactar el ítem**
5. Enunciado autocontenido, con contexto verosímil, datos, unidades y restricciones.
6. Pregunta directa y acotada; si aplica, indicar dónde mirar.
7. Alternativas paralelas en estructura y extensión; numéricas en orden.
8. Clave única, defendible con evidencia explícita.
9. Cada distractor con un error de razonamiento identificable (tipología §2).
10. Comprobar que no se pueda acertar sin usar la habilidad declarada.

**Al escribir la respuesta comentada**
11. Aplicar los 5 bloques de la sección 4, conservando el mecanismo SVG para fórmulas.
12. Refutar **todas** las alternativas, incluida la clave (por qué sí).

**Verificación final**
13. Leer solo las alternativas: ¿se adivina la clave por longitud, especificidad o lenguaje? Si sí, reescribir.
14. ¿Un estudiante que domina el contenido pero no la habilidad falla el ítem? Debe fallarlo.
15. Mantener el HTML/CSS/JS existente (`ver-respuesta-btn`, `respuesta-caja`, `data-correct-index`).
16. Si la unidad tiene subunidades ("Sub") sin desarrollar, aplicar el patrón de la sección 5.1 antes de dar la unidad por terminada.
17. Actualizar la tabla de avance en `ESTUDIO-METODOLOGIA-PAES.md` (crearla si no existe) y, si se despliega vía Netlify, copiar el HTML actualizado a `deploy-netlify/public/`.

