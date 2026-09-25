## 8. Potencia y energía eléctrica

### a. La potencia eléctrica

La **potencia** (*P*) de un artefacto es la **energía que transforma por unidad de tiempo**. Como cada coulomb que atraviesa un elemento con voltaje *V* le entrega *V* joules, y por segundo pasan *I* coulomb, la potencia es:

<p style="text-align:center"><strong><em>P</em> = <em>V</em> · <em>I</em></strong></p>

Su unidad es el **watt (W)**: 1 W = 1 J/s = 1 V · 1 A. Combinando con la ley de Ohm se obtienen otras dos formas:

<p style="text-align:center"><strong><em>P</em> = <em>I</em>² · <em>R</em></strong> &nbsp;&nbsp;&nbsp;&nbsp; <strong><em>P</em> = <em>V</em>² / <em>R</em></strong></p>

::: nota
**Cuál usar.** Las tres dan lo mismo; conviene elegir la que usa los datos conocidos. En un circuito **en serie**, la corriente es común y resulta cómodo *P* = *I*² · *R*: la resistencia **mayor** disipa **más** potencia. En un circuito **en paralelo** (como una casa), el voltaje es común y resulta cómodo *P* = *V*² / *R*: la resistencia **menor** disipa **más** potencia.
:::

::: ejemplo
**Leer la placa de un hervidor.** Un hervidor dice «220 V – 2 000 W».

- Corriente que consume: *I* = *P* / *V* = 2 000 / 220 ≈ **9,1 A**.
- Resistencia de su elemento calefactor: *R* = *V*² / *P* = 220² / 2 000 ≈ **24 Ω**.

Si se conectara a 110 V (la mitad), su potencia sería (110)² / 24 ≈ 500 W: **la cuarta parte**, porque la potencia depende del **cuadrado** del voltaje. Por eso un artefacto hecho para 220 V funciona mal en un país con 110 V.
:::

::: tip
**¿Más resistencia, más potencia?** Depende de qué se mantenga fijo. Con el **mismo voltaje** (en paralelo, en una casa), **menos** resistencia significa **más** potencia: un calefactor de 2 000 W tiene menos resistencia que una ampolleta de 60 W. Con la **misma corriente** (en serie), **más** resistencia significa **más** potencia. Por eso, dos ampolletas distintas brillan al revés según se conecten en serie o en paralelo.
:::

### b. La energía eléctrica

La **energía** que consume un artefacto es su potencia por el tiempo que funciona:

<p style="text-align:center"><strong><em>E</em> = <em>P</em> · <em>t</em></strong></p>

En el SI, con *P* en watt y *t* en segundos, la energía queda en **joule**. Pero para el consumo doméstico el joule es una unidad muy pequeña, y se usa el **kilowatt-hora (kWh)**: la energía que consume un artefacto de 1 kW (1 000 W) durante 1 hora.

<p style="text-align:center">1 kWh = 1 000 W · 3 600 s = <strong>3,6 × 10<sup>6</sup> J</strong></p>

::: tip
**El kWh es energía, no potencia.** «Kilowatt» mide potencia (qué tan rápido se usa la energía); «kilowatt-hora» mide energía (cuánta se usó en total). Un artefacto de 100 W encendido 10 horas consume lo mismo que uno de 1 000 W encendido 1 hora: **1 kWh**.
:::

### c. Calcular la cuenta de la luz

El medidor de una casa registra los kWh consumidos, y la empresa distribuidora cobra un precio por cada kWh. Para calcular el costo de usar un artefacto:

1. Pasar la potencia a **kW** (dividir los watt por 1 000).
2. Multiplicar por las **horas** de uso: se obtienen los **kWh**.
3. Multiplicar por el **precio del kWh**.

::: ejemplo
**Cuánto cuesta usar algunos artefactos.** Supón un precio de $200 por kWh (valor ilustrativo: el precio real depende de la comuna, la empresa y el año, y figura en cada boleta).

| Artefacto | Potencia | Uso diario | kWh al mes (30 días) | Costo mensual |
|---|---|---|---|---|
| Hervidor | 2 000 W | 15 min | 2 kW · 0,25 h · 30 = **15 kWh** | **$3 000** |
| Refrigerador | 150 W (promedio) | 24 h | 0,15 · 24 · 30 = **108 kWh** | **$21 600** |
| Ampolleta LED | 9 W | 5 h | 0,009 · 5 · 30 = **1,35 kWh** | **$270** |
| Ampolleta incandescente | 60 W | 5 h | 0,06 · 5 · 30 = **9 kWh** | **$1 800** |

El refrigerador, aunque tiene poca potencia, es el que más consume porque funciona todo el día. En el consumo lo que importa es **potencia por tiempo**.
:::

### d. El efecto Joule

Cuando la corriente atraviesa una resistencia, los choques de los electrones con los átomos transforman energía eléctrica en **calor**. Es el **efecto Joule**, y su potencia es *P* = *I*² · *R*.

- Es **útil** en hervidores, estufas, planchas, secadores de pelo, tostadores, duchas y calefonts eléctricos.
- Es una **pérdida** en los cables, los motores y los cargadores, que se calientan sin que eso sirva de nada. Como depende de *I*², las pérdidas crecen rápido con la corriente: por eso la electricidad se transporta por las líneas de alta tensión con **alto voltaje y baja corriente**.
- Es un **peligro** cuando un cable lleva más corriente de la que soporta: se calienta, derrite su aislante y puede causar un incendio.
