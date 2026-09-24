# Preguntas tipo PAES por título (metodología DEMRE)

Cada título con materia recibe **3 ítems tipo PAES** creados por ti (2 si casi no tiene texto
propio; ninguno en secciones que ya son preguntas del libro ni en el título del capítulo).
`listar_titulos.py` entrega el `id` de cada título y cuántos ítems crear.

La diferencia con la variante `pdf-a-html+ia` es que aquí **no se pregunta lo que dice el
libro, sino lo que el estudiante debe saber hacer con eso**: ítems contextualizados, con una
habilidad oficial declarada y una respuesta comentada que enseña como una clase.

> Si en la sesión existe la skill `paes-estudio-demre` (o `paes-generador-preguntas`), léela y
> aplícala: manda esa metodología. Este archivo es su resumen operativo.

## 1. Antes de escribir: prueba, eje y habilidad

Pregunta al usuario (o dedúcelo del PDF) **a qué prueba PAES corresponde el libro** y déjalo
en el JSON (`"prueba"`). Habilidades oficiales y su proporción en la prueba real:

| Prueba | Habilidades oficiales | Proporción |
|---|---|---|
| Competencia Lectora | Localizar · Interpretar · Evaluar | 10-30 % · 30-60 % · 20-30 % |
| M1 | Resolver problemas · Modelar · Representar · Argumentar | 30-60 % · 5-25 % · 10-35 % · 5-15 % |
| M2 | Resolver problemas · Modelar · Representar · Argumentar | 30-60 % · 5-30 % · 10-35 % · 5-25 % |
| Ciencias | Observar y plantear preguntas · Planificar y conducir una investigación · Procesar y analizar la evidencia · Evaluar · Comunicar | 10-20 % · 20-40 % · 30-50 % · 20-30 % · resto |
| Historia y Cs. Sociales | Pensamiento temporal y espacial · Análisis de fuentes de información · Pensamiento crítico | 35-70 % · 15-45 % · 25-70 % |

Ejes o áreas temáticas (campo `eje`): M1 y M2 → Números · Álgebra y funciones · Geometría ·
Probabilidad y estadística. Ciencias → Biología (organización, estructura y actividad celular ·
procesos y funciones biológicas · herencia y evolución · organismo y ambiente), Física (ondas ·
mecánica · energía-Tierra · electricidad), Química (estructura atómica · química orgánica ·
reacciones químicas y estequiometría). Historia → Historia · Formación ciudadana · Sistema
económico. Competencia Lectora no tiene ejes.

**Una sola habilidad focal por ítem**, elegida antes de redactar, y dentro de cada sección
respeta las proporciones de la tabla (`revisar_preguntas.py --paes` las verifica).

## 2. El enunciado

1. **Contexto real y verosímil, nunca decorativo**: un agrónomo que compara vitamina C en tres
   frutas, un curso que mide la germinación de semillas, una investigadora que registra la
   temperatura de un lago. El contexto puede ser nuevo; la materia usada es la del título.
2. **Autocontenido**: todos los datos, unidades y restricciones necesarios están en el
   enunciado o en el estímulo (tabla, gráfico, figura o texto breve que tú describes).
3. **Pregunta directa y acotada**; si corresponde, indica dónde mirar («según la tabla»,
   «a partir del gráfico»).
4. **No debe poder acertarse sin desplegar la habilidad declarada.** Un estudiante que se
   sabe las definiciones de memoria, pero no sabe aplicarlas, debe fallar el ítem.
5. Nada de «¿Qué es X?» ni «¿Cuál de las siguientes define X?»: eso es memorización y la PAES
   no lo evalúa así.

## 3. Las alternativas

6. **Cuatro (A–D)**; en Ciencias y M2 se permiten 5 si el contenido lo pide.
7. **Paralelismo**: misma estructura sintáctica y **largo parecido** (que ninguna se distinga
   por ser la más larga o la más detallada: es el error más común y se detecta solo).
8. **Numéricas en orden** creciente o decreciente.
9. Prohibido «todas/ninguna de las anteriores» y las dobles negaciones.
10. **Ningún distractor absurdo**: cada uno nace de un error de razonamiento real. Declara su
    tipo con esta tipología:

| `tipo` | Cómo funciona |
|---|---|
| `verdadero pero irrelevante` | Es cierto, pero no responde lo preguntado. |
| `variable equivocada` | Usa o mide otra variable distinta de la pedida. |
| `sobre-alcance` | Concluye más de lo que los datos permiten. |
| `sub-alcance` | Usa una distinción que los datos no contienen. |
| `condición incompleta` | Cumple una de las dos condiciones necesarias. |
| `error de cálculo típico` | Resultado de una operación mal encaminada. |
| `anacronismo` | Correcto, pero en otro periodo. |
| `atribución cruzada` | Asigna a un sujeto lo que hizo otro. |
| `relación inversa o inexistente` | Invierte la causalidad o inventa el vínculo. |

