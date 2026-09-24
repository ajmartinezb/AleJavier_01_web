## 5. Control del ciclo celular: los puntos de control

El ciclo celular no avanza «automáticamente». Funciona como una línea de montaje con **inspectores**: en ciertos momentos, la célula verifica que todo esté en orden antes de seguir. Esos momentos son los **puntos de control**. El temario DEMRE pide conocer tres.

| Punto de control | Qué verifica | Si algo está mal… |
|---|---|---|
| **G1–S** (al final de G1) | Que la célula tenga el **tamaño** adecuado, suficientes **nutrientes**, **señales** que la estimulen a dividirse (factores de crecimiento) y un **ADN sin daños** | Se detiene en G1 para reparar el ADN, o entra en G0. Si el daño es irreparable, puede activar la **apoptosis** (muerte celular programada). Es el punto de «no retorno»: si se supera, la célula se compromete a dividirse |
| **G2–M** (al final de G2) | Que el ADN se haya **replicado completo y sin errores** | Se detiene la entrada a mitosis hasta que se repare el ADN |
| **De metafase** (del huso) | Que **todos los cinetocoros** estén unidos a microtúbulos de ambos polos | La anafase no comienza. Así se evita que una célula hija quede con cromosomas de más o de menos |

::: tip
**Razonar con alteraciones.** Si una toxina desactiva el punto de control de metafase, las cromátidas se pueden separar aunque algunos cromosomas no estén bien unidos al huso: se producirán células hijas con **números anormales de cromosomas**. Si además se inhiben las moléculas que inducen la apoptosis, esas células anormales **no morirán** y podrían seguir dividiéndose sin control. Este es el razonamiento de una pregunta de la prueba oficial de invierno de 2027.
:::

### a. Ciclinas y quinasas: el motor del ciclo

El avance del ciclo depende de un grupo de proteínas reguladoras:

- **Quinasas dependientes de ciclinas (Cdk):** enzimas que activan o desactivan otras proteínas agregándoles grupos fosfato. Están siempre presentes, pero solo funcionan cuando se unen a una ciclina.
- **Ciclinas:** proteínas cuya concentración **sube y baja** a lo largo del ciclo. Se fabrican en una etapa y se destruyen en la siguiente.

Cada combinación de ciclina y Cdk impulsa una transición: una lleva la célula de G1 a S y otra, de G2 a mitosis. El complejo que dispara la mitosis se llamó **MPF**, «factor promotor de la fase M».

::: nota
**Un experimento clásico: la fusión de células.** En 1970, los investigadores Rao y Johnson fusionaron células que estaban en distintas fases del ciclo:

- Al fusionar una célula en **fase S** con una en **G1**, el núcleo en G1 **empezó a replicar su ADN** antes de tiempo.
- Al fusionar una célula en **mitosis** con una en interfase, el núcleo en interfase **condensó su cromatina** de inmediato, como si entrara en mitosis.

**Conclusión:** el citoplasma contiene **señales químicas** que controlan el avance del ciclo. Esas señales resultaron ser los complejos ciclina-Cdk.
:::

::: nota
**Otro experimento: las ciclinas del erizo de mar.** A comienzos de la década de 1980, Tim Hunt estudió embriones de erizo de mar, que se dividen rápido y en forma sincronizada. Encontró una proteína que se acumulaba durante cada interfase y **desaparecía bruscamente al final de cada mitosis**, y la llamó **ciclina**. Por los descubrimientos sobre el control del ciclo, Hunt, Paul Nurse y Leland Hartwell recibieron el Premio Nobel de Medicina en 2001.
:::

### b. Genes que aceleran y genes que frenan

El control del ciclo depende de dos grupos de genes, que funcionan como el acelerador y el freno de un auto:

| Tipo | Función normal | Cuando mutan… | Ejemplos |
|---|---|---|---|
| **Protooncogenes** (el acelerador) | Codifican proteínas que **estimulan** la división en respuesta a señales: receptores de factores de crecimiento, proteínas que transmiten la señal | Se convierten en **oncogenes**: estimulan la división **aunque no haya señal**, como un acelerador trabado. Basta con que **una** copia mute | *RAS*, receptor de EGF |
| **Genes supresores de tumores** (el freno) | Codifican proteínas que **detienen** el ciclo si hay problemas, reparan el ADN o inducen la apoptosis | Se pierde el freno. En general deben fallar **las dos** copias | ***TP53*** (proteína p53, «guardián del genoma»), ***RB***, *BRCA1* |

::: tip
**La proteína p53** se activa cuando el ADN está dañado. Detiene el ciclo en G1 para que se repare, y si el daño es muy grave, ordena la apoptosis. Está alterada en cerca de la mitad de los cánceres humanos. Sin p53, una célula con el ADN dañado sigue dividiéndose y acumula más mutaciones.
:::
