## Ejemplos PAES resueltos

Cuatro preguntas del estilo de la PAES sobre manipulación genética, resueltas con el guion DEMRE. Intenta responder antes de leer la resolución.

::: ejemplo
**Ejemplo 1 · Habilidad: Planificar y conducir una investigación**

Un laboratorio quiere que una bacteria produzca una proteína humana. Dispone del ADN humano que contiene el gen, de plásmidos y de cuatro enzimas de restricción distintas (P, Q, R y S), cada una con su propio sitio de reconocimiento.

¿Qué criterio debe seguir al elegir la enzima para cortar el gen y el plásmido?

- **A)** Cortar el gen con la enzima P y el plásmido con la enzima Q, para que los extremos sean distintos.
- **B)** Cortar ambos ADN con la misma enzima, para que los extremos cohesivos sean complementarios.
- **C)** Cortar el gen con las cuatro enzimas, para asegurar que quede completamente aislado.
- **D)** Cortar el plásmido con las cuatro enzimas, para aumentar la cantidad de sitios disponibles.

**Resolución.** Esta pregunta evalúa la habilidad de *planificar y conducir una investigación*: elegir el procedimiento adecuado para lograr un objetivo. La tarea consiste en aplicar lo que se sabe sobre los extremos cohesivos.

Una enzima de restricción corta en una secuencia determinada y deja extremos cohesivos: puntas de cadena simple con una secuencia específica. Esas puntas **solo se aparean con puntas complementarias**, es decir, con las que deja la misma enzima. Si el gen y el plásmido se cortan con enzimas distintas, sus extremos no encajan y la ligasa no puede unirlos. Clave: **B**.

- **A** hace justamente lo contrario de lo necesario: extremos distintos impiden la unión. *Relación inversa o inexistente.*
- **C** fragmentaría el gen en varios trozos, en vez de aislarlo entero. *Sobre-alcance.*
- **D** abriría el plásmido en muchos puntos y lo destruiría como vector circular. *Relación inversa o inexistente.*

**Qué hay que saber y saber hacer:** conocer qué son los extremos cohesivos y deducir de ahí la condición sobre la enzima. *Dato para la PAES:* cuando el enunciado ofrece varias enzimas, la respuesta casi siempre es **la misma en ambos ADN**; es la comprobación más rápida para descartar alternativas.
:::

::: ejemplo
**Ejemplo 2 · Habilidad: Procesar y analizar la evidencia**

Se realiza una PCR partiendo de **una sola** molécula de ADN molde. El equipo se programa para 20 ciclos y cada ciclo duplica la cantidad de fragmento.

¿Cuál es el orden de magnitud del número de copias al terminar?

- **A)** 40 copias
- **B)** 400 copias
- **C)** 20 000 copias
- **D)** 1 000 000 de copias

**Resolución.** Esta pregunta evalúa la habilidad de *procesar y analizar la evidencia*: aplicar una relación cuantitativa conocida. La tarea consiste en reconocer que el crecimiento es exponencial y no lineal.

Si cada ciclo duplica la cantidad, después de *n* ciclos hay 2<sup>n</sup> veces la cantidad inicial. Con 20 ciclos: 2<sup>20</sup> = 1 048 576, es decir, del orden de **un millón** de copias. Conviene anclar la cuenta en un valor conocido: 2<sup>10</sup> ≈ 1000, de modo que 2<sup>20</sup> = (2<sup>10</sup>)<sup>2</sup> ≈ 1000 × 1000. Clave: **D**.

- **A** resulta de multiplicar 20 × 2, es decir, de suponer un crecimiento lineal. *Error de cálculo típico.*
- **B** resulta de elevar 20 al cuadrado. *Error de cálculo típico.*
- **C** resulta de multiplicar 20 por 1000, mezclando ambos errores. *Error de cálculo típico.*

**Qué hay que saber y saber hacer:** distinguir crecimiento exponencial de crecimiento lineal y manejar potencias de dos. *Atajo:* memoriza que 2<sup>10</sup> ≈ mil, 2<sup>20</sup> ≈ un millón y 2<sup>30</sup> ≈ mil millones; con eso se resuelve cualquier ítem de PCR sin calculadora.
:::

