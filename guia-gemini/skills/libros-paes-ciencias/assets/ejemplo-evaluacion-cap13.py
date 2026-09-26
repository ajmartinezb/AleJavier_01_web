"""Evaluación formativa del capítulo 13 de Física (la Tierra y el Universo)."""
from collections import Counter
P = [
("C", "¿Cómo explica el modelo heliocéntrico el movimiento retrógrado de Marte?",
 ["Marte invierte de verdad su sentido de giro por unas semanas.", "Marte se mueve en un epiciclo que gira sobre un deferente.", "La Tierra, más rápida, adelanta a Marte.", "El Sol atrae a Marte con más fuerza cuando está en su afelio."],
 "Es un efecto de perspectiva: cuando la Tierra, en una órbita interior y más rápida, adelanta a Marte, este parece retroceder respecto de las estrellas lejanas. Los epiciclos son la explicación de Ptolomeo."),
("A", "¿Cuál es la causa de las estaciones del año?",
 ["La inclinación del eje de rotación de la Tierra.", "La variación de la distancia entre la Tierra y el Sol.", "Los cambios en la energía que emite el Sol en el año.", "La variación de la rapidez de rotación de la Tierra."],
 "El eje inclinado hace que cada hemisferio reciba los rayos del Sol más directos y por más horas en una parte del año. La distancia varía solo un 3 %, y la Tierra está más cerca del Sol en enero, que es verano en Chile e invierno en el hemisferio norte."),
("B", "Eratóstenes midió un ángulo de 7,2° entre Siena y Alejandría, separadas por unos 800 km. ¿Qué circunferencia terrestre obtuvo?",
 ["5 760 km", "40 000 km", "57 600 km", "400 000 km"],
 "7,2° es 1/50 de 360°, así que la circunferencia es 50 × 800 km = 40 000 km. Multiplicar 7,2 × 800 da 5 760, y otros errores de proporción dan los demás valores."),
("D", "Según Aristóteles, ¿qué caracterizaba al mundo supralunar?",
 ["Estaba formado por tierra, agua, aire y fuego.", "Sus cuerpos caían en línea recta hacia la Tierra.", "Estaba sometido a cambios, nacimientos y muertes.", "Era perfecto, inmutable y con movimientos circulares."],
 "Desde la Luna hacia afuera, el cosmos de Aristóteles estaba hecho de éter, era perfecto e inmutable y solo tenía movimientos circulares uniformes. Los cuatro elementos, el cambio y la caída en línea recta pertenecían al mundo sublunar."),
("C", "¿Qué argumento usaban los defensores del geocentrismo para afirmar que la Tierra no gira alrededor del Sol?",
 ["Que el Sol se ve más grande que las estrellas.", "Que la Luna muestra fases a lo largo del mes.", "Que no se observaba paralaje en las estrellas.", "Que los planetas tienen movimiento retrógrado."],
 "Si la Tierra se moviera alrededor del Sol, las estrellas cercanas deberían cambiar de posición a lo largo del año. No se observaba porque las estrellas están muy lejos: la paralaje se midió recién en 1838."),
("A", "¿Qué función cumplían los epiciclos en el modelo de Ptolomeo?",
 ["Explicar el retroceso y los cambios de brillo de los planetas.", "Explicar por qué las estaciones del año tienen distinta duración.", "Explicar la forma elíptica de las órbitas de los planetas.", "Explicar por qué la Tierra rota sobre su propio eje."],
 "Cuando el planeta recorre la parte interior de su epiciclo, visto desde la Tierra retrocede y está más cerca, por lo que se ve más brillante. Ptolomeo no usaba elipses, y en su modelo la Tierra no rota."),
("B", "¿Qué afirmación sobre el modelo de Copérnico es correcta?",
 ["Usaba órbitas elípticas y por eso era mucho más preciso.", "Seguía usando círculos y epiciclos para ajustar los datos.", "Ubicaba al Sol en el centro de toda la Vía Láctea.", "Fue confirmado de inmediato por la paralaje estelar."],
 "Copérnico conservó los círculos perfectos y necesitó epiciclos pequeños; su modelo no era más preciso que el de Ptolomeo. Las elipses llegaron con Kepler, y la paralaje se midió en 1838."),
("D", "Tycho Brahe observó que la «estrella nueva» de 1572 no tenía paralaje diaria. ¿Qué concluyó?",
 ["Que era un fenómeno de la atmósfera terrestre.", "Que la Tierra giraba en torno al Sol cada año.", "Que era un planeta desconocido hasta entonces.", "Que estaba más allá de la Luna, en el cielo."],
 "Sin paralaje, el objeto debía estar más allá de la Luna. Eso contradecía la idea de Aristóteles de un mundo supralunar inmutable. Tycho, sin embargo, no aceptó que la Tierra se moviera."),
("C", "¿Qué observación de Galileo refutó directamente el modelo de Ptolomeo?",
 ["Las montañas y cráteres en la superficie de la Luna.", "Las manchas que se desplazan sobre el disco del Sol.", "Las fases completas de Venus y su cambio de tamaño.", "Las numerosas estrellas que forman la Vía Láctea."],
 "En el modelo de Ptolomeo, Venus solo podría verse nueva o creciente. Verla casi llena exige que Venus pase por detrás del Sol, es decir, que gire a su alrededor. Las otras observaciones contradicen la perfección del cielo, no la posición de la Tierra."),
("B", "¿Qué mostraban las cuatro lunas de Júpiter descubiertas por Galileo?",
 ["Que Júpiter es el planeta más grande del sistema solar.", "Que hay cuerpos que no giran en torno a la Tierra.", "Que la Tierra gira alrededor del Sol una vez al año.", "Que las órbitas de los planetas son elípticas."],
 "Las lunas giran en torno a Júpiter, no en torno a la Tierra: no todo en el cielo gira alrededor nuestro. Pero esa observación no prueba por sí sola que la Tierra se mueva alrededor del Sol."),
("A", "En un barco que navega con velocidad constante, se suelta una piedra desde lo alto del mástil. ¿Dónde cae?",
 ["Al pie del mástil, igual que con el barco detenido.", "Detrás del mástil, porque el barco avanza mientras cae.", "Delante del mástil, porque la piedra conserva más impulso.", "Depende de la rapidez con que navegue el barco."],
 "Por inercia, la piedra comparte la velocidad horizontal del barco y cae al pie del mástil. Con ese argumento Galileo explicó por qué no notamos el movimiento de la Tierra."),
("D", "¿Qué dice la primera ley de Kepler?",
 ["Los planetas se mueven en círculos con el Sol en el centro.", "Los planetas van más rápido cuando están cerca del Sol.", "El cuadrado del período es proporcional al cubo de a.", "Las órbitas son elipses, con el Sol en un foco."],
 "La primera ley habla de la forma de la órbita: una elipse con el Sol en un foco, no en el centro. La rapidez variable es la segunda ley y la relación T²–a³, la tercera."),
("C", "Según la segunda ley de Kepler, ¿en qué punto de su órbita la Tierra se mueve más rápido?",
 ["En el afelio, porque está más lejos del Sol.", "En todos los puntos por igual, porque la órbita es cerrada.", "En el perihelio, a inicios del mes de enero.", "En los equinoccios de marzo y septiembre."],
 "La línea Sol–planeta barre áreas iguales en tiempos iguales; cerca del Sol esa línea es más corta y el planeta debe recorrer un arco más largo. Por eso va más rápido en el perihelio, que la Tierra alcanza a comienzos de enero."),
("A", "Un asteroide gira alrededor del Sol con un semieje mayor de 9 UA. ¿Cuál es su período?",
 ["27 años", "18 años", "9 años", "4,3 años"],
 "T² = a³ = 9³ = 729, así que T = √729 = 27 años. Suponer T proporcional a a da 9 años; T = a<sup>2/3</sup> da 4,3 años."),
("B", "¿Qué explicó Newton con la ley de gravitación universal?",
 ["Por qué la Tierra está en el centro del universo.", "Por qué los planetas cumplen las leyes de Kepler.", "Por qué las estrellas brillan con luz propia.", "Por qué el universo se está expandiendo."],
 "Newton dedujo las tres leyes de Kepler a partir de sus leyes del movimiento y de una fuerza que disminuye con el cuadrado de la distancia. Las leyes de Kepler describen; la gravitación las explica."),
("D", "La galaxia de Andrómeda está a unos 2,5 millones de años luz. ¿Qué significa esto?",
 ["Que la galaxia tiene 2,5 millones de años de edad.", "Que un viaje hasta ella duraría 2,5 millones de años.", "Que la galaxia dejará de existir en 2,5 millones de años.", "Que su luz tardó 2,5 millones de años en llegarnos."],
 "El año luz es una unidad de distancia: la que recorre la luz en un año. Por eso vemos Andrómeda como era hace 2,5 millones de años. No indica su edad, y una nave, mucho más lenta que la luz, tardaría muchísimo más."),
("C", "Una galaxia muestra la línea del hidrógeno de 656 nm en 682 nm. ¿Qué se concluye?",
 ["Que la galaxia se acerca a nosotros.", "Que la galaxia está formada solo por hidrógeno.", "Que la galaxia se aleja, con z ≈ 0,04.", "Que la galaxia es más fría que el Sol."],
 "La longitud de onda aumentó: corrimiento al rojo. z = (682 − 656) / 656 ≈ 0,04, lo que indica alejamiento, a unos 12 000 km/s. Acercarse daría corrimiento al azul."),
("A", "¿Por qué la radiación de fondo de microondas es una evidencia del Big Bang?",
 ["Es el resto enfriado de un universo que fue muy caliente y denso.", "Proviene de la estrella más cercana al Sol, Próxima Centauri.", "Muestra que las galaxias se alejan con rapidez proporcional a d.", "Demuestra que el universo se creó a partir de una explosión."],
 "La radiación llega por igual de todas direcciones y corresponde a 2,7 K: es la luz liberada hace unos 380 000 años, estirada por la expansión. La proporcionalidad v–d es otra evidencia (la ley de Hubble-Lemaître), y el Big Bang no fue una explosión en un punto."),
("B", "¿Qué observación NO permite distinguir entre la teoría del Big Bang y la del estado estacionario?",
 ["La radiación de fondo de microondas.", "El corrimiento al rojo de las galaxias.", "La proporción de 25 % de helio.", "Las diferencias de las galaxias lejanas."],
 "Las dos teorías aceptan que el universo se expande, así que ambas explican el corrimiento al rojo. La radiación de fondo, el helio primordial y la evolución de las galaxias las distinguen: solo el Big Bang los predice."),
("D", "Si la energía oscura aumentara con el tiempo hasta desgarrar galaxias, estrellas y átomos, ¿qué final tendría el universo?",
 ["Big Crunch", "Big Bounce", "Big Freeze", "Big Rip"],
 "Ese escenario se llama Big Rip, o gran desgarro. El Big Crunch es un colapso por la gravedad, el Big Freeze una expansión eterna con enfriamiento, y el Big Bounce un universo cíclico."),
]
assert len(P) == 20
print(Counter(p[0] for p in P))
h = ['<h2>Evaluación formativa</h2>',
     '<p>Veinte preguntas sobre el cielo visto desde la Tierra, los modelos geocéntricos y heliocéntrico, los aportes de Tycho Brahe, Galileo, Kepler y Newton, las escalas del universo y las teorías sobre su origen, evolución y destino. Responde todas y luego revisa las explicaciones.</p>', '']
for i, (k, enun, alts, exp) in enumerate(P, 1):
    h += [f'<div class="pregunta" data-correcta="{k}">', f'  <p class="enunciado"><strong>{i}.</strong> {enun}</p>', '  <ol class="alternativas">']
    h += [f'    <li data-letra="{L}">{a}</li>' for L, a in zip("ABCD", alts)]
    h += ['  </ol>', f'  <div class="respuesta"><p><strong>Respuesta correcta: {k}</strong></p><p>{exp}</p></div>', '</div>', '']
open('fisica/capitulos/cap13-tierra-universo/90-evaluacion-formativa.html', 'w', encoding='utf-8').write("\n".join(h))
pos = Counter()
for i, (k, _, alts, _) in enumerate(P, 1):
    L = [len(a) for a in alts]
    ki = "ABCD".index(k)
    rank = sorted(L, reverse=True).index(L[ki])
    pos[rank] += 1
    if L[ki] == max(L) and L.count(max(L)) == 1 and L[ki] - sorted(L)[-2] > 5:
        print("clave más larga:", i, L)
print("posición de largo de la clave (0 = más larga):", sorted(pos.items()))
