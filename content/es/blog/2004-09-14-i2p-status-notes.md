---
title: "Notas de estado de I2P del 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Actualización semanal del estado de I2P que abarca la versión 0.4.0.1, actualizaciones del modelo de amenazas, mejoras en el sitio web, cambios en la hoja de ruta y necesidades de desarrollo de aplicaciones cliente"
categories: ["status"]
---

Hi y'all, its that time of the week again

## Índice:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Desde el lanzamiento 0.4.0.1 del miércoles pasado, las cosas han ido bastante bien en la red - más de 2/3 de la red se ha actualizado, y hemos mantenido entre 60 y 80 routers en la red. Los tiempos de conexión a IRC varían, pero últimamente las conexiones de 4-12 horas han sido normales. Sin embargo, ha habido algunos informes de comportamiento extraño al iniciar en OS/X, aunque creo que también se están logrando avances en ese frente.

## 2) Actualizaciones del modelo de amenazas

Como mencioné en respuesta a la publicación de Toni, ha habido una reescritura bastante sustancial del modelo de amenazas. La diferencia principal es que, en lugar de abordar las amenazas de manera ad hoc como antes, intenté seguir algunas de las taxonomías propuestas en la literatura. El mayor problema para mí fue encontrar formas de encajar las técnicas concretas que la gente puede utilizar en los patrones propuestos; a menudo, un solo ataque encajaba en varias categorías distintas. Por ello, no estoy del todo satisfecho con cómo se transmite la información en esa página, pero es mejor que antes.

## 3) Actualizaciones del sitio web

Gracias a la ayuda de Curiosity, hemos empezado con algunas actualizaciones del sitio web - la más visible de las cuales se puede ver en la propia página de inicio. Esto debería ayudar a quienes se topan con I2P y quieren saber de inmediato qué demonios es esto de I2P, en lugar de tener que ir buscando y rebuscando por las distintas páginas. En cualquier caso, progreso; siempre hacia adelante :)

## 4) Hoja de ruta

Hablando de avances, por fin he elaborado una hoja de ruta renovada basada en lo que considero que necesitamos implementar y en lo que debe lograrse para satisfacer las necesidades del usuario. Los principales cambios respecto a la hoja de ruta anterior son:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Los otros elementos programados para varias versiones 0.4.* ya se han implementado. Sin embargo, hay otra cosa que se eliminó de la hoja de ruta...

## 5) Aplicaciones cliente

Necesitamos aplicaciones cliente. Aplicaciones que sean atractivas, seguras, escalables y anónimas. I2P por sí solo no hace mucho; simplemente permite que dos extremos se comuniquen entre sí de forma anónima. Si bien I2PTunnel ofrece una auténtica navaja suiza muy potente, herramientas como esa solo resultan realmente atractivas para los entusiastas de la tecnología. Necesitamos más que eso: necesitamos algo que permita a las personas hacer lo que realmente quieren hacer y que, además, les ayude a hacerlo mejor. Necesitamos un motivo para que la gente use I2P más allá de simplemente porque es más seguro.

Hasta ahora he estado promoviendo MyI2P para satisfacer esa necesidad - un sistema de blogs distribuido que ofrece una interfaz al estilo de LiveJournal. Recientemente comenté en la lista parte de la funcionalidad dentro de MyI2P. Sin embargo, lo he retirado de la hoja de ruta, ya que es simplemente demasiado trabajo para mí y no podría, al mismo tiempo, darle a la red base de I2P la atención que necesita (ya estamos extremadamente justos de recursos).

Hay algunas otras aplicaciones que tienen mucho potencial. Stasher proporcionaría una infraestructura significativa para el almacenamiento de datos distribuido, pero no estoy seguro de cómo está avanzando. Aun con Stasher, sin embargo, haría falta una interfaz de usuario atractiva (aunque algunas aplicaciones FCP podrían funcionar con él).

IRC también es un sistema potente, aunque tiene sus limitaciones debido a la arquitectura basada en servidores. oOo ha realizado algo de trabajo para ver cómo implementar DCC transparente, de modo que quizá la parte de IRC podría usarse para chat público y DCC para transferencias de archivos privadas o chat sin servidor.