::: ejemplo
**Ejemplo 3 · Habilidad: Evaluar**

Un grupo de estudiantes transforma bacterias con un plásmido que lleva el gen de interés y un gen de resistencia a la ampicilina. Luego siembra las bacterias en un medio de cultivo **con ampicilina** y observa que crecen algunas colonias. Uno de ellos concluye: «La ampicilina hizo que las bacterias se volvieran resistentes».

¿Cuál es el error de esa conclusión?

- **A)** Confunde el gen de resistencia con el gen de interés del plásmido usado.
- **B)** Supone que el antibiótico genera la resistencia, cuando solo elimina a las no transformadas.
- **C)** Supone que la resistencia a la ampicilina no puede transmitirse a las células hijas.
- **D)** Confunde la transformación bacteriana con el proceso de conjugación entre bacterias.

**Resolución.** Esta pregunta evalúa la habilidad de *evaluar*: juzgar la consistencia de una conclusión frente al procedimiento realizado. La tarea consiste en identificar qué papel cumple realmente el antibiótico.

El plásmido ya traía el gen de resistencia antes de entrar en las bacterias. Al sembrar en un medio con ampicilina, mueren todas las bacterias que **no** incorporaron el plásmido y sobreviven las que sí. El antibiótico no induce nada: actúa como un **filtro** que permite identificar a las transformadas. Es el paso 5 del procedimiento. Clave: **B**.

- **A** describe una confusión que la conclusión citada no comete. *Verdadero pero irrelevante.*
- **C** afirma lo contrario de lo que ocurre: el plásmido se replica y pasa a las células hijas. *Relación inversa o inexistente.*
- **D** introduce un proceso distinto, que no forma parte del experimento descrito. *Variable equivocada.*

**Qué hay que saber y saber hacer:** conocer la función del gen marcador y distinguir seleccionar de inducir. *Dato:* es el mismo razonamiento del capítulo 9 sobre la resistencia a antibióticos en la naturaleza. Aquí la selección se aplica a propósito; allá ocurre sola. El mecanismo es idéntico.
:::

::: ejemplo
**Ejemplo 4 · Habilidad: Evaluar**

Dos cultivos de tomate se comparan durante una temporada. El cultivo 1 corresponde a una variedad modificada genéticamente para resistir a un hongo; el cultivo 2, a la variedad convencional. Ambos se riegan y fertilizan igual, pero el cultivo 1 se sembró en un terreno con mejor drenaje.

Al final, el cultivo 1 produjo un 30 % más de fruta. El informe concluye que la modificación genética aumenta el rendimiento.

¿Cuál es la principal objeción a esa conclusión?

- **A)** El tamaño de la muestra es insuficiente para obtener conclusiones válidas.
- **B)** La variedad modificada y la convencional pertenecen a especies diferentes.
- **C)** El tipo de terreno difiere entre ambos cultivos y pudo influir en el resultado.
- **D)** El rendimiento debió medirse en kilogramos y no como un porcentaje.

**Resolución.** Esta pregunta evalúa la habilidad de *evaluar*: juzgar si un diseño permite atribuir un efecto a la variable estudiada. La tarea consiste en revisar qué variables quedaron controladas y cuáles no.

Para atribuir la diferencia a la modificación genética, todo lo demás debe mantenerse igual. El enunciado declara iguales el riego y la fertilización, pero informa una diferencia adicional: el **drenaje del terreno**. Como el drenaje afecta el rendimiento por sí solo, ambos factores quedan confundidos y no se puede saber cuánto aportó cada uno. Clave: **C**.

- **A** invoca el tamaño de muestra, sobre el que el enunciado no entrega información. *Sub-alcance.*
- **B** es falsa: ambas son variedades de la misma especie. *Relación inversa o inexistente.*
- **D** propone un cambio de unidad que no corrige el problema del diseño. *Verdadero pero irrelevante.*

**Qué hay que saber y saber hacer:** identificar variables independientes, dependientes y controladas, y detectar factores confundidos. *Dato para la PAES:* cuando un enunciado se detiene a mencionar una diferencia entre los grupos que no era necesaria para la historia, casi siempre es ahí donde está el problema del diseño.
:::