## 4. La respuesta comentada (bloque `comentario`)

Debe **enseñar algo nuevo**, como un profesor explicando la página del libro. Orden fijo:

1. `habilidad_tarea`: «Esta pregunta evalúa la habilidad de *[habilidad]*, es decir,
   *[definición en una frase]*. La tarea consiste en *[qué hay que hacer con la información]*.»
2. `concepto`: la definición, ley o procedimiento **del libro** que resuelve el ítem, con su
   terminología (menciona el título de donde sale).
3. `desarrollo`: el razonamiento paso a paso, mostrando el dato, la marca textual o el cálculo
   que sostiene cada paso hasta la clave.
4. `distractores`: una frase por alternativa incorrecta que **nombra el error** (tipología §3).
5. `saber_hacer`: «Qué hay que saber y saber hacer»: el conocimiento, el procedimiento y un
   dato o atajo que extienda la materia (un caso especial, una generalización, la conexión con
   la unidad siguiente).

Extensión orientativa del comentario completo: **120-220 palabras**.

## 5. Formato: `preguntas-ia/NN.json`

```json
{
  "prueba": "ciencias",
  "preguntas": [
    {
      "tema": "variables-experimentales-y-su-clasificacion",
      "eje": "Organización, estructura y actividad celular",
      "habilidad": "Planificar y conducir una investigación",
      "enunciado": "Un grupo de estudiantes quiere saber si la cantidad de fertilizante influye en la altura de plantas de poroto. Preparan cuatro macetas con la misma tierra, el mismo riego y la misma exposición al sol, y agregan 0, 2, 4 y 6 g de fertilizante. A las tres semanas miden la altura de cada planta. ¿Cuál es la variable dependiente de este diseño?",
      "alternativas": [
        "La cantidad de tierra usada en cada maceta.",
        "La altura alcanzada por cada planta.",
        "La masa de fertilizante agregada.",
        "El tiempo de exposición al sol."
      ],
      "correcta": "B",
      "comentario": {
        "habilidad_tarea": "Esta pregunta evalúa la habilidad de planificar y conducir una investigación, es decir, reconocer y organizar los elementos de un diseño experimental. La tarea consiste en distinguir, dentro del diseño descrito, cuál es la variable que se mide.",
        "concepto": "Según el título «Variables experimentales y su clasificación», la variable dependiente (o variable respuesta) es la que cambia en función de la independiente y es la que el investigador cuantifica con un instrumento.",
        "desarrollo": "Lo que los estudiantes deciden y modifican es la masa de fertilizante (0, 2, 4 y 6 g): esa es la independiente. Tierra, riego y sol se mantienen iguales, así que son controladas. Lo único que se mide al final es la altura de cada planta, que depende del fertilizante recibido: es la variable dependiente.",
        "saber_hacer": "Hay que saber la diferencia entre variable independiente, dependiente y controlada, y saber leer un diseño experimental identificando qué se cambia, qué se mantiene y qué se mide. Atajo para la PAES: la variable dependiente casi siempre aparece en la frase que dice qué se midió o registró al final."
      },
      "distractores": {
        "A": {"tipo": "variable equivocada", "texto": "La cantidad de tierra se mantiene igual en las cuatro macetas: es una variable controlada, no la que se mide."},
        "C": {"tipo": "variable equivocada", "texto": "La masa de fertilizante es lo que los estudiantes manipulan, es decir, la variable independiente."},
        "D": {"tipo": "condición incompleta", "texto": "El tiempo de exposición al sol también se mantiene constante, por lo que es una variable controlada."}
      }
    }
  ]
}
```

`tema` es el `id` que entregó `listar_titulos.py`. También se acepta `distractores` con texto
simple (sin `tipo`), pero en esta variante se pide el tipo.

## 6. Verificación obligatoria

Antes de ensamblar:

```bash
python scripts/revisar_preguntas.py --preguntas preguntas-ia/01.json \
    --fragmentos fragmentos --seccion 1 --paes --prueba ciencias
```

Corrige todo lo que aparezca en `problemas` y repite hasta que quede vacío. Además, revisa a
mano estas dos preguntas del DEMRE:

- **Leyendo solo las alternativas, ¿se adivina la clave** por su largo, su especificidad o su
  lenguaje? Si sí, reescríbelas.
- **¿Un estudiante que domina el contenido pero no la habilidad falla el ítem?** Debe fallarlo.
