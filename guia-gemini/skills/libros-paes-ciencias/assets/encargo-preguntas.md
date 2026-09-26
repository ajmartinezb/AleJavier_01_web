# Encargo: ítems IA tipo PAES — {LIBRO}, capítulo {N} ({TÍTULO DEL CAPÍTULO})

Proyecto: la carpeta raíz del proyecto (donde está GEMINI.md). Capítulo: {libro}/capitulos/{capNN-slug}/ (lee los .md del bloque que te toca y también 00-portada.md y 01-conceptos-clave.md para contexto).

LEE ANTES DE ESCRIBIR:
1. herramientas/references/preguntas-paes.md (formato JSON y reglas; manda).
2. Un ejemplo de calidad ya aprobado: biologia/capitulos/cap02-niveles-organizacion-teoria-celular/preguntas.json (mira 3–4 ítems para calibrar tono y extensión).
3. Resumen de metodología DEMRE (skill paes-estudio-demre): contexto real y verosímil, nunca decorativo; enunciado autocontenido con datos, unidades y restricciones; UNA habilidad focal; pregunta directa; 4 alternativas A–D paralelas en estructura y LARGO; numéricas en orden creciente o decreciente; nada de «todas/ninguna de las anteriores» ni dobles negaciones; ningún distractor absurdo: cada uno nace de un error real y declara su `tipo` de esta lista exacta: verdadero pero irrelevante, variable equivocada, sobre-alcance, sub-alcance, condición incompleta, error de cálculo típico, anacronismo, atribución cruzada, relación inversa o inexistente. En Ciencias, el contenido es el vehículo y lo evaluado es la habilidad científica (formular pregunta de investigación, identificar variables, elegir procedimiento, interpretar tabla/gráfico, identificar evidencia que apoya una hipótesis, evaluar validez o coherencia, comparar modelo con situación real, predecir). No hagas preguntas de «¿qué es X?».

FORMATO DE CADA ÍTEM (objeto JSON):
{"tema": "<id exacto del título>", "eje": "{EJE O ÁREA}", "habilidad": "<una de: Observar y plantear preguntas | Planificar y conducir una investigación | Procesar y analizar la evidencia | Evaluar | Comunicar>", "enunciado": "...", "alternativas": ["...","...","...","..."], "correcta": "A|B|C|D", "comentario": {"habilidad_tarea": "Esta pregunta evalúa la habilidad de ..., es decir, .... La tarea consiste en ....", "concepto": "Según el título «<título de la sección>», ... (la ley/definición del capítulo con su terminología)", "desarrollo": "paso a paso hasta la clave, con cálculos y unidades si corresponde", "saber_hacer": "Qué hay que saber y saber hacer: conocimiento + procedimiento + un dato o atajo que extienda la materia"}, "distractores": {"<letra>": {"tipo": "<tipo>", "texto": "Esta opción es incorrecta porque ... (nombra el error)"} ... para las 3 letras incorrectas}}

Comentario completo (los 4 bloques sumados): 130–220 palabras. Español de Chile, redacción propia; no copies frases del capítulo (el revisor detecta secuencias literales del libro en el enunciado). Unidades SI, coma decimal, espacio entre número y unidad; potencias con <sup>…</sup> (HTML permitido en enunciado y alternativas). Si necesitas una tabla, descríbela dentro del enunciado en texto (p. ej. «f = 5 Hz → λ = 6,0 cm; f = 10 Hz → λ = 3,0 cm…») o usa una tabla HTML simple <table><tr><th>…</th></tr>…</table>.

EQUILIBRIOS OBLIGATORIOS (dentro de tu lote):
- Claves: reparte A, B, C y D lo más parejo posible; nunca la misma letra en los 3 ítems de un título; no más de 2 iguales seguidas.
- Largo: la clave NO debe delatarse por largo. La posición de largo de la clave (más larga / 2.ª / 3.ª / más corta) debe repartirse de forma pareja (≈25 % cada una). Verifícalo con un script al final. Además, ninguna alternativa puede medir más de 3 veces la más corta, y la correcta no puede superar en >40 % y >12 caracteres al promedio de las otras.
- Habilidades en tu lote: ≈15 % Observar y plantear preguntas, ≈30 % Planificar y conducir una investigación, ≈35 % Procesar y analizar la evidencia, ≈20 % Evaluar (Comunicar, opcional y como mucho 1).
- Varía contextos reales y chilenos cuando se pueda (laboratorio escolar, noticias científicas, instituciones chilenas, datos reales, simulaciones…); no repitas escenario dentro de un mismo título.
- Precisión física: verifica cada cálculo (ver datos abajo).

CANTIDAD: exactamente las indicadas por título abajo (3 en subsecciones a., b., …; 2 en el título de sección numerado).

SALIDA: escribe un archivo JSON válido con la forma {"prueba": "ciencias", "preguntas": [ ... ]} en la ruta indicada abajo. Luego valida:
  python herramientas/construir.py {libro}          (primero, para generar los fragmentos)
  python herramientas/scripts/revisar_preguntas.py --preguntas <tu archivo> --fragmentos {libro}/.construccion/fragmentos --seccion {N} --paes --prueba ciencias
  python guia-gemini/scripts/reparto_claves.py <tu archivo>
Corrige hasta que no queden problemas por pregunta (ignora solo los avisos globales de proporción de habilidades si tu lote es pequeño, pero intenta cumplirlos). No modifiques ningún otro archivo del repo. Responde con un resumen breve: número de ítems, reparto de claves, reparto de posición de largo, reparto de habilidades y problemas pendientes.

NOTAS PARA ESTE CAPÍTULO (rellenar en cada sesión):
- eje: "{EJE}" (exactamente así. Física: «Ondas», «Mecánica», «Energía – Tierra» o «Electricidad». Biología: «Organización, estructura y actividad celular», «Procesos y funciones biológicas», «Herencia y evolución», «Organismo y ambiente» o «Estructura y función de los seres vivos»; usa el mismo que ya tenga ese capítulo).
- Qué evalúa la PAES en este tema: {…}
- Datos y valores que deben usarse (con la misma cifra que el capítulo): {…}
- Errores frecuentes de los estudiantes, para los distractores: {…}

TU LOTE (ids exactos de los títulos, sacados de listar_titulos.py):
- {id-del-titulo-numerado}: 2 ítems
- {a-id-subtitulo}: 3
- …
Salida: {libro}/capitulos/{capNN-slug}/notas/items-lote-1.json  (la carpeta notas/ no se publica; al final se unen los lotes con guia-gemini/scripts/unir_lotes.py)
