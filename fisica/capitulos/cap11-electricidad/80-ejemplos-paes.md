## Ejemplos PAES resueltos

Cuatro ítems al estilo de la prueba, resueltos paso a paso. Cúbrelos primero y después compara.

::: ejemplo
**Ejemplo 1 (Procesar y analizar la evidencia).** Un grupo aplica distintos voltajes a dos componentes, P y Q, y mide la corriente que circula por cada uno:

| Voltaje (V) | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| Corriente en P (A) | 0,10 | 0,20 | 0,30 | 0,40 |
| Corriente en Q (A) | 0,20 | 0,32 | 0,40 | 0,46 |

¿Cuál de las siguientes conclusiones es coherente con los datos?

A) P cumple la ley de Ohm con una resistencia de 20 Ω, y la resistencia de Q aumenta con el voltaje.
B) P y Q cumplen la ley de Ohm, porque en ambos la corriente aumenta con el voltaje.
C) P cumple la ley de Ohm con una resistencia de 0,05 Ω, y Q tiene resistencia constante.
D) Q cumple la ley de Ohm con una resistencia de 10 Ω, y la resistencia de P disminuye con el voltaje.

**Desarrollo.**

1. **Calcular *V* / *I* en cada fila.** En P: 2/0,10 = 20; 4/0,20 = 20; 6/0,30 = 20; 8/0,40 = 20 Ω. Es constante: P es **óhmico**, con *R* = 20 Ω.
2. **En Q:** 2/0,20 = 10; 4/0,32 = 12,5; 6/0,40 = 15; 8/0,46 ≈ 17,4 Ω. La resistencia **aumenta** con el voltaje: Q **no** es óhmico (se comporta como el filamento de una ampolleta que se calienta).
3. **Descartar.** B usa un criterio insuficiente: que la corriente aumente no basta, tiene que aumentar en **proporción**. C invierte el cociente (*I* / *V* = 0,05) y afirma que Q es constante. D confunde los dos componentes.

**Clave: A.**

**Lo que evalúa.** Usar una operación matemática (el cociente *V* / *I*) para decidir si un elemento cumple una ley.
:::

::: ejemplo
**Ejemplo 2 (Planificar y conducir una investigación).** Una estudiante quiere medir la corriente que pasa por una ampolleta y el voltaje entre sus extremos. Tiene una pila, la ampolleta, cables, un amperímetro y un voltímetro.

¿Cuál es la forma correcta de conectar los instrumentos?

A) El amperímetro en paralelo con la ampolleta y el voltímetro en serie con ella.
B) Ambos instrumentos en serie con la ampolleta, uno a cada lado.
C) El amperímetro en serie con la ampolleta y el voltímetro en paralelo con ella.
D) Ambos instrumentos en paralelo con la ampolleta, entre sus dos extremos.

**Desarrollo.**

1. **El amperímetro** debe medir la corriente que **atraviesa** la ampolleta: se intercala en el mismo camino, **en serie**. Su resistencia es muy baja para no alterar la corriente.
2. **El voltímetro** debe medir la diferencia de potencial **entre dos puntos**: se conecta a los extremos de la ampolleta, **en paralelo**. Su resistencia es muy alta para no desviar corriente.
3. **Descartar.** A intercambia las conexiones: el amperímetro en paralelo sería casi un cortocircuito y el voltímetro en serie casi cortaría la corriente. B y D ponen a uno de los dos en la conexión incorrecta.

**Clave: C.**

**Lo que evalúa.** Asociar cada instrumento con la variable que mide y con la forma correcta de incluirlo en el circuito.
:::

::: ejemplo
**Ejemplo 3 (Evaluar).** Una familia quiere reducir su cuenta de la luz y evalúa tres medidas. Con un precio de $200 por kWh:

- Medida 1: cambiar 6 ampolletas incandescentes de 60 W por LED de 9 W. Cada ampolleta se usa 4 horas al día.
- Medida 2: desenchufar un televisor que en espera consume 5 W, las 20 horas al día que no se usa.
- Medida 3: usar el hervidor (2 000 W) 5 minutos menos al día.

¿Cuál es la afirmación correcta sobre el ahorro mensual (30 días)?

A) La medida 3 ahorra más, porque el hervidor tiene la mayor potencia.
B) La medida 2 ahorra más, porque el televisor está en espera la mayor parte del día.
C) Las tres medidas ahorran lo mismo, porque todas reducen el consumo.
D) La medida 1 ahorra más, porque reduce mucha potencia durante varias horas.

**Desarrollo.**

1. **Medida 1:** ahorro de potencia 6 · (60 − 9) = 306 W = 0,306 kW, por 4 h · 30 días = **36,7 kWh** ≈ $7 300.
2. **Medida 2:** 0,005 kW · 20 h · 30 días = **3 kWh** ≈ $600.
3. **Medida 3:** 2 kW · (5/60) h · 30 días = **5 kWh** ≈ $1 000.
4. **Conclusión.** La medida 1 ahorra por lejos lo más. A comete el error de mirar solo la potencia sin considerar el **tiempo**. B sobrevalora un consumo de muy baja potencia. C no compara los valores.

**Clave: D.**

**Lo que evalúa.** Evaluar alternativas tecnológicas con un criterio cuantitativo: la energía es potencia **por** tiempo.
:::

::: ejemplo
**Ejemplo 4 (Observar y plantear preguntas).** En una casa, cada vez que se enciende la estufa eléctrica mientras funciona el hervidor, se desconecta el automático del circuito de la cocina. Con uno solo de los dos artefactos, el automático no se desconecta.

¿Cuál de las siguientes hipótesis explica mejor la observación?

A) El automático se desconecta porque la estufa tiene una fuga de corriente hacia la tierra.
B) La corriente total de los dos artefactos juntos supera la corriente máxima del automático.
C) El voltaje de la red baja a la mitad cuando se conectan dos artefactos a la vez.
D) El hervidor y la estufa están conectados en serie y se reparten la corriente.

**Desarrollo.**

1. **Qué patrón hay.** Cada artefacto por separado funciona; los dos juntos, no. Lo que cambia al agregar el segundo es la **corriente total** del circuito.
2. **Hipótesis coherente.** Los artefactos de una casa están en **paralelo**: sus corrientes se **suman**. Si la suma supera la corriente máxima del automático, este corta por **sobrecarga**. Se puede poner a prueba sumando las corrientes de placa (potencia / 220 V) y comparándolas con el valor del automático.
3. **Descartar.** A: una fuga a tierra la detectaría el **diferencial**, y ocurriría también con la estufa sola. C: en paralelo, cada artefacto recibe los 220 V completos. D: los enchufes no están en serie; si lo estuvieran, ninguno funcionaría bien.

**Clave: B.**

**Lo que evalúa.** Formular una hipótesis coherente con la observación y con el modelo del circuito en paralelo, y que se pueda comprobar.
:::