La funcionalidad general de eepsite(I2P Site) también es importante, y lo que tenemos ahora es completamente insatisfactorio. Como señala DrWoo, existen riesgos significativos para el anonimato con la configuración actual, y aunque oOo ha hecho algunos parches filtrando algunos encabezados, hay mucho más trabajo por hacer antes de que los eepsites(I2P Sites) puedan considerarse seguros. Hay varios enfoques distintos para abordar esto, todos los cuales pueden funcionar, pero todos requieren trabajo. Sé que duck mencionó que tenía a alguien trabajando en algo, aunque no sé cómo va eso o si podría integrarse en I2P para que todos lo usen o no. ¿Duck?

Otro par de aplicaciones cliente que podrían ayudar serían una aplicación de transferencia de archivos swarming (distribución por enjambres, al estilo de BitTorrent) o una aplicación de intercambio de archivos más tradicional (al estilo de DC/Napster/Gnutella/etc). Esto es lo que sospecho que mucha gente quiere, pero hay problemas con cada uno de estos sistemas. Sin embargo, son bien conocidos y portarlos puede que no resulte demasiado problemático (quizá).

Bien, lo anterior no es nada nuevo - ¿por qué saqué todos esos temas? Bueno, necesitamos encontrar la manera de implementar una aplicación cliente que sea atractiva, segura, escalable y anónima, y eso no va a ocurrir por sí solo, de la nada. He llegado a aceptar que no voy a poder hacerlo por mi cuenta, así que debemos ser proactivos y encontrar la manera de llevarlo a cabo.

Para lograrlo, creo que nuestro sistema de recompensas puede ayudar, pero pienso que una de las razones por las que no hemos visto mucha actividad en ese frente (personas trabajando en implementar una recompensa) es porque están demasiado dispersos. Para obtener los resultados que necesitamos, considero que debemos priorizar lo que queremos y concentrar nuestros esfuerzos en ese elemento principal, 'endulzar el trato' para, con suerte, animar a alguien a dar un paso al frente y trabajar en la recompensa.

Mi opinión personal sigue siendo que un sistema de blogs seguro y distribuido como MyI2P sería lo mejor. En lugar de simplemente mover datos de un lado a otro de forma anónima, ofrece una manera de construir comunidades, la savia vital de cualquier esfuerzo de desarrollo. Además, ofrece una relación señal/ruido relativamente alta, baja probabilidad de abuso de los bienes comunes y, en general, una carga de red ligera. Sin embargo, no ofrece toda la riqueza de los sitios web normales, pero los 1,8 millones de usuarios activos de LiveJournal no parecen echarla de menos.

Más allá de eso, asegurar la arquitectura de eepsite(I2P Site) sería mi siguiente preferencia, proporcionando a los navegadores la seguridad que necesitan y permitiendo que la gente sirva eepsites(I2P Sites) 'sin configuración previa'.

La transferencia de archivos y el almacenamiento de datos distribuido también son increíblemente potentes, pero no parecen estar tan orientados a la comunidad como probablemente querríamos para la primera aplicación normal para el usuario final.

Quiero que todas las aplicaciones enumeradas estén implementadas para ayer, así como otras mil aplicaciones que ni podría empezar a imaginar. También quiero la paz mundial, el fin del hambre, la destrucción del capitalismo, la liberación del estatismo, del racismo, del sexismo y de la homofobia, y el fin de la destrucción abierta del medio ambiente y todas esas otras cosas malas. Sin embargo, somos un número limitado de personas y solo podemos hacer tanto. Por ello, debemos priorizar y concentrar nuestros esfuerzos en lograr lo que sí podemos, en lugar de quedarnos de brazos cruzados, abrumados por todo lo que queremos hacer.

Tal vez podamos hablar de algunas ideas sobre lo que deberíamos hacer en la reunión de esta noche.

## 6) ???

Bueno, eso es todo lo que tengo por el momento, y oye, ¡terminé de redactar las notas de estado *antes* de la reunión! Así que nada de excusas, pásate a las 9 p. m. GMT y inúndanos a todos con tus ideas.

=jr
