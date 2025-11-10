---
title: "Notas de estado de I2P del 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Actualización semanal del estado de I2P que abarca la versión 0.4, problemas de capacidad de la red, actualizaciones del sitio web y mejoras en la interfaz de I2PTunnel"
categories: ["status"]
---

Hola a todos, perdón por llegar tarde...

## Índice:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Como estoy seguro de que todos han visto, la versión 0.4 salió el otro día y, en general, va bastante bien. Cuesta creer que hayan pasado 6 meses desde que salió la 0.3 (y un año desde que se publicó el SDK 1.0 (kit de desarrollo de software)), pero hemos avanzado mucho, y el trabajo duro, el entusiasmo y la paciencia de todos ustedes han hecho maravillas. ¡Felicidades y gracias!

Como en todo buen lanzamiento, en cuanto salió encontramos algunos problemas, y en los últimos días hemos estado recibiendo informes de errores y aplicando parches sin parar (puedes seguir los cambios a medida que se corrigen). Aún nos quedan algunos errores por corregir antes de publicar la próxima versión, pero eso debería estar hecho en un día más o menos.

## 2) Capacidad y sobrecarga

Hemos visto algunas asignaciones de tunnels bastante sesgadas en las últimas versiones y, aunque algunas de ellas están relacionadas con errores (dos de ellas se han corregido desde que salió la 0.4), todavía queda una pregunta general sobre el algoritmo: ¿cuándo debería un router dejar de aceptar más tunnels?

Hace algunas revisiones, añadimos código de limitación (throttling) para rechazar solicitudes para participar en un tunnel si el router estaba sobrecargado (el tiempo de procesamiento local de mensajes supera 1s), y eso ha ayudado sustancialmente. Sin embargo, hay dos aspectos de ese algoritmo simple que no se abordan: - cuando nuestro ancho de banda está saturado, nuestro tiempo de procesamiento local puede seguir siendo rápido, por lo que seguiríamos aceptando más solicitudes de tunnel - cuando un solo par participa en "demasiados" tunnels, cuando fallan, perjudican más a la red.

El primer problema se resuelve bastante fácilmente simplemente activando el limitador de ancho de banda (ya que la limitación de ancho de banda ralentiza el tiempo de procesamiento de mensajes de acuerdo con el retardo debido al ancho de banda). El segundo es más complicado, y se necesita más investigación y más simulación. Estoy pensando en algo en la línea de rechazar probabilísticamente las solicitudes de tunnel en función de la proporción entre los tunnels en los que se participa y los tunnels solicitados desde la red, incluyendo algún "factor de amabilidad" base, estableciendo P(reject) = 0 si estamos participando en menos que eso.

Pero, como dije, se necesita más trabajo y simulación.

## 3) Actualizaciones del sitio web

Ahora que tenemos la nueva interfaz web de I2P, prácticamente toda nuestra documentación antigua para usuarios finales está obsoleta. Necesitamos ayuda para revisar esas páginas y actualizarlas para que describan cómo están las cosas ahora. Como han sugerido duck y otros, necesitamos una nueva guía de arranque rápido además del readme de `http://localhost:7657/` - algo que ayude a la gente a ponerse en marcha y entrar en el sistema.

Además, nuestra nueva interfaz web tiene espacio de sobra para integrar ayuda contextual. Como puedes ver en el help.jsp incluido, "mmm. probablemente deberíamos tener aquí algún texto de ayuda."

Probablemente sería estupendo si pudiéramos añadir enlaces de 'Acerca de' y/o 'Solución de problemas' a las distintas páginas, explicando qué significan las cosas y cómo usarlas.

## 4) Interfaz web de I2PTunnel

Llamar "espartana" a la nueva interfaz `http://localhost:7657/i2ptunnel/` sería quedarse corto. Tenemos mucho trabajo por hacer para acercarla a un estado utilizable - ahora mismo la funcionalidad está técnicamente ahí, pero realmente hay que saber qué está pasando entre bastidores para que tenga sentido. Creo que duck puede tener algunas ideas adicionales al respecto para plantear durante la reunión.

## 5) Hoja de ruta y tareas pendientes

He descuidado mantener la hoja de ruta actualizada, pero la realidad es que tenemos alguna revisión adicional por delante. Para ayudar a explicar lo que veo como los "grandes problemas", he elaborado una nueva lista de tareas, que entra en cierto detalle sobre cada una. Creo que a estas alturas deberíamos estar bastante abiertos a revisar nuestras opciones y quizá replantear la hoja de ruta.

Una cosa que he olvidado mencionar en esa lista de tareas es que, al añadir el protocolo de conexión ligero, podemos incluir (opcional) la autodetección de la dirección IP. Esto puede ser 'peligroso' (por eso será opcional), pero reducirá drásticamente la cantidad de solicitudes de soporte que recibimos :)

De todos modos, esos asuntos publicados en la lista de tareas son los que hemos previsto para varias versiones, y con toda seguridad no estarán todos en la 1.0 ni siquiera en la 2.0. He esbozado algunas posibles priorizaciones / versiones, pero aún no estoy totalmente decidido al respecto. Sin embargo, si la gente puede identificar otras cosas importantes más adelante, se agradecería mucho, ya que un asunto no programado siempre es un dolor de cabeza.

## 6) ???

Bien, eso es todo lo que tengo por ahora (menos mal, porque la reunión empieza en unos minutos). Pásate por #i2p en irc.freenode.net, www.invisiblechat.com o irc.duck.i2p a las 21:00 GMT para seguir charlando.
